import mysql.connector

class CustomerOrder:
    def __init__(self, user_id):
        self.user_id = user_id  # The ID of the user placing the order
        self.pizza_type = None  # The type of pizza being ordered
        self.pizza_size = None  # The size of the pizza being ordered
        self.side_item1 = None  # First side item
        self.side_item2 = None  # Second side item
        self.drink = None  # Drink for the order
        self.total_price = 0.00  # Total price of the order

    # Method to add pizza details to the order
    def add_pizza(self, pizza_type, pizza_size, pizza_price):
        self.pizza_type = pizza_type
        self.pizza_size = pizza_size
        self.total_price += pizza_price
        print(f"Added {self.pizza_size} {self.pizza_type} Pizza to the order.")

    # Method to add side items to the order
    def add_side_items(self, side_item1, side_item2, side_item1_price=0, side_item2_price=0):
        self.side_item1 = side_item1
        self.side_item2 = side_item2
        self.total_price += side_item1_price + side_item2_price
        print(f"Added {self.side_item1} and {self.side_item2} to the order.")

    # Method to add a drink to the order
    def add_drink(self, drink, drink_price):
        self.drink = drink
        self.total_price += drink_price
        print(f"Added {self.drink} to the order.")

    # Method to place the order and save it to the database
    def place_order(self, cnx, cursor):
        try:
            # Insert the order into the orders table
            order_query = """
            INSERT INTO orders (user_id, pizza_type, pizza_size, side_item1, side_item2, drink, total_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(order_query, (
                self.user_id,
                self.pizza_type,
                self.pizza_size,
                self.side_item1,
                self.side_item2,
                self.drink,
                self.total_price
            ))
            cnx.commit()  
            print("Order placed successfully!")
        except mysql.connector.Error as err:
            print(f"Error placing order: {err}")

    # Method to display the order summary
    def display_order_summary(self):
        print("\nOrder Summary:")
        print(f"Pizza: {self.pizza_size} {self.pizza_type}")
        print(f"Sides: {self.side_item1}, {self.side_item2}")
        print(f"Drink: {self.drink}")
        print(f"Total Price: ${self.total_price:.2f}\n")
