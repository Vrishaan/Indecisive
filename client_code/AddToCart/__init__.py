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
from ..Chart import Chart

class AddToCart(AddToCartTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Ensure drop_down_1 (quantity) is blank when the form is first initialized
        self.drop_down_1.selected_value = None

    def form_show(self, **event_args):
        # Ensure drop_down_1 (quantity) is blank when the form is shown
        self.drop_down_1.selected_value = None

    # Add to Cart Form: Updating the add_button_click method
    def add_button_click(self, **event_args):
        if self.drop_down_2.selected_value is not None and self.drop_down_1.selected_value is not None:
            # Get the selected size and quantity
            size = self.drop_down_2.selected_value
            quantity = self.drop_down_1.selected_value
            # Add the item to the cart, passing the updated self.item, size, and quantity
            get_open_form().add_to_cart(self.item, quantity, size)
            # Hide add_button and show added_button
            self.add_button.visible = False
            self.added_button.visible = True
            self.timer_1.interval = 2
            # Reset the drop-downs
            self.drop_down_1.selected_value = None
            self.drop_down_2.selected_value = None
            self.label_4.text = "Select Size and Quantity"
            alert(f"{quantity} x {self.item['name']}({size}) added to cart.")
        else:
            alert("Please select both size and quantity before adding to cart.")
    def timer_1_tick(self, **event_args):
      self.add_button.visible = True
      self.added_button.visible = False
    def drop_down_1_show(self, **event_args):
        name = self.item['name']  # Get the name from the item
        size = self.drop_down_2.selected_value  # Get the selected size from drop-down 2
        
        # Query the table to find a row where both 'name' and 'size' match
        row = app_tables.size.get(name=name, size=size)
        
        if row:
            stock = row['stock']  # Access the 'stock' field in the row
            if isinstance(stock, int) and stock > 0:
                # Generate options from 1 to stock
                options = list(range(1, stock + 1))
                self.drop_down_1.items = [(str(option), option) for option in options]
                # Reset the selected value to None (blank) after updating items
                self.drop_down_1.selected_value = None
                # Update label with remaining stock
                self.label_4.text = f"{stock} Remaining in Stock"
            else:
                # No stock available: Set items to a list with only a blank option
                self.drop_down_1.items = []
                # Ensure selected value is None (blank)
                self.drop_down_1.selected_value = None
                # Update label to indicate no stock available
                self.label_4.text = "No stock available"
        else:
            # No size found: Set items to a list with only a blank option
            self.drop_down_1.items = []
            # Ensure selected value is None (blank)
            self.drop_down_1.selected_value = None
            # Update label to indicate no stock found
            self.label_4.text = "No stock found"

    def drop_down_2_change(self, **event_args):
        # Reset the quantity dropdown when size changes
        self.drop_down_1.selected_value = None  # Explicitly reset to None (blank)
        self.drop_down_1_show()  # Update the available quantity based on the selected size

    def primary_color_1_click(self, **event_args):
        """This method is called when the button is clicked."""
        # Open the Chart form modally
        alert(content=Chart(), large=True, buttons=[])
