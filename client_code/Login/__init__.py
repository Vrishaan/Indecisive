from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.users
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Login(LoginTemplate):
  def __init__(self, **properties):
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    while not anvil.users.login_with_form():
      pass
    self.my_reminders = anvil.server.call('get_reminders')
  
    # Any code you write here will run when the form opens.
