from ._anvil_designer import MainTemplate
from anvil import *
import anvil.users
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Home import Home
from ..Shop import Shop
from ..Contact import Contact
from ..About import About
from ..Cart import Cart
from ..Order_Status import Order_Status

class Main(MainTemplate):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.navigate(self.home_link, Home())
    self.cart_items = []
    
    for link in [self.home_link_copy, self.shop_link_copy, self.about_link_copy, self.contact_link_copy, self.insta_link_copy, self.cart_link_copy, self.Order_Status_link_copy]:
      link.role = ['spaced-title', 'display-responsive']
    
    for link in [self.home_link, self.shop_link, self.about_link, self.contact_link, self.insta_link, self.cart_link, self.Order_Status_link]:
      link.role = ['spaced-title', 'display-none-responsive']
    
  def add_to_cart(self, product, quantity, size):
    #if item is already in cart, just update the quantity
    for i in self.cart_items:
      if i['product'] == product:
        i['quantity'] += quantity
        break
    else:
      self.cart_items.append({'product': product, 'quantity': quantity, 'size': size})
    
  def navigate(self, active_link, form):
    for i in [self.home_link, self.shop_link, self.about_link, self.contact_link, self.cart_link, self.Order_Status_link]:
      i.foreground = 'theme:Primary 700'
    active_link.foreground = 'theme:Secondary 500'
    self.column_panel_1.clear()
    self.column_panel_1.add_component(form, full_width_row=True)

  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.navigate(self.home_link, Home())


  def shop_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.navigate(self.shop_link, Shop())

  def about_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.navigate(self.about_link, About())
    
  def contact_link_click(self, **event_args):
    """This method is called when the Link is shown on the screen"""
    self.navigate (self.contact_link, Contact())

  def cart_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.navigate(self.cart_link, Cart(items=self.cart_items))

  def Order_Status_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.navigate(self.Order_Status_link, Order_Status())
    pass