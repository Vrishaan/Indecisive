from ._anvil_designer import Admin_ProductsTemplate
from anvil import *
import anvil.users
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Edit import Edit

class Admin_Products(Admin_ProductsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def add_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    save_clicked = alert(content=Edit(item=self.item), large=True)
