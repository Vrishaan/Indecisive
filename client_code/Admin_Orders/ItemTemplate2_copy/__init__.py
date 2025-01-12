from ._anvil_designer import ItemTemplate2_copyTemplate
from anvil import *
import anvil.server
import anvil.users
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate2_copy(ItemTemplate2_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.item['status'] = self.drop_down_1.selected_value
    self.item.update()
    pass

  def drop_down_1_show(self, **event_args):
    """This method is called when the DropDown is shown on the screen"""
    self.item['status']
    pass