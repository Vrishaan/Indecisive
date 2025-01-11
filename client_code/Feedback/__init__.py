from ._anvil_designer import FeedbackTemplate
from anvil import *
import anvil.server
import anvil.users
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Feedback(FeedbackTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Fetch all feedback records from the "Feedback" table
        self.all_feedback = list(app_tables.feedback.search())  # Store all feedback in a list
        self.display_products(self.all_feedback)  # Initially display all feedback

    def load_feedback(self):
        """Fetches feedback data and displays it"""
        feedback_records = app_tables.feedback.search()  # Fetch all records from Feedback table
        self.repeating_panel_1.items = feedback_records  # Bind the records to a repeating panel

    def display_products(self, feedback_list):
        """
        Displays the given list of feedback records in the UI.
        Binds the feedback data to the repeating panel.
        """
        if feedback_list:
            self.repeating_panel_1.items = feedback_list  # Bind the data to the RepeatingPanel
        else:
            self.repeating_panel_1.items = []  # Clear the panel
            alert("No feedback records match your search.", title="No Matches Found")

    def search_box_pressed_enter(self, **event_args):
        """Called when the user presses Enter in the search box"""
        search_query = self.search_box.text.lower()  # Get the search query in lowercase

        # Filter feedback by 'email', 'about', or 'message' fields
        filtered_feedback = [
            feedback for feedback in self.all_feedback
            if search_query in feedback['email'].lower()
            or search_query in feedback['about'].lower()
            or search_query in feedback['message'].lower()
        ]

        # Display the filtered feedback or show a no-match message
        self.display_products(filtered_feedback)

        # Clear the search box after taking input
        self.search_box.text = ""

    def shop_button_click(self, **event_args):
        """Resets the feedback display to show all records"""
        self.display_products(self.all_feedback)
        self.drop_down_1.selected_value = "All"

    def drop_down_1_change(self, **event_args):
     """This method is called when an item is selected in the dropdown."""
    # Get the selected value from the dropdown
     selected_value = self.drop_down_1.selected_value

     if selected_value == "All":
        # Show all feedback
        filtered_feedback = self.all_feedback
     elif selected_value == "Unseen":
        # Show feedback with the checkbox unchecked (False)
        filtered_feedback = [feedback for feedback in self.all_feedback if not getattr(feedback, 'check_box_1', False)]
     elif selected_value == "Seen":
        # Show feedback with the checkbox checked (True)
        filtered_feedback = [feedback for feedback in self.all_feedback if getattr(feedback, 'check_box_1', False)]
     else:
        # If no valid option is selected, show no feedback
        filtered_feedback = []

    # Display the filtered feedback
     self.display_products(filtered_feedback)


