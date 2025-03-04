from ._anvil_designer import ProductTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import stripe.checkout
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..AddToCart import AddToCart

class Product(ProductTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Preload back image to eliminate lag
        self.front_image = self.item['img']
        self.back_image = self.item['img_2']

        # Add hidden Image component to preload back image
        self.hidden_image = Image(source=self.back_image, visible=False)
        self.add_component(self.hidden_image)

        # Set initial image
        self.image_1.source = self.front_image

    def add_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        save_clicked = alert(content=AddToCart(item=self.item), large=True)

    def image_1_mouse_enter(self, x, y, **event_args):
        """Show back image instantly when mouse hovers over the component"""
        self.image_1.source = self.back_image

    def image_1_mouse_leave(self, x, y, **event_args):
        """Revert to front image instantly when the mouse leaves"""
        self.image_1.source = self.front_image
