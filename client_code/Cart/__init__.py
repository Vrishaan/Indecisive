from ._anvil_designer import CartTemplate
from anvil import *
import anvil.users
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Cart(CartTemplate):
  def __init__(self, items, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.order = []
    self.items = items

    if not self.items:
      self.empty_cart_panel.visible = True
      self.column_panel_1.visible = False
    
    self.repeating_panel_1.items = self.items
    
    self.subtotal = sum(item['product']['price'] * item['quantity'] for item in self.items)
    self.subtotal_label.text = f"Rs{self.subtotal:.02f}"
    
    if self.subtotal >= 3000: #free shipping for orders over $35
      self.shipping_label.text = 'FREE'     
    else: #add $5 shipping
      self.shipping_label.text = "Rs 199.00"
      self.subtotal = self.subtotal + 199
      
    self.total_label.text = f"Rs{self.subtotal:.02f}"
      

  def shop_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().shop_link_click()

  def checkout_button_click(self, **event_args):
    """This method is called when the button is clicked"""  
    for i in self.items:
        self.order.append({'name': i['product']['name'], 'quantity': i['quantity']})
    try:
        # Perform the Stripe checkout
        charge = stripe.checkout.charge(
            amount=self.subtotal * 100,  # Amount in cents
            currency="INR",
            shipping_address=True,
            title="Indecisive Clothing Store",
            icon_url="_/theme/cupcake_logo.png"
        )
        
        # Log the Stripe charge response for debugging
        print(f"Stripe charge response: {charge}")
        
        # Validate the response
        if charge and 'charge_id' in charge:
            # Call server function to save the order
            anvil.server.call('add_order', charge['charge_id'], self.order)

            # Show success notification
            Notification("Your order has been received!").show()

            # Clear the cart and navigate back to cart page
            get_open_form().cart_items = []
            get_open_form().cart_link_click()
        else:
            # Unexpected response
            print(f"Unexpected charge response: {charge}")
            alert("Payment succeeded, but we couldn't process the order. Please contact support.")
    except Exception as e:
        # General exception handling for any errors
        print(f"Exception during checkout: {e}")
        alert("Payment failed. Please try again.")