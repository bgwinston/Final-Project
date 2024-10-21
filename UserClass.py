import mysql.connector

class User:
    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email

    # Method to create a new user in the database
    def create_account(self, cnx, cursor):
        try:
            # Check if the username already exists
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (self.username,))
            if cursor.fetchone():
                return "Username already exists!"
            
            # Insert new user into the database
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (self.username, self.password, self.email))
            cnx.commit()
            return "Account created successfully!"
        
        except mysql.connector.Error as err:
            return f"Error creating account: {err}"

    # Method to log in a user
    def login(self, cnx, cursor):
        try:
            # Query to check if the username and password match
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (self.username, self.password))
            user = cursor.fetchone()

            if user:
                user_id = user[0]
                return "Login successful!",user_id
            else:
                return "Invalid username or password!", None
        
        except mysql.connector.Error as err:
            return f"Error logging in: {err}"
