from ._anvil_designer import ContactTemplate
from anvil import *
import anvil.users
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Contact(ContactTemplate):
  def send_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.name_box.text
    email = self.email_box.text
    message = self.message_box.text
    
    if name and email and message:
      anvil.server.call('add_message', name, email, message)
      self.name_box.text = ""
      self.email_box.text = ""
      self.message_box.text = ""
      alert("Thanks for getting in touch!")
    else:
      alert("Please fill out the entire form before sending your message")
      





