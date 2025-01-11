from ._anvil_designer import Admin_OrdersTemplate
from anvil import *
import anvil.server
import anvil.users
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Admin_Orders(Admin_OrdersTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Fetch all order records from the "orders" table
        self.all_orders = list(app_tables.orders.search())  # Store all orders in a list
        self.display_products(self.all_orders)  # Initially display all orders

    def load_orders(self):
        """Fetches order data and displays it"""
        order_records = app_tables.orders.search()  # Fetch all records from orders table
        self.repeating_panel_1.items = order_records  # Bind the records to a repeating panel

    def display_products(self, order_list):
        """
        Displays the given list of order records in the UI.
        Binds the order data to the repeating panel.
        """
        if order_list:
            self.repeating_panel_1.items = order_list  # Bind the data to the RepeatingPanel
        else:
            self.repeating_panel_1.items = []  # Clear the panel
            alert("No order records match your search.", title="No Matches Found")

    def search_box_pressed_enter(self, **event_args):
        """Called when the user presses Enter in the search box"""
        search_query = self.search_box.text.lower()  # Get the search query in lowercase

        # Filter orders by 'email', 'name', 'charge_id', or 'size'
        filtered_orders = [
            order
            for order in self.all_orders
            if search_query in order["email"].lower()
            or search_query in order["name"].lower()
            or search_query in order["charge_id"].lower()
            or search_query in order["size"].lower()
        ]

        # Display the filtered orders or show a no-match message
        self.display_products(filtered_orders)

        # Clear the search box after taking input
        self.search_box.text = ""

    def shop_button_click(self, **event_args):
        """Resets the order display to show all records"""
        self.display_products(self.all_orders)
        self.drop_down_1.selected_value = "All"

    def drop_down_1_change(self, **event_args):
        """This method is called when an item is selected in the dropdown."""
        # Get the selected value from the dropdown
        selected_value = self.drop_down_1.selected_value

        if selected_value == "All":
            # Show all orders
            filtered_orders = self.all_orders
        elif selected_value == "Unseen":
            # Show orders where 'seen' is False (if 'seen' column exists in 'orders' table)
            filtered_orders = [
                order for order in self.all_orders if not order.get("seen", False)
            ]
        elif selected_value == "Seen":
            # Show orders where 'seen' is True (if 'seen' column exists in 'orders' table)
            filtered_orders = [
                order for order in self.all_orders if order.get("seen", False)
            ]
        else:
            # If no valid option is selected, show no orders
            filtered_orders = []

        # Display the filtered orders
        self.display_products(filtered_orders)
