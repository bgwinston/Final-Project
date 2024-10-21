class Notify:
    def __init__(self, employees):
        self.employees = employees  # List of employee objects or dictionaries

    def notify_available_employees(self, order_details):
        # Find available employees
        available_employees = [emp for emp in self.employees if emp["is_available"]]
        
        # Notify each available employee about the new order
        for employee in available_employees:
            self.send_notification(employee, order_details)

    def send_notification(self, employee, order_details):
        # You can implement actual notification logic here (e.g., send an email, SMS, or log to console)
        # For now, we'll just print the notification to simulate the process
        print(f"Notify {employee['name']} ({employee['role']}) of new order:")
        print(f"Order details: {order_details}")