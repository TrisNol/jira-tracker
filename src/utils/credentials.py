import os
import json
from pathlib import Path
from typing import Dict, Optional, Any


class CredentialManager:
    """
    A utility class to manage loading and saving credentials to AppData/Roaming
    """

    APP_NAME = "jira-tracker"

    def __init__(self):
        self.credentials_path = self._get_credentials_path()

    def _get_credentials_path(self) -> Path:
        """Get the path to the credentials file"""
        roaming_dir = os.path.join(os.environ.get("APPDATA", ""), self.APP_NAME)
        os.makedirs(roaming_dir, exist_ok=True)
        return Path(os.path.join(roaming_dir, "credentials.json"))

    def load_credentials(self) -> Optional[Dict[str, Any]]:
        """
        Load credentials from the JSON file if it exists

        Returns:
            Dictionary containing credentials or None if the file doesn't exist
        """
        try:
            if self.credentials_path.exists():
                with open(self.credentials_path, "r") as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return None

    def save_credentials(self, url: str, username: str, token: str) -> bool:
        """
        Save credentials to a JSON file in AppData/Roaming/jira-tracker

        Args:
            url: Jira server URL
            username: Username for Jira
            token: API token for Jira

        Returns:
            True if save was successful, False otherwise
        """
        try:
            credentials = {"url": url, "username": username, "token": token}

            with open(self.credentials_path, "w") as f:
                json.dump(credentials, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return False

    def delete_credentials(self) -> bool:
        """Delete the saved credentials file"""
        try:
            if self.credentials_path.exists():
                os.remove(self.credentials_path)
            return True
        except Exception as e:
            print(f"Error deleting credentials: {e}")
            return False
