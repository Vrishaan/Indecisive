from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import stripe.checkout
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate1(ItemTemplate1Template):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      name= self.item['name']
      self.product=app_tables.products.get(name=name)

    def delete_button_click(self, **event_args):
     """Delete the item from the cart."""
     # Get the item details from `self.item` (this represents the current item in the repeating panel)
     product_name = self.item['name']
     product_size = self.item['size']
     user_email = anvil.users.get_user()['email']

     # Fetch the corresponding row from the cart table
     row_to_delete = app_tables.cart.get(name=product_name, size=product_size, email=user_email)
     # Delete the row
     row_to_delete.delete()
     # Refresh the repeating panel
     get_open_form().cart_link_click()


    def label_1_show(self, **event_args):
        """Show product name in label_1."""
        self.label_1.text = self.item['name']

    def label_2_show(self, **event_args):
       """Show product price in label_2"""
       self.label_2.text=f"Price: {self.product['price']}"
  

    def label_3_show(self, **event_args):
       """Show product name in label_3."""
       self.label_3.text = f"Size: {str(self.item['size'])}"

    def label_4_show(self, **event_args):
       """Show product quantity in label_4."""
       self.label_4.text = f"Quantity: {str(self.item['quantity'])}"

    def image_1_show(self, **event_args):
      """This method is called when the Image is shown on the screen"""
      self.image_1.source=self.product['img']
      pass

    def total_label_show(self, **event_args):
      """This method is called when the Label is shown on the screen"""
      self.total_label.text=f"Subtotal: Rs {self.item['quantity']*self.product['price']}"
      pass

