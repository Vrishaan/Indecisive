from ._anvil_designer import CartTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import stripe

class Cart(CartTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.order = []
        user = anvil.users.get_user()
        user_email = user['email']
        rows = app_tables.cart.search(email=user_email)
        # Check if rows exist
        if len(list(rows)) > 0:  # Convert to a list to count rows
          self.empty_cart_panel.visible = False
          self.column_panel_1.visible = True
          self.populate_items(user_email)
        else:  # No rows found, show empty cart panel
          self.empty_cart_panel.visible = True
          self.column_panel_1.visible = False

    def populate_items(self, email):
        """Fetch and populate cart items."""
        cart_rows = app_tables.cart.search(email=email)
        items = []

        for row in cart_rows:
            # Get the corresponding product details
            product = app_tables.products.get(name=row['name'])
            if product:
                items.append({
                    'name': row['name'],
                    'size': row['size'],
                    'quantity': row['quantity'],
                    'price': product['price'],
                    'img': product['img']
                })

        self.items = items
        self.repeating_panel_1.items = self.items

        # Calculate subtotal
        self.subtotal = sum(item['price'] * item['quantity'] for item in self.items)
        self.subtotal_label.text = f"Subtotal: Rs {self.subtotal:.02f}"

        # Calculate shipping
        if self.subtotal >= 3000:  # Free shipping for orders over Rs. 3000
            self.shipping_label.text = 'FREE'
            shipping_cost = 0
        else:
            self.shipping_label.text = "Rs 199.00"
            shipping_cost = 199

        # Update total
        self.total_label.text = f"Total: Rs {self.subtotal + shipping_cost:.02f}"

    def shop_button_click(self, **event_args):
        """This method is called when the Shop button is clicked."""
        get_open_form().shop_link_click()

    def checkout_button_click(self, **event_args):
        """This method is called when the Checkout button is clicked."""
        # Prepare the order
        self.order = [{'name': item['name'], 'quantity': item['quantity'], 'size': item['size']} for item in self.items]
        try:
            # Perform the Stripe checkout
            charge = stripe.checkout.charge(
                amount=int(self.subtotal * 100),  # Amount in cents
                currency="INR",
                shipping_address=True,
                title="Indecisive Clothing Store",
                icon_url="_/theme/Logo%20.png"
            )
            
            # Validate the response and process the order
            if charge.get('result') == 'succeeded' and 'charge_id' in charge:
                charge_id=charge
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
                    anvil.server.call('send_order_confirmation_email', email, self.order, self.subtotal, charge_id)

                # Show a success notification
                Notification("Your order has been received! A confirmation email has been sent.").show()

                # Clear the cart and navigate back
                user_email = anvil.users.get_user()['email']

               # Fetch all rows in the cart table for the logged-in user's email
                rows_to_delete = app_tables.cart.search(email=user_email)

               # Iterate over the rows and delete them
                for row in rows_to_delete:
                 row.delete()

               # Refresh the UI
                get_open_form().cart_link_click()
        except Exception:
            Notification("An error occurred during the checkout process. Please try again.").show()