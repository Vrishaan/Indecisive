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
    if not name or not description or not price_text or not self.file_loader_1.file:
        alert("Please fill in all the fields.")
        return  # Stop the function if any field is empty

    # Convert price and stock values after ensuring they are not empty
    try:
        price = float(price_text)  # Convert price to float
        if stock_text:
          stock = int(stock_text)  # Convert stock to int
        else:
          stock = 0
    except ValueError:
        alert("Please enter valid numbers for price and stock.")
        return

    is_best_seller = self.check_box_1.checked  # Checkbox value
    image = self.file_loader_1.file  # The image file uploaded by the user
    self.image_1.source = self.file_loader_1.file

    # Call the server function to add the product to the database
    anvil.server.call('add_product', name, description, price, stock, is_best_seller, image, small, medium, large)
    self.add_button.visible = False
    self.added_button.visible = True
    self.timer_1.interval = 2

    # Optionally, clear the fields after submission
    self.text_box_1.text = ''
    self.text_box_2.text = ''
    self.text_box_3.text = ''
    self.quantity_box.text = ''
    self.quantity_box_copy.text = ''
    self.quantity_box_copy_2.text = ''
    self.check_box_1.checked = False
    self.file_loader_1.clear()

    # You can show a success message here
    alert("Product added successfully!")
    open_form('Admin')

  # Assuming `file_loader_1` is your FileLoader and `image_1` is the Image component

  def file_loader_1_change(self, file, **event_args):
    # Check if a file is uploaded
    if file:
        # Set the image_1 source to the uploaded file
        self.image_1.source = file

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.add_button.visible = True
    self.added_button.visible = False
    pass