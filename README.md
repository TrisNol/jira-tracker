# jira-tracker
A desktop app to conveniently track time spent on Jira tickets

## Features

- Connect to Jira using your personal API token
- View tickets assigned to you
- Track time spent on different work packages
- Save and load your credentials securely

## Credential Storage

The app can store your Jira credentials securely in your AppData/Roaming folder:
- Credentials are stored in `%APPDATA%\jira-tracker\credentials.json`
- You can save credentials by checking the "Save credentials" box during login
- Load saved credentials using the "Load Saved Credentials" button
- Delete saved credentials from the dashboard using the "Delete Saved Credentials" button
- When logging out, you'll be asked if you want to clear saved credentials before the app closes

## Building the app

```
poetry run pyinstaller --onefile --noconsole .\src\main.py --name JiraTracker --manifest manifest.xml --version-file version.info
```
