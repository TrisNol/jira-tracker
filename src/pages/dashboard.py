import ttkbootstrap as ttk
import requests

from atlassian import Jira
from PIL import Image, ImageTk
from io import BytesIO
from components.ticket_row import TicketRow


class DashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Access shared Jira instance
        jira: Jira = self.controller.jira_instance

        # Display user information
        user = jira.myself()

        # Create a frame for the top-right corner
        top_right_frame = ttk.Frame(self)
        top_right_frame.pack(
            side=ttk.constants.TOP, anchor=ttk.constants.E, pady=10, padx=10
        )

        # Should not happen but just to be safe
        if not jira:
            return

        # Fetch user information
        user_display_name = user["displayName"]
        avatar_url = user["avatarUrls"]["48x48"]

        # Display the user's display name
        ttk.Label(top_right_frame, text=user_display_name, bootstyle="success").pack(
            side=ttk.constants.LEFT, padx=5
        )

        # Fetch and display the avatar
        response = requests.get(avatar_url)
        avatar_image = Image.open(BytesIO(response.content))

        avatar_photo = ImageTk.PhotoImage(
            avatar_image.resize((48, 48))
        )  # Resize the image to 48x48
        avatar_label = ttk.Label(top_right_frame, image=avatar_photo)
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
