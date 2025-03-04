from ._anvil_designer import ChartTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import stripe.checkout
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Chart(ChartTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.

    def primary_color_1_click(self, **event_args):
        """This method is called when the close button is clicked."""
        # Close the modal alert
        self.raise_event("x-close-alert")
