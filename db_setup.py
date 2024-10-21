from dbConnection import cnx, cursor

def create_users_table(cnx, cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    );
    """
    try:
        cursor.execute(create_table_query)
        cnx.commit()  # Commit the changes to the database
        print("Users table created successfully!")
    except Exception as e:
        print(f"An error occurred while creating the users table: {e}")

def create_pizza_orders_table(cnx, cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        employee_id INT,
        pizza_type VARCHAR(100) NOT NULL,
        pizza_size VARCHAR(50) NOT NULL,
        side_item1 VARCHAR(50),
        side_item2 VARCHAR(50),
        drink VARCHAR(50),
        total_price DECIMAL(10, 2) NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (name) REFERENCES employees(name) ON DELETE SET NULL
    );
    """
    try:
        cursor.execute(create_table_query)
        cnx.commit()  # Commit the changes to the database
        print("Pizza orders table created successfully!")
    except Exception as e:
        print(f"An error occurred while creating the pizza orders table: {e}")

def create_employee_table(cnx, cursor):
    create_table_query ="""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        role VARCHAR(50) NOT NULL,
        contact_info VARCHAR(100),
        is_available BOOLEAN DEFAULT TRUE,
        available_start TIME,
        available_end TIME
    );
    """
    try:
        cursor.execute(create_table_query)
        cnx.commit()  # Commit the changes to the database
        print("Employees table created successfully!")
    except Exception as e:
        print(f"An error occurred while creating the employees table: {e}")

if __name__ == "__main__":
    create_users_table(cnx, cursor)
    create_employee_table(cnx, cursor)  # Make sure to create employees table first
    create_pizza_orders_table(cnx, cursor)
