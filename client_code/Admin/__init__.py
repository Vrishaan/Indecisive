from ._anvil_designer import AdminTemplate
from anvil import *
import anvil.server
import anvil.users
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Product import Product

class Admin(AdminTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    
    products = app_tables.products.search()
    for p in products:
      self.flow_panel_1.add_component(Product(item=p), width='30%')

  def flow_panel_1_show(self, **event_args):
    """This method is called when the FlowPanel is shown on the screen"""
    pass
