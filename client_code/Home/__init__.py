from ._anvil_designer import HomeTemplate
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

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Fetch best-sellers from the database
    best_sellers = app_tables.products.search(best_seller=True)
    
    # Apply roles to the banner
    self.banner.role = ['spaced-title', 'left-right-padding']
    
    # Add best-sellers to the flow panel
    for p in best_sellers:
      self.flow_panel_1.add_component(Product(item=p), width='30%')
    
    # Optionally, handle the "show" event
    self.flow_panel_1.set_event_handler('show', self.flow_panel_1_show)

  def flow_panel_1_show(self, **event_args):
    """Handler for when flow_panel_1 is shown"""
    # Add any necessary logic here or leave it as a placeholder
    pass

  def shop_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().shop_link_click()
