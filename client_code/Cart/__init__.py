from ._anvil_designer import CartTemplate
from anvil import *
import anvil.users
import stripe.checkout
import anvil.server
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
        
        # Calculate subtotal
        self.subtotal = sum(item['product']['price'] * item['quantity'] for item in self.items)
        self.subtotal_label.text = f"Rs{self.subtotal:.02f}"
        
        # Calculate shipping
        if self.subtotal >= 3000:  # Free shipping for orders over Rs. 3000
            self.shipping_label.text = 'FREE'     
        else:  # Add Rs. 199 shipping
            self.shipping_label.text = "Rs 199.00"
            self.subtotal += 199
        
        # Update total
        self.total_label.text = f"Rs{self.subtotal:.02f}"

    def shop_button_click(self, **event_args):
        """This method is called when the Shop button is clicked."""
        get_open_form().shop_link_click()

    def checkout_button_click(self, **event_args):
        """This method is called when the Checkout button is clicked."""
        # Prepare the order
        self.order = [{'name': item['product']['name'], 'quantity': item['quantity'], 'size': item['size']} for item in self.items]
        try:
            # Perform the Stripe checkout
            charge = stripe.checkout.charge(
                amount=int(self.subtotal * 100),  # Amount in cents
                currency="INR",
                shipping_address=True,
                title="Indecisive Clothing Store",
                icon_url="_/theme/cupcake_logo.png"
            )
            
            # Log the charge response for debugging
            print(f"Stripe charge response: {charge}")
            
            # Validate the response and process the order
            if charge.get('result') == 'succeeded' and 'charge_id' in charge:
                # Save the order on the server
                anvil.server.call('add_order', charge['charge_id'], self.order)

                # Reduce stock in the "size" DataTable
                for item in self.order:
                    name = item['name']
                    size = item['size']
                    quantity = item['quantity']
                    
                    # Find the matching row in the "size" DataTable
                    row = app_tables.size.get(name=name, size=size)
                    if row:
                        # Reduce stock and update the DataTable
                        new_stock = max(0, row['stock'] - quantity)
                        row['stock'] = new_stock

                # Call server function to send the order confirmation email
                user = anvil.users.get_user()
                if user:
                    email = user['email']
                    anvil.server.call('send_order_confirmation_email', email, self.order, self.subtotal)

                # Show a success notification
                Notification("Your order has been received! A confirmation email has been sent.").show()

                # Clear the cart and navigate back
                get_open_form().cart_items = []
                get_open_form().cart_link_click()
        except Exception as e:
            # Log the error for debugging but do not show failure alerts
            print(f"Exception during checkout: {e}")