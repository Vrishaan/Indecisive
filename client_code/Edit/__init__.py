from ._anvil_designer import EditTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Edit(EditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Display the initial stock
    if hasattr(self, 'item'):
      product_row = app_tables.products.get(name=self.item["name"])
      if product_row:
        self.stock_label.text = f"{product_row['stock']} Remaining in Stock"

  def add_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.quantity_box.text:
      try:
        # Ensure the quantity is a valid integer
        quantity = int(self.quantity_box.text)
        
        # Update the "Stock" in the "Products" database
        product_row = app_tables.products.get(name=self.item["name"])
        if product_row:
          product_row["stock"] = quantity  # Increment stock by the specified quantity
          Notification(f"Updated stock for {self.item['name']} to {product_row['stock']}").show()
          # Refresh the stock label
          self.stock_label.text = f"{product_row['stock']} Remaining in Stock"
        else:
          Notification(f"Product {self.item['name']} not found in database.").show()
      except ValueError:
        Notification("Please enter a valid integer for quantity.").show()
      
      self.quantity_box.text = ""  # Clear the input box
    else:
      Notification("Please specify a quantity").show()
      
  def delete_click(self, **event_args):
    """This method is called when the delete button is clicked"""
    if confirm(f"Are you sure you want to delete {self.item['name']} from the database?"):
      product_row = app_tables.products.get(name=self.item["name"])
      if product_row:
        product_row.delete()
        Notification(f"Product {self.item['name']} has been deleted.").show()
        # Optionally, you can navigate to another form or refresh the current form
        open_form('Edit')
      else:
        Notification(f"Product {self.item['name']} not found in database.").show()

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.add_button.visible = True
    self.added_button.visible = False
    self.timer_1.interval = 0
