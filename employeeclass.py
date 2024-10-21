import mysql.connector 

from datetime import datetime

class Employee:
    def __init__(self, employee_id=None, name=None, role=None, contact_info=None, is_available=False, available_start=None, available_end=None):
        self.employee_id = employee_id
        self.name = name
        self.role = role
        self.contact_info= contact_info
        self.is_available = False #Default is False 
        self.available_start = available_start
        self.available_end = available_end

    def add_employee(self, cnx, cursor):
        try:
            query = """
                INSERT INTO employees (name, role, contact_info, available_start, available_end)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.name, self.role, self.contact_info, self.available_start, self.available_end))
            cnx.commit()
            return "Employee added successfully!"
        except mysql.connector.Error as err:
            return f"Error adding employee: {err}"

    def save_availability(self, cnx, cursor):
        try:
            query = """
                UPDATE employees
                SET is_available = %s
                WHERE employee_id = %s
            """
            cursor.execute(query, (self.is_available, self.employee_id))
            cnx.commit()
        except mysql.connector.Error as err:
            print(f"Error updating availability: {err}")

    def update_availability(self):
        """Dynamically check if the employee is available based on the current time."""
        current_time = datetime.now().time()

        # Convert string time to datetime.time objects for comparison
        start_time = datetime.strptime(self.available_start, "%H:%M").time()
        end_time = datetime.strptime(self.available_end, "%H:%M").time()

        # Determine if the employee is currently available
        if start_time <= current_time <= end_time:
            self.is_available = True
        else:
            self.is_available = False

  # This method is responsible for notifying the employee about a new order -output to console
    def notify_new_order(self, order_id, order_details):
        # Logic to notify the employee of a new order
        print(f"Notification for Employee {self.name} ({self.role}):")
        print(f"Order ID: {order_id}")
        print(f"Pizza Type: {order_details['pizza_type']}")
        print(f"Pizza Size: {order_details['pizza_size']}")
        print(f"Sides: {order_details['side_item1']}, {order_details['side_item2']}")
        print(f"Drink: {order_details['drink']}")
        print(f"Total Price: {order_details['total_price']}")

     # Method to assign an order to the employee
    def assign_order(self, order_id):
        print(f"Order ID {order_id} has been assigned to Employee {self.name} (ID: {self.employee_id})")
        #