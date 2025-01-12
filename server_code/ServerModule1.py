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
    app_tables.contact.add_row(
        name=name, 
        email=email, 
        message=message, 
        date=datetime.now().date(),  # Corrected date handling
        seen=False  # Explicitly set the boolean field
    )
    anvil.email.send(
        from_name="Contact Form", 
        subject="New Web Contact",
        text=f"New web contact from {name} ({email})\nMessage: {message}"
    )

  
@anvil.server.callable
def add_subscriber(email):
  app_tables.subscribers.add_row(email=email)
  
@anvil.server.callable
def add_order(charge_id, cart_items):
    # Get the logged-in user's email
    user = anvil.users.get_user()
    user_email = user['email'] 
    date = datetime.now().date()
    app_tables.orders.add_row(
      charge_id=charge_id,
      email=user_email,
      date=date,
      status="Approval pending"
    )
    for item in cart_items:
        # Extract details from each cart item
        name = item.get('name')  # Name of the product
        quantity = item.get('quantity')  # Quantity of the product
        size = item.get('size')  # Size of the product 

        # Add a new row to the "orders" DataTable
        app_tables.order_details.add_row(
            charge_id=charge_id,
            name=name,
            quantity=quantity,
            size=size
        )

# This is the server-side function to handle the database update
@anvil.server.callable
def add_product(name, description, price, stock, is_best_seller, image, small, medium, large):
    # Store the image in the "media" table and get the media URL
    image_media = anvil.BlobMedia(image.content_type, image.get_bytes())

    # Add a new product to the "products" table
    app_tables.products.add_row(
        name=name,
        description=description,
        price=price,
        best_seller=is_best_seller,
        img=image_media
    )
    app_tables.size.add_row(
      name=name,
      stock= small,
      size= 'S'
    )
    app_tables.size.add_row(
      name=name,
      stock= medium,
      size= 'M'
    )
    app_tables.size.add_row(
      name=name,
      stock= large,
      size= 'L'
    )

@anvil.server.callable
def send_order_confirmation_email(email, order, subtotal, charge_id):
    """Send an order confirmation email to the user."""
    subject = "Order Confirmation - Indecisive Clothing Store"
    body = f"Thank you for your order with Indecisive! We are pleased to confirm that your order has been successfully received.\n\nYou can view your order summary and track your order status by using your Order ID: {charge_id['charge_id']}\n\n"
    body += "Thank you for choosing Indecisive. We appreciate your business and look forward to serving you again.\n\nBest Regards,\nIndecisve Clothing Store."
    anvil.google.mail.send(to=email, subject=subject, text=body)