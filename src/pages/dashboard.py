import ttkbootstrap as ttk
import requests

from atlassian import Jira
from PIL import Image, ImageTk
from io import BytesIO
from components.ticket_row import TicketRow
from utils.credentials import CredentialManager

# We'll use string references to avoid circular imports


class Dashboard(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.credential_manager = CredentialManager()

        # Access shared Jira instance
        jira: Jira = self.controller.jira_instance

        # Create a frame for the top bar
        top_bar_frame = ttk.Frame(self)
        top_bar_frame.pack(
            side=ttk.constants.TOP, fill=ttk.constants.X, pady=10, padx=10
        )

        # Add logout button on the left
        logout_btn = ttk.Button(
            top_bar_frame, text="Logout", bootstyle="danger", command=self.logout
        )
        logout_btn.pack(side=ttk.constants.LEFT)

        # Add credential management buttons
        cred_frame = ttk.Frame(top_bar_frame)
        cred_frame.pack(side=ttk.constants.LEFT, padx=20)

        delete_creds_btn = ttk.Button(
            cred_frame,
            text="Delete Saved Credentials",
            bootstyle="danger-outline",
            command=self.delete_credentials,
        )
        delete_creds_btn.pack(side=ttk.constants.LEFT, padx=5)

        # Create a frame for the top-right corner (user info)
        user_frame = ttk.Frame(top_bar_frame)
        user_frame.pack(side=ttk.constants.RIGHT)

        # Should not happen but just to be safe
        if not jira:
            return

        # Display user information
        user = jira.myself()

        # Fetch user information
        user_display_name = user["displayName"]
        avatar_url = user["avatarUrls"]["48x48"]

        # Display the user's display name
        ttk.Label(user_frame, text=user_display_name, bootstyle="success").pack(
            side=ttk.constants.LEFT, padx=5
        )

        # Fetch and display the avatar
        response = requests.get(avatar_url)
        avatar_image = Image.open(BytesIO(response.content))

        avatar_photo = ImageTk.PhotoImage(
            avatar_image.resize((48, 48))
        )  # Resize the image to 48x48
        avatar_label = ttk.Label(user_frame, image=avatar_photo)
        avatar_label.image = (
            avatar_photo  # Keep a reference to avoid garbage collection
        )
        avatar_label.pack(side=ttk.constants.LEFT, padx=5)

        # Fetch a list of tickets assigned to the user
        issues = jira.jql("assignee = currentUser() AND resolution = Unresolved")[
            "issues"
        ]
        ticket_options = [issue["key"] for issue in issues]

        # Work package options - shared across all rows
        work_package_options = ["Coding", "Concept", "Meeting", "PR Review", "Testing"]

        # Create 5 rows
        for i in range(5):
            # Create a ticket row component
            TicketRow(
                parent=self,
                jira=jira,
                row_index=i,
                ticket_options=ticket_options,
                work_package_options=work_package_options,
            )

            # Add a separator after each row except the last one
            if i < 4:
                ttk.Separator(self, orient=ttk.constants.HORIZONTAL).pack(
                    fill=ttk.constants.X, pady=5
                )

    def logout(self):
        """Log out, clear credentials, and close the app"""
        # Clear Jira instance
        self.controller.jira_instance = None

        # Ask user if they want to clear saved credentials
        logout_option = ttk.dialogs.Messagebox.show_question(
            title="Logout Options",
            message="Would you like to clear your saved credentials before closing?",
            buttons=["Yes", "No", "Cancel"],
        )

        if logout_option == "Cancel":
            # User canceled the logout
            return
        elif logout_option == "Yes":
            # Clear saved credentials
            success = self.credential_manager.delete_credentials()
            if success:
                print("Credentials deleted successfully")
            else:
                print("Failed to delete credentials")

        # Exit the application if not cancelled
        if logout_option in ["Yes", "No"]:
            self.controller.quit()

    def delete_credentials(self):
        """Delete saved credentials"""
        # Show confirmation dialog
        confirm = ttk.dialogs.Messagebox.show_question(
            title="Confirm Delete",
            message="Are you sure you want to delete your saved credentials?",
        )

        if confirm == "Yes":
            success = self.credential_manager.delete_credentials()
            if success:
                ttk.dialogs.Messagebox.show_info(
                    title="Success", message="Credentials deleted successfully."
                )
            else:
                ttk.dialogs.Messagebox.show_error(
                    title="Error", message="Failed to delete credentials."
                )
