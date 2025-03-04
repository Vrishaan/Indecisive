from ._anvil_designer import Order_StatusTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import stripe.checkout
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Order_Status(Order_StatusTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.order_row = None  # Initialize order_row to None
        self.total_cost = 0  # Initialize total cost as 0

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        charge_id = self.text_box_1.text
        # Use get() to find the row in orders matching the charge_id
        self.order_row = app_tables.orders.get(charge_id=charge_id)
        if self.order_row:  # Check if an order row is found
            # Display the order status
            self.label_2.text = f"Status: {self.order_row['status']}"
            self.label_4.text = "Order Details:"           
            # Fetch related order details using the charge_id
            order_details = app_tables.order_details.search(charge_id=charge_id)            
            if order_details:
                # Prepare a list of product details (including quantity, size, etc.)
                products = []
                self.total_cost = 0  # Reset total cost before recalculating               
                for detail in order_details:
                    # Fetch product details from the products table based on the name in order_details
                    product = app_tables.products.get(name=detail['name'])
                    if product:
                        # Combine product details with the order detail (quantity, size, etc.)
                        product_info = {
                            'product': product,
                            'quantity': detail['quantity'],  # Get quantity from order_details
                            'size': detail['size'],  # Get size from order_details
                        }                   
                        # Calculate subtotal for this product
                        subtotal = product['price'] * detail['quantity']
                        self.total_cost += subtotal  # Add to total cost
                        # Add the product info to the products list
                        products.append(product_info)               
                # Bind the list of products to the repeating panel
                self.repeating_panel_1.items = products               
                # Update the total cost label
                self.label_3.text = f"Total Cost: Rs {self.total_cost:.02f}"
            else:
                alert("No order details found for this Order ID")
        else:
            alert("Please enter a valid Order ID")
