from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.users
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate3(ItemTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # No additional initialization is required.

  def label_3_show(self, **event_args):
    """This method is called when the Label for 'name' is shown"""
    self.label_3.text = self.item['name']

  def label_4_show(self, **event_args):
    """This method is called when the Label for 'size' is shown"""
    self.label_4.text = self.item['size']

  def label_10_show(self, **event_args):
    """This method is called when the Label for 'quantity' is shown"""
    self.label_10.text = self.item['quantity']
