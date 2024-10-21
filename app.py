from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, session
from OrderEstimationClass import OrderEstimation
from UserClass import User
from dbConnection import cnx, cursor
from employeeclass import Employee
from Notifyclass import Notify
from adminClass import Admin
from CustomersOrdersClass  import CustomerOrder


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions

@app.route("/", methods=["GET", "POST"])
def homepage():
    message = None  # To store any messages (success or error)

    if request.method == "POST":
        if "login" in request.form:
            username = request.form["username"]
            password = request.form["password"]

            user = User(username=username, password=password)
            message, id = user.login(cnx, cursor)

            if id:
                session['id'] = id  # Store user ID in the session
                return redirect("/index")
            else:
                message = "Login failed: Invalid username or password."

        elif "create_account" in request.form:
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]

            new_user = User(username=username, password=password, email=email)
            message = new_user.create_account(cnx, cursor)

    return render_template("homepage.html", message=message)

# Show previous orders
@app.route("/index")
def index():
    if 'id' not in session:
        return redirect("/login")

    user_id = session['id']

    query = """
    SELECT order_id, pizza_type, pizza_size, side_item1, side_item2, drink, total_price, order_date
    FROM orders
    WHERE user_id = %s
    ORDER BY order_date DESC
    """
    cursor.execute(query, (user_id,))
    previous_orders = cursor.fetchall()

    if not previous_orders:
        return render_template("index.html", orders=[])

    return render_template("index.html", orders=previous_orders)

@app.route("/order", methods=["GET", "POST"])
def order_page():
    if 'id' not in session:
        return redirect("/")

    if request.method == "POST":
        user_id = session['id']
        # Get the selected pizza type and size
        pizza_type_label = request.form.get("pizza_type_label")
        pizza_size_label = request.form.get("pizza_size_label")
        side_item1_label = request.form.get("side_item1_label")
        side_item2_label = request.form.get("side_item2_label")
        drink_label = request.form.get("drink_label")

        # Calculate total price
        total_price = float(request.form.get("total_price"))

        # Current date and time
        order_date = datetime.now()

        # Calculate estimated preparation time
        order_estimation = OrderEstimation(pizza_type_label, pizza_size_label, side_item1_label, side_item2_label, drink_label)
        estimated_time_minutes = order_estimation.calculate_estimation_time()
        estimated_time = order_date + timedelta(minutes=estimated_time_minutes)

        # Insert order into the database
        query = """
        INSERT INTO orders (user_id, pizza_type, pizza_size, side_item1, side_item2, drink, total_price, order_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, pizza_type_label, pizza_size_label, side_item1_label, side_item2_label, drink_label, total_price, order_date))
        cnx.commit()

        # Get the order_id of the last inserted order
        order_id = cursor.lastrowid

        # Fetch an available employee
        query_employee = """
        SELECT employee_id, name, role 
        FROM employees 
        WHERE is_available = TRUE
        LIMIT 1
        """
        cursor.execute(query_employee)
        employee = cursor.fetchone()

        if employee:
            employee_id, employee_name, employee_role = employee

            # Update the order to assign the employee
            update_order_query = """
            UPDATE orders
            SET employee_id = %s
            WHERE order_id = %s
            """

            cursor.execute(update_order_query, (employee_id, order_id))
            cnx.commit()

            # Notify and assign the order to the selected employee
            employee_obj = Employee(employee_id=employee_id, name=employee_name, role=employee_role)
            employee_obj.notify_new_order(order_id, {
                "pizza_type": pizza_type_label,
                "pizza_size": pizza_size_label,
                "side_item1": side_item1_label,
                "side_item2": side_item2_label,
                "drink": drink_label,
                "total_price": total_price
            })
            employee_obj.assign_order(order_id)
        else:
            print("No available employees found")

        # Render the confirmation page
        return render_template("confirmation.html", pizza_type=pizza_type_label, pizza_size=pizza_size_label,
                               side_item1=side_item1_label, side_item2=side_item2_label, drink=drink_label,
                               total_price=total_price, order_date=order_date.strftime("%Y-%m-%d %H:%M:%S"),
                               estimated_time=estimated_time.strftime("%Y-%m-%d %H:%M:%S"),
                               estimated_time_minutes=estimated_time_minutes)
    
    return render_template("order.html", user_id=session['id'])


@app.route("/reorder/<int:order_id>", methods=["GET", "POST"])
def reorder(order_id):
    if 'id' not in session:
        return redirect("/login")  # Redirect to login if not logged in

    user_id = session['id']  # Get the logged-in user's ID

    # Query to get the previous order details by order_id
    query = """
    SELECT pizza_type, pizza_size, side_item1, side_item2, drink, total_price 
    FROM orders
    WHERE order_id = %s AND user_id = %s
    """
    cursor.execute(query, (order_id, user_id))
    previous_order = cursor.fetchone()

    if previous_order:
        pizza_type, pizza_size, side_item1, side_item2, drink, total_price = previous_order

        # Recalculate the total price based on the current prices, if needed
        current_total_price = total_price  # Using the price stored from the previous order

        # Render the order page with pre-filled data for reorder
        return render_template("order.html", 
                               pizza_type=pizza_type, 
                               pizza_size=pizza_size,
                               side_item1=side_item1, 
                               side_item2=side_item2, 
                               drink=drink, 
                               total_price=current_total_price)
    else:
        return "Order not found or not authorized to reorder this."
    
@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    message = None

    if request.method == "POST":
        # Retrieve form data
        name = request.form.get("name")
        role = request.form.get("role")
        contact_info = request.form.get("contact_info")
        available_start = request.form.get("available_start")
        available_end = request.form.get("available_end")

        # Create an instance of the Employee class and add to the database
        new_employee = Employee(name=name, role=role, contact_info=contact_info, available_start=available_start, available_end=available_end)
        message = new_employee.add_employee(cnx, cursor)

        # After adding the employee, redirect to the employee list page
        return redirect("/employee_list")  # This will trigger the '/employee_list' route to show the updated list

    # Render the 'add_employee' form when it's a GET request
    return render_template("add_employee.html", message=message)


@app.route("/employee_list", methods=["GET"])
def show_employees():
    # Query to get the list of employees
    query = """
        SELECT employee_id, name, role, contact_info, available_start, available_end 
        FROM employees
    """
    cursor.execute(query)
    employees = cursor.fetchall()

    # Get the current time
    current_time = datetime.now().time()

    # Process employee availability
    employee_list = []
    for emp in employees:
        employee_id, name, role, contact_info, available_start, available_end = emp

        # Convert available_start and available_end to `time` objects if they are strings
        if isinstance(available_start, timedelta):
            available_start_time = (datetime.min + available_start).time()  # Convert timedelta to time
        else:
            available_start_time = available_start

        if isinstance(available_end, timedelta):
            available_end_time = (datetime.min + available_end).time()  # Convert timedelta to time
        else:
            available_end_time = available_end

        # Check if the current time falls within the employee's available hours
        is_available = available_start_time <= current_time <= available_end_time

        employee_list.append({
            "employee_id": employee_id,
            "name": name,
            "role": role,
            "contact_info": contact_info,
            "available_start": available_start_time,
            "available_end": available_end_time,
            "is_available": is_available
        })

    # Create an order detail example for notification
    order_details = {
        "pizza_type": "Pepperoni",
        "pizza_size": "Large",
        "total_price": 19.99
    }

    # Instantiate the Notify class and notify available employees
    notifier = Notify(employee_list)
    notifier.notify_available_employees(order_details)

    # Render the employee list template
    return render_template("employee_list.html", employees=employee_list)

# Route to view orders assigned to employees
@app.route("/admin/view_assigned_orders", methods=["GET"])
def view_assigned_orders():
    try:
        # Query for assigned orders
        query_assigned = """
        SELECT o.order_id, o.pizza_type, o.pizza_size, o.side_item1, o.side_item2, o.drink, o.total_price, e.name, o.order_date
        FROM orders o
        JOIN employees e ON o.employee_id = e.employee_id
        WHERE o.employee_id IS NOT NULL
        ORDER BY o.order_date DESC
        """

        cursor.execute(query_assigned)
        assigned_orders = cursor.fetchall()
        print(f"Assigned orders: {assigned_orders}")

        # Query for unassigned orders
        query_unassigned = """
        SELECT o.order_id, o.pizza_type, o.pizza_size, o.side_item1, o.side_item2, o.drink, o.total_price, o.order_date
        FROM orders o
        WHERE o.employee_id IS NULL
        ORDER BY o.order_date DESC
        """
        cursor.execute(query_unassigned)
        unassigned_orders = cursor.fetchall()

        # Check for results
        if not assigned_orders and not unassigned_orders:
            print("No assigned or unassigned orders found.")

    except Exception as e:
        print(f"Error fetching orders: {e}")

    # Render the template with both assigned and unassigned orders
    return render_template("view_assigned_orders.html", assigned_orders=assigned_orders, unassigned_orders=unassigned_orders)


# Route to view total cost by items in a specific month
@app.route("/admin/view_items_sold", methods=["GET", "POST"])
def view_total_items_sold():
    admin = Admin(admin_id=1, name="Admin")
    items_sold = None

    if request.method == "POST":
        year = int(request.form.get("year"))
        month = int(request.form.get("month"))

        # Get the total quantity of items sold for the specified month
        items_sold = admin.view_total_items_sold(cnx, cursor, year, month)

    return render_template("view_total_items_sold.html", items_sold=items_sold)

if __name__ == "__main__":
    app.run(debug=True)
