class OrderEstimation:
    def __init__(self, pizza_type, pizza_size, side_item1, side_item2, drink):
        self.pizza_type = pizza_type
        self.pizza_size = pizza_size
        self.side_item1 = side_item1
        self.side_item2 = side_item2
        self.drink = drink

    def calculate_estimation_time(self):
        # Define preparation times (in minutes)
        pizza_time = {
            "Pepperoni": 15,
            "Margherita": 10,
            "BBQ Chicken": 18
        }

        size_time = {
            "Small": 5,
            "Medium": 7,
            "Large": 10
        }

        side_time = {
            "Salad": 2,
            "Breadsticks": 5,
            "Wings": 7,
            "Garlic Bread": 3,
            "None": 0
        }

        drink_time = {
            "Soda": 1,
            "Water": 1,
            "None": 0
        }

        # Calculate total preparation time
        total_time = 0
        total_time += pizza_time.get(self.pizza_type, 10)  # Default 10 minutes if not found
        total_time += size_time.get(self.pizza_size, 5)    # Default 5 minutes for size
        total_time += side_time.get(self.side_item1, 0)    # Default 0 for no side
        total_time += side_time.get(self.side_item2, 0)    # Default 0 for no side
        total_time += drink_time.get(self.drink, 0)        # Default 0 for no drink

        return total_time
