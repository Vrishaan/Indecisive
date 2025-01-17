from ._anvil_designer import AdminHomeTemplate
from anvil import *
import anvil.server
import anvil.users
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Admin_Products import Admin_Products
from ..AddProduct import AddProduct

class AdminHome(AdminHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Load all products from the database
    self.all_products = list(app_tables.products.search())
    
    # Initially display all products
    self.display_products(self.all_products)

  def display_products(self, products):
    """Populate the FlowPanel with products"""
    self.flow_panel_1.clear()  # Clear the FlowPanel
    
    if products:
      # Add each product as a component to the FlowPanel
      for p in products:
        self.flow_panel_1.add_component(Admin_Products(item=p), width='30%')
    else:
      # Display a message if no products match the search query
      self.flow_panel_1.add_component(
          Label(text="No products found.", align="center", role="headline")
      )

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(content=AddProduct(), large=True)
    pass

  def search_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in the search box"""
    search_query = self.search_box.text.lower()  # Get the search query in lowercase
    
    # Filter products by name or description
    filtered_products = [
      p for p in self.all_products
      if search_query in p['name'].lower() or search_query in p['description'].lower()
    ]
    
    # Display the filtered products or a no-match message
    self.display_products(filtered_products)
    
    # Clear the search box after taking input
    self.search_box.text = ""

  def shop_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.display_products(self.all_products)
    pass
