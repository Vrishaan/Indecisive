from ._anvil_designer import AdminTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..AdminHome import AdminHome
from ..Admin_Orders import Admin_Orders
from ..Feedback import Feedback

class Admin(AdminTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Initialize navigation to AdminHome
        self.navigate(self.link_2, AdminHome())

        for link in [self.link_2, self.link_4, self.link_1]:
            link.role = ['spaced-title', 'display-none-responsive']

    def navigate(self, active_link, form):
        """
        Handles navigation within the Admin page.
        Updates the active link's color and displays the selected form.
        """
        # Reset all links to default color
        for link in [self.link_2, self.link_4, self.link_1]:
            link.foreground = 'theme:Primary 700'

        # Highlight the active link
        active_link.foreground = 'theme:Secondary 500'

        # Clear the panel and display the selected form
        self.column_panel_1.clear()
        self.column_panel_1.add_component(form, full_width_row=True)

    def link_2_click(self, **event_args):
        """Navigate to the Admin Home page."""
        self.navigate(self.link_2, AdminHome())

    def link_4_click(self, **event_args):
        """Navigate to the Admin Orders page."""
        self.navigate(self.link_4, Admin_Orders())

    def link_1_click(self, **event_args):
        """Navigate to the Feedback page."""
        self.navigate(self.link_1, Feedback())