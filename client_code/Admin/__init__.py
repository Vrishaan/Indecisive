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
from ..Admin_Products import Admin_Products

class Admin(AdminTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    
    products = app_tables.products.search()
    for p in products:
      self.flow_panel_1.add_component(Admin_Products(item=p), width='30%')

  def navigate(self, active_link, form):
    for i in [self.home_link, self.shop_link, self.about_link, self.contact_link, self.cart_link]:
      i.foreground = 'theme:Primary 700'
    active_link.foreground = 'theme:Secondary 500'
    self.column_panel_1.clear()
    self.column_panel_1.add_component(form, full_width_row=True)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('AddProduct')
    pass

