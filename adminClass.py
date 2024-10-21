from datetime import datetime, timedelta

class Admin:
    def __init__(self, admin_id, name):
        self.admin_id = admin_id
        self.name = name

    # Method to view orders assigned to employees
    def view_assigned_orders(self, cnx, cursor):
        query = """
        SELECT o.order_id, o.pizza_type, o.pizza_size, o.side_item1, o.side_item2, o.drink, o.total_price, o.order_date, e.name AS employee_name
        FROM orders o
        JOIN employees e ON o.employee_id = e.employee_id
        ORDER BY o.order_date DESC;
    """
        cursor.execute(query)
        assigned_orders = cursor.fetchall()
        return assigned_orders

    # Method to view items sold from greatest to least within a given month
    def view_total_items_sold(self, cnx, cursor, year, month):
        start_date = datetime(year, month, 1)
        end_date = (start_date + timedelta(days=31)).replace(day=1)

        query = """
        SELECT 'Pizza Size' AS category, pizza_size AS item, COUNT(*) AS quantity_sold
        FROM orders
        WHERE order_date >= %s AND order_date < %s
        GROUP BY pizza_size
        UNION ALL
        SELECT 'Pizza Type', pizza_type, COUNT(*)
        FROM orders
        WHERE order_date >= %s AND order_date < %s
        GROUP BY pizza_type
        UNION ALL
        SELECT 'Side Item 1', side_item1, COUNT(*)
        FROM orders
        WHERE order_date >= %s AND order_date < %s
        GROUP BY side_item1
        UNION ALL
        SELECT 'Side Item 2', side_item2, COUNT(*)
        FROM orders
        WHERE order_date >= %s AND order_date < %s
        GROUP BY side_item2
        UNION ALL
        SELECT 'Drink', drink, COUNT(*)
        FROM orders
        WHERE order_date >= %s AND order_date < %s
        GROUP BY drink
        ORDER BY quantity_sold DESC
        """
        cursor.execute(query, (start_date, end_date, start_date, end_date, start_date, end_date, start_date, end_date, start_date, end_date))
        items_sold = cursor.fetchall()
        return items_sold