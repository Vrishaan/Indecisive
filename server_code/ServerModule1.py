import anvil.users
import anvil.stripe
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import stripe
import anvil.email

@anvil.server.callable
def add_message(name, email, message):
  app_tables.contact.add_row(name=name, email=email, message=message, date=datetime.now())
  anvil.email.send(from_name="Contact Form", 
                   subject="New Web Contact",
                   text=f"New web contact from {name} ({email})\nMessage: {message}")
  
@anvil.server.callable
def add_subscriber(email):
  app_tables.subscribers.add_row(email=email)
  
@anvil.server.callable
def add_order(charge_id, cart_items):
  app_tables.orders.add_row(charge_id=charge_id, order=cart_items)
