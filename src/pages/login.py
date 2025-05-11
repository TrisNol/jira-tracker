import re
import ttkbootstrap as ttk

from ttkbootstrap.validation import ValidationEvent, validator, add_validation
from atlassian import Jira
from pages.dashboard import DashboardPage


@validator
def validate_server_url(event: ValidationEvent) -> bool:
    url = event.postchangetext
    url_regex = r"^(https?:\/\/)?([\w\-]+\.)+[\w\-]+(\/[\w\-]*)*\/?$"
    return re.match(url_regex, url) is not None


@validator
def validate_username(event: ValidationEvent) -> bool:
    username = event.postchangetext
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, username) is not None


class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Jira Server URL
        ttk.Label(self, text="Jira Server URL:", bootstyle="primary").pack(
            anchor=ttk.constants.W, padx=10, pady=(10, 0)
        )
        self.url_entry = ttk.Entry(self, width=40)
        self.url_entry.pack(fill=ttk.constants.X, padx=10, pady=5)
        add_validation(self.url_entry, validate_server_url)

        # Username
        ttk.Label(self, text="Username:", bootstyle="primary").pack(
            anchor=ttk.constants.W, padx=10, pady=(10, 0)
        )
        self.username_entry = ttk.Entry(self, width=40)
        self.username_entry.pack(fill=ttk.constants.X, padx=10, pady=5)
        add_validation(self.username_entry, validate_username)

        # Token
        ttk.Label(self, text="Token:", bootstyle="primary").pack(
            anchor=ttk.constants.W, padx=10, pady=(10, 0)
        )
        token_frame = ttk.Frame(self)
        token_frame.pack(fill=ttk.constants.X, padx=10, pady=5)

        self.token_entry = ttk.Entry(token_frame, width=34, show="*")
        self.token_entry.pack(
            side=ttk.constants.LEFT, fill=ttk.constants.X, expand=True
        )

        # Login Button
        login_button = ttk.Button(
            self, text="Login", bootstyle=ttk.constants.SUCCESS, command=self.login
        )
        login_button.pack(pady=10)

    def login(self):
        url = self.url_entry.get()
        username = self.username_entry.get()
        token = self.token_entry.get()

        try:
            # Create Jira and Confluence instances
            jira = Jira(url=url, username=username, password=token)

            # Test the connection
            user = jira.myself()
            print(user)

            # Store instances in the controller (MainApp)
            self.controller.jira_instance = jira

            # Navigate to the next page
            self.controller.show_page(DashboardPage)
        except Exception as e:
            print(f"Error: {e}")
