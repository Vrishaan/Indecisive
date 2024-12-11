from ._anvil_designer import AddProductTemplate
from anvil import *
import anvil.users
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# This is the code for your form to call the server function when the button is clicked
class AddProduct(AddProductTemplate):
  def add_button_click(self, **event_args):
    # Get values from the form fields
    name = self.text_box_1.text
    description = self.text_box_2.text
    price = float(self.text_box_3.text)  # Convert price to float
    stock = int(self.quantity_box.text)  # Convert stock to int
    is_best_seller = self.check_box_1.checked  # Checkbox value

    image = self.file_loader_1.file  # The image file uploaded by the user
    self.image_1.source = self.file_loader_1.file
    
    # Call the server function to add the product to the database
    anvil.server.call('add_product', name, description, price, stock, is_best_seller, image)

    # Optionally, clear the fields after submission
    self.text_box_1.text = ''
    self.text_box_2.text = ''
    self.text_box_3.text = ''
    self.quantity_box.text = ''
    self.check_box_1.checked = False
    self.file_loader_1.clear()

    # You can show a success message here
    alert("Product added successfully!")
    open_form('Admin')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Admin')
    pass

  def image_1_show(self, **event_args):
    """This method is called when the Image is shown on the screen"""
    pass

