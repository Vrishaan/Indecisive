from ._anvil_designer import ContactTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.google.auth, anvil.google.drive
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class Contact(ContactTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    # Initialize the map
    self.map_1.center = GoogleMap.LatLng(19.00493908512311, 72.82994174280753)
    self.map_1.zoom = 15
    icon = GoogleMap.Icon(url="_/theme/maps-icon.png")
    self.marker = GoogleMap.Marker(animation=GoogleMap.Animation.DROP, 
                                    position=GoogleMap.LatLng(19.00493908512311, 72.82994174280753),
                                    icon=icon)
    self.map_1.add_component(self.marker)

    def marker_click(sender, **event_args):
      i = GoogleMap.InfoWindow(content=Label(text="Indecisive Clothing Store", 
                                             bold=True, 
                                             foreground="theme:Primary 700"))
      i.open(self.map_1, sender)

    self.marker.set_event_handler("click", marker_click)

    # Populate the dropdown with product names and "Other"
    products = app_tables.products.search()
    product_names = [p['name'] for p in products] + ["Other"]
    self.product_dropdown.items = product_names
    self.product_dropdown.selected_value = None  # Default to no selection

  def send_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Get logged-in user information
    user = anvil.users.get_user()
    if user:
      # Access user properties directly
      email = user['email'] 
      
      about = self.product_dropdown.selected_value
      message = self.message_box.text

      if about and message:
        # Add feedback to the Feedback database
        app_tables.feedback.add_row(
          email=email,
          about=about,
          message=message,
          date=datetime.now().date(),
          seen=False
        )

        # Clear form fields
        self.product_dropdown.selected_value = None
        self.message_box.text = ""
        alert("Thanks for your feedback!")
      else:
        alert("Please select a product (or 'Other') and provide your message before sending.")
    else:
      alert("You must be logged in to send feedback.")
