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
    price_text = self.text_box_3.text
    stock_text = self.quantity_box.text
    small = self.quantity_box.text
    medium = self.quantity_box_copy.text
    large = self.quantity_box_copy_2.text

    # Check if any required field is empty
    if not name or not description or not price_text or not stock_text or not small or not medium or not large or not self.file_loader_1.file:
        alert("Please fill in all the fields.")
        return  # Stop the function if any field is empty

    # Convert price and stock values after ensuring they are not empty
    try:
        price = float(price_text)  # Convert price to float
        stock = int(stock_text)  # Convert stock to int
    except ValueError:
        alert("Please enter valid numbers for price and stock.")
        return

    is_best_seller = self.check_box_1.checked  # Checkbox value
    image = self.file_loader_1.file  # The image file uploaded by the user
    self.image_1.source = self.file_loader_1.file

    # Call the server function to add the product to the database
    anvil.server.call('add_product', name, description, price, stock, is_best_seller, image, small, medium, large)

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

  # Assuming `file_loader_1` is your FileLoader and `image_1` is the Image component

  def file_loader_1_change(self, file, **event_args):
    # Check if a file is uploaded
    if file:
        # Set the image_1 source to the uploaded file
        self.image_1.source = file
        # Optionally, you can add some extra behavior when the image is shown, like enabling or resizing components