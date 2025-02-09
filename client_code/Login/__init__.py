from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.users
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Home import Home
     
class Login(LoginTemplate):
  def __init__(self, **properties):
    self.init_components()
   

  def button_1_click(self, **event_args):
    anvil.users.login_with_form()
     
    user= anvil.users.get_user()
    if user['admin'] is True:
      open_form('Admin')
    else:
      open_form('Main')
    pass

    