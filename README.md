# Jira Tracker
A lightweight desktop app for tracking time against Jira tickets and submitting
it as Jira worklogs.

## Why this repo exists

A workday rarely stays on one ticket. Coding, meetings, reviews, and testing can
split attention across several issues, making it difficult to reconstruct time
accurately at the end of the day. Logging each interval in Jira also means
repeatedly finding the issue and entering the same details.

Jira Tracker puts ticket selection, timers, and worklog submission in one desktop
window. It aims to reduce context switching, keep elapsed time visible while you
work, and record the type of activity alongside the time spent. It is a focused
time-entry tool, not a replacement for Jira's planning or reporting features.

## Features

- Connect to Jira Cloud using your account email and API token
- Select unresolved tickets assigned to you, or enter a ticket key manually
- Track time in five independent rows with play, pause, and reset controls
- Label work with Coding, Concept, Meeting, PR Review, or Testing
- Open a selected ticket in your browser
- Transfer tracked time to Jira as a worklog with the work package as its comment
- Optionally save and reload login details locally (see the security note below)

## Getting started

### Prerequisites

- Python 3.12 or 3.13 (the supported range is `>=3.12,<3.14`)
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- Git to clone the repository
- A graphical desktop session and Python's Tkinter support
- Access to a Jira Cloud site, an
	[Atlassian API token](https://id.atlassian.com/manage-profile/security/api-tokens),
	and permission to browse issues and log work on the relevant tickets

The issue search uses Jira Cloud's REST API v3. Jira Server and Data Center
compatibility is not currently established. Jira time tracking must be enabled
for worklog submission.

On Linux, Tkinter may need a separate OS package, such as `python3-tk` on
Debian/Ubuntu. Install the package matching your Python interpreter. Verify it
with `python -m tkinter`; a small test window should open. A headless terminal
alone cannot display the app.

### Install

Run these commands in a terminal:

```bash
git clone https://github.com/TrisNol/jira-tracker.git
cd jira-tracker
poetry env use python3.12
poetry install
```

Use `python3.13` instead if that is your installed supported version. On Windows,
you can pass the full path to a Python 3.12 or 3.13 executable to
`poetry env use`. The repository configures Poetry to create its virtual
environment in `.venv`; no manual activation is needed for `poetry run` commands.

### Run

From the repository root:

```bash
poetry run python src/main.py
```

The login window opens first. Enter:

- **Jira Server URL:** your site root, for example `https://your-team.atlassian.net`
	(not an issue URL or a REST API path)
- **Username:** your Atlassian account email address
- **Token:** your API token, not your account password

Leave **Save credentials** unchecked unless you accept the storage behavior
described below, then click **Login**.

## Tracking and logging work

1. Select a ticket in a row. The dropdown contains unresolved issues assigned to
	 you; you can also type another ticket key, such as `TEAM-123`.
2. Select the work package for the activity. **Open** opens the ticket in your
	 default browser.
3. Click **Play** to start tracking and **Pause** when you stop or switch tasks.
	 Rows are independent: starting one does not pause another.
4. Pause the timer, check the ticket and work package, then click **Transfer**.
	 This creates a real Jira worklog using the tracked seconds and the selected
	 work package as the comment. A successful transfer resets that row's timer.
5. Use **Reset** only to discard time that you do not want to submit.

Timers and row selections are kept in memory only. Transfer time before closing
or logging out; unsubmitted time is not restored on the next launch. Although
the timer display is editable, manually entering a duration does not update the
tracked seconds used for transfer. Start the timer with **Play** before
transferring; manual time entry is not currently supported.

## Credential Storage

**Security note:** saved credentials include your API token in plain-text JSON.
They are not encrypted or stored in an OS credential vault. Only save them on a
trusted machine, protect access to the file, and never commit or share it.

- On Windows, the file is `%APPDATA%\jira-tracker\credentials.json`.
- If `APPDATA` is unset (typically on Linux/macOS), the file is
	`jira-tracker/credentials.json` relative to the directory from which you launch
	the app. It is not stored in a platform-specific user configuration directory.
- Check **Save credentials** during login to save the details after authentication.
- Use **Load Saved Credentials** on the login page to populate the fields, then
	click **Login** to connect.
- Use **Delete Saved Credentials** on the dashboard to remove the saved file.
- **Logout** asks whether to delete saved credentials before closing. Closing the
	window directly does not offer this deletion prompt.

## Building the app

Install the dependencies as above, then build from the repository root:

```bash
poetry run pyinstaller --onefile --name jira-tracker --paths src --hidden-import pages.login --hidden-import pages.dashboard src/main.py
```

The hidden imports include the pages loaded dynamically at runtime. PyInstaller
is already a project dependency; a separate global installation is unnecessary.
The build creates a `build/` directory, a `jira-tracker.spec` file, and the
executable in `dist/`.

Run the result on Linux/macOS:

```bash
./dist/jira-tracker
```

Or on Windows (PowerShell):

```powershell
.\dist\jira-tracker.exe
```

Build on the OS where you intend to run the executable; PyInstaller is not a
cross-compiler. The executable bundles Python dependencies, but still needs a
graphical session, network access, and Jira credentials. The default build keeps
a console available for diagnostics.

## Troubleshooting

- **Poetry rejects the Python version:** select Python 3.12 or 3.13 with
	`poetry env use`, then rerun `poetry install`.
- **Missing Tkinter or no display:** install Tkinter for the selected interpreter
	and run from a graphical desktop. Check with `poetry run python -m tkinter`.
- **Login or transfer fails:** check the site URL, email, token validity, issue
	access, and permission to log work. The terminal and error dialog provide
	details. Do not include tokens or saved credentials in bug reports.
- **A ticket is missing from the dropdown:** it only lists unresolved tickets
	assigned to the signed-in user and is loaded when the dashboard opens. Enter
	the key manually; large result sets may be incomplete because search pagination
	is not implemented.
- **The packaged app cannot find a page module:** rebuild with both hidden-import
	options shown above.

## Documentation site

The site uses Zensical. Its home page is copied from this README, so edit the
README first and synchronize it before previewing or building the site.

```bash
poetry install --with docs
sh scripts/copy_docs.sh
poetry run zensical serve
```

Open `http://localhost:3000` for the preview. Stop it with `Ctrl+C`. To generate
the static site in `site/` instead:

```bash
poetry run zensical build
```
