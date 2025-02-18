from ._anvil_designer import ShopTemplate
from anvil import *
import anvil.users
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Product import Product
class Shop(ShopTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.banner.role = ['spaced-title', 'left-right-padding']
    
    self.all_products = list(app_tables.products.search())
    
    self.display_products(self.all_products)

  def display_products(self, products):
   self.flow_panel_1.clear()
   for p in products:
     self.flow_panel_1.add_component(Product(item=p), width='30%')

  def search_box_pressed_enter(self, **event_args):
    """Called when the user presses Enter in the search box"""
    search_query = self.search_box.text.lower()  
    
    filtered_products = [
      p for p in self.all_products
      if search_query in p['name'].lower() or search_query in p['description'].lower()
    ]
    
    self.display_products(filtered_products)
    
    self.search_box.text = ""

  def shop_button_click(self, **event_args):
    self.display_products(self.all_products)
    pass
