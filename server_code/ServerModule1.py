import anvil.users
import anvil.stripe
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import anvil.email
import anvil.google.auth
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
    # Get the logged-in user's email
    user = anvil.users.get_user()
    user_email = user['email'] 

    for item in cart_items:
        # Extract details from each cart item
        name = item.get('name')  # Name of the product
        quantity = item.get('quantity')  # Quantity of the product
        size = item.get('size')  # Size of the product (ensure size is passed in cart_items)

        # Add a new row to the "orders" DataTable
        app_tables.orders.add_row(
            charge_id=charge_id,
            email=user_email,
            name=name,
            quantity=quantity,
            size=size
        )

# This is the server-side function to handle the database update
@anvil.server.callable
def add_product(name, description, price, stock, is_best_seller, image):
    # Store the image in the "media" table and get the media URL
    image_media = anvil.BlobMedia(image.content_type, image.get_bytes())

    # Add a new product to the "products" table
    app_tables.products.add_row(
        name=name,
        description=description,
        price=price,
        stock=stock,
        best_seller=is_best_seller,
        img=image_media
    )

@anvil.server.callable
def send_order_confirmation_email(email, order, subtotal):
    """Send an order confirmation email to the user."""
    subject = "Order Confirmation - Indecisive Clothing Store"
    body = "Thank you for your purchase!\n\nHere is your order summary:\n\n"
    for item in order:
        body += f" {item['quantity']} x {item['name']} (Size: {item['size']})\n"
    body += f"\nTotal Amount Paid: Rs {subtotal:.02f}\n\nThank you!"
    anvil.google.mail.send(to=email, subject=subject, text=body)