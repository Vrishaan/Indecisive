from ._anvil_designer import EditTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables

class Edit(EditTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Initially display the stock and bestseller status
        self.update_stock_display()
        self.update_bestseller_checkbox()
      
        # Initialize the selected_image attribute to None
        self.selected_image = None
        self.image_1.source = self.item['img']
    

    def file_loader_1_change(self, **event_args):
        """This method is triggered when the user selects a file to upload."""
        # Load the image data when the file is selected
        file = self.file_loader_1.file  # FileLoader component to fetch the uploaded file

        if file:
            # Set the image to the uploaded file for preview
            self.selected_image = file
            self.image_1.source = self.selected_image  # Update the Image component with the selected image

    def update_bestseller_checkbox(self):
        """Fetch and display the current bestseller status of the product."""
        product_name = self.item['name']  # Access the product's 'name'

        # Fetch the corresponding row for the product from the products table
        product_row = app_tables.products.get(name=product_name)

        # Set the checkbox value based on the current bestseller status
        if product_row:
            self.check_box_1.checked = product_row['best_seller']  # Assuming 'bestseller' is a boolean field in the 'products' table
        else:
            self.check_box_1.checked = False  # Default to unchecked if not found

    def add_button_click(self, **event_args):
        """This method is called when the button is clicked to update the stock and other details."""
        try:
            # Get the edited values from the textboxes
            edited_name = self.text_box_name.text
            
            # Clean and convert the price input (remove "Rs:" and convert to float)
            price_text = self.text_box_price.text
            if price_text.startswith("Rs:"):
                edited_price = float(price_text.replace("Rs:", "").strip())  # Remove "Rs:" and any leading spaces
            else:
                raise ValueError("Invalid price format. Please enter price as 'Rs: <amount>'.")

            edited_description = self.text_box_description.text

            # Initialize quantities as None by default
            small_quantity = None
            medium_quantity = None
            large_quantity = None

            # Check if quantity fields have valid inputs and convert to integers if valid
            if self.quantity_box.text:
                small_quantity = int(self.quantity_box.text)  # Convert to int if valid input
                size_row = app_tables.size.get(name=self.item['name'],size='S')
                size_row['stock'] = small_quantity
                Notification(f"Quantity (S) updated to: {small_quantity}").show()
            if self.quantity_box_copy.text:
                medium_quantity = int(self.quantity_box_copy.text)  # Convert to int if valid input
                size_row = app_tables.size.get(name=self.item['name'],size='M')
                size_row['stock'] = medium_quantity
                Notification(f"Quantity (M) updated to: {medium_quantity}").show()
            if self.quantity_box_copy_2.text:
                large_quantity = int(self.quantity_box_copy_2.text)  # Convert to int if valid input
                size_row = app_tables.size.get(name=self.item['name'],size='L')
                size_row['stock'] = large_quantity
                Notification(f"Quantity (L) updated to: {large_quantity}").show()

            # Fetch the product row from the database
            product_name = self.item['name']  # Access the product's 'name'
            product_row = app_tables.products.get(name=product_name)

            # Only update product details (name, price, description, bestseller) if they are changed
            if product_row:
                if product_row['name'] != edited_name:
                    product_row['name'] = edited_name
                    Notification(f"Product name updated to {edited_name}").show()

                if product_row['price'] != edited_price:
                    product_row['price'] = edited_price
                    Notification(f"Product price updated to Rs: {edited_price}").show()

                if product_row['description'] != edited_description:
                    product_row['description'] = edited_description
                    Notification("Product description updated.").show()

                # Update the bestseller status
                bestseller_status = self.check_box_1.checked  # Get the value of the checkbox
                if product_row['best_seller'] != bestseller_status:
                    product_row['best_seller'] = bestseller_status
                    Notification(f"Product best seller status updated to: {bestseller_status}").show()
                  
                # Check if a new image was selected and update the product's image
                if self.selected_image:
                    product_row['img'] = self.selected_image  # Update the image field in the database
                    Notification("Product image updated.").show()
                self.add_button.visible = False
                self.added_button.visible = True
                self.timer_1.interval = 2
            # Update the stock display after the update
            self.update_stock_display()

        except ValueError as e:
            # Show the specific error message
            Notification(str(e)).show()

        # Clear the quantity input boxes after update
        self.quantity_box.text = ""
        self.quantity_box_copy.text = ""
        self.quantity_box_copy_2.text = ""
        open_form('Admin')

    def update_stock_display(self):
        """Fetch and display the current stock for S, M, L sizes."""
        product_name = self.item['name']  # Access the product's 'name'

        # Fetch the current stock values for sizes S, M, and L
        small_row = app_tables.size.get(name=product_name, size="S")
        medium_row = app_tables.size.get(name=product_name, size="M")
        large_row = app_tables.size.get(name=product_name, size="L")

        # Display the stock values
        if small_row:
            self.stock_label.text = f"S: {small_row['stock']} Remaining in Stock"
        else:
            self.stock_label.text = "S: Not found in the database"

        if medium_row:
            self.stock_label_copy.text = f"M: {medium_row['stock']} Remaining in Stock"
        else:
            self.stock_label_copy.text = "M: Not found in the database"

        if large_row:
            self.stock_label_copy_2.text = f"L: {large_row['stock']} Remaining in Stock"
        else:
            self.stock_label_copy_2.text = "L: Not found in the database"

    def delete_click(self, **event_args):
        """This method is called when the delete button is clicked to delete the product."""
        if confirm(f"Are you sure you want to delete {self.item['name']} from the database?"):
            product_name = self.item['name']  # Access the product's 'name'

            # Fetch the corresponding rows from the 'size' table based on product name and size
            size_row_1 = app_tables.size.get(name=product_name, size='S')
            size_row_2 = app_tables.size.get(name=product_name, size='M')
            size_row_3 = app_tables.size.get(name=product_name, size='L')
            product_row = app_tables.products.get(name=product_name)

            if size_row_1 and size_row_2 and size_row_3 and product_row:
                size_row_1.delete()  # Delete the entry in the 'size' table
                size_row_2.delete()
                size_row_3.delete()
                product_row.delete()
                Notification(f"Product {product_name} has been deleted.").show()
                open_form('Admin')
            else:
                Notification("Could not delete, please try again").show()

    def timer_1_tick(self, **event_args):
      """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
      self.add_button.visible = True
      self.added_button.visible = False
      pass
