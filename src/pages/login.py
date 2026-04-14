import re
import ttkbootstrap as ttk

from ttkbootstrap.validation import ValidationEvent, validator, add_validation
from utils.credentials import CredentialManager
from utils.jira_client import JiraClient

# We'll use string references to avoid circular imports


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


class Login(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.credential_manager = CredentialManager()

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

        # Add toggle visibility button for token
        self.show_token_var = ttk.BooleanVar(value=False)
        self.show_token_btn = ttk.Button(
            token_frame, text="👁️", width=3, command=self.toggle_token_visibility
        )
        self.show_token_btn.pack(side=ttk.constants.RIGHT, padx=(5, 0))

        # Add "Save Credentials" checkbox
        credentials_frame = ttk.Frame(self)
        credentials_frame.pack(fill=ttk.constants.X, padx=10, pady=5)

        self.save_credentials_var = ttk.BooleanVar(value=False)
        save_credentials_cb = ttk.Checkbutton(
            credentials_frame,
            text="Save credentials",
            variable=self.save_credentials_var,
            bootstyle="round-toggle",
        )
        save_credentials_cb.pack(side=ttk.constants.LEFT)

        # Add "Load Credentials" button
        load_credentials_btn = ttk.Button(
            credentials_frame,
            text="Load Saved Credentials",
            command=self.load_credentials,
            bootstyle=ttk.constants.INFO,
        )
        load_credentials_btn.pack(side=ttk.constants.RIGHT)

        # Login Button
        login_button = ttk.Button(
            self, text="Login", bootstyle=ttk.constants.SUCCESS, command=self.login
        )
        login_button.pack(pady=10)

    def toggle_token_visibility(self):
        """Toggle the visibility of the token field"""
        if self.show_token_var.get():
            self.token_entry.configure(show="")
            self.show_token_var.set(False)
        else:
            self.token_entry.configure(show="*")
            self.show_token_var.set(True)

    def load_credentials(self):
        """Load credentials from storage when button is clicked"""
        if credentials := self.credential_manager.load_credentials():
            self.populate_credentials_fields(credentials)
            ttk.dialogs.Messagebox.show_info(
                title="Success", message="Credentials loaded successfully."
            )
        else:
            ttk.dialogs.Messagebox.show_error(
                title="Error", message="No saved credentials found."
            )

    def populate_credentials_fields(self, credentials):
        """Fill the form fields with the loaded credentials"""
        if credentials.get("url"):
            self.url_entry.delete(0, ttk.constants.END)
            self.url_entry.insert(0, credentials["url"])

        if credentials.get("username"):
            self.username_entry.delete(0, ttk.constants.END)
            self.username_entry.insert(0, credentials["username"])

        if credentials.get("token"):
            self.token_entry.delete(0, ttk.constants.END)
            self.token_entry.insert(0, credentials["token"])

    def login(self):
        url = self.url_entry.get()
        username = self.username_entry.get()
        token = self.token_entry.get()

        try:
            # Create wrapped Jira client
            jira = JiraClient(url=url, username=username, password=token)

            # Test the connection
            user = jira.myself()
            print(user)

            # Save credentials if checkbox is selected
            if self.save_credentials_var.get():
                success = self.credential_manager.save_credentials(url, username, token)
                if success:
                    print("Credentials saved successfully")
                else:
                    print("Failed to save credentials")

            # Store instances in the controller (MainApp)
            self.controller.jira_instance = jira

            # Navigate to the next page using string reference
            self.controller.show_page("Dashboard")
        except Exception as e:
            print(f"Error: {e}")
            ttk.dialogs.Messagebox.show_error(
                title="Login Failed", message=f"Could not connect to Jira: {e}"
            )
