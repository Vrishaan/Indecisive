from ._anvil_designer import AddToCartTemplate
from anvil import *
import anvil.users
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class AddToCart(AddToCartTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


  def add_button_click(self, **event_args):
    get_open_form().add_to_cart(self.item, self.drop_down_1.selected_value)
    self.drop_down_1.selected_value = 1
    self.add_button.visible = False
    self.added_button.visible = True
    self.timer_1.interval = 1

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.add_button.visible = True
    self.added_button.visible = False
    self.timer_1.interval = 0

  def drop_down_1_show(self, **event_args):
        stock = self.item['stock']
        if isinstance(stock, int) and stock > 0:
            # Generate options from 1 to stock
            options = list(range(1, stock + 1))
            self.drop_down_1.items = [(str(option), option) for option in options]
        else:
            self.drop_down_1.items = [("No stock available", None)]
