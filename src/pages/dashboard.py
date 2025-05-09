import ttkbootstrap as ttk
import requests
import webbrowser

from ttkbootstrap.constants import *
from ttkbootstrap.icons import Icon

from atlassian import Jira
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime, timezone


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
        top_right_frame.pack(side=TOP, anchor=E, pady=10, padx=10)

        # Should not happen but just to be safe
        if not jira:
            return

        # Fetch user information
        user_display_name = jira.myself()["displayName"]
        avatar_url = jira.myself()["avatarUrls"]["48x48"]

        # Display the user's display name
        ttk.Label(top_right_frame, text=user_display_name, bootstyle="success").pack(
            side=LEFT, padx=5
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
        avatar_label.pack(side=LEFT, padx=5)

        # Fetch a list of tickets assigned to the user
        issues = jira.jql("assignee = currentUser() AND resolution = Unresolved")[
            "issues"
        ]
        ticket_options = [issue["key"] for issue in issues]

        # Create a frame for the ticket selection
        ticket_frame = ttk.Frame(self)
        ticket_frame.pack(side=TOP, fill=X, pady=10, padx=10)

        # Label for ticket selection
        ttk.Label(ticket_frame, text="Select or Enter Ticket:", bootstyle="info").pack(
            side=LEFT, padx=5
        )

        # Combobox for ticket selection with editable entry
        ticket_var = ttk.StringVar()
        ticket_combobox = ttk.Combobox(
            ticket_frame, textvariable=ticket_var, values=ticket_options
        )
        ticket_combobox.pack(side=LEFT, padx=5)

        # Button to open the selected ticket in a browser
        def open_ticket():
            ticket_key = ticket_var.get()
            if ticket_key:
                ticket_url = f"{jira.url}/browse/{ticket_key}"
                webbrowser.open(ticket_url)

        # Create a button with the text "Open" to open the ticket
        open_button = ttk.Button(
            ticket_frame, text="Open", command=open_ticket, bootstyle="link"
        )
        open_button.pack(side=LEFT, padx=5)

        # Timer input field and play/pause button
        timer_var = ttk.StringVar(value="00:00:00")  # Default timer value
        timer_entry = ttk.Entry(
            ticket_frame, textvariable=timer_var, width=10, justify=CENTER
        )
        timer_entry.pack(side=LEFT, padx=5)

        # Timer state
        timer_running = [
            False
        ]  # Use a mutable object to allow modification in nested functions
        timer_seconds = [0]  # Store elapsed seconds
        timer_job = [None]  # Store the after job ID
        timer_started = [None]  # Store the start time

        def update_timer():
            if timer_running[0]:
                timer_seconds[0] += 1
                hours, remainder = divmod(timer_seconds[0], 3600)
                minutes, seconds = divmod(remainder, 60)
                timer_var.set(f"{hours:02}:{minutes:02}:{seconds:02}")
                timer_job[0] = self.after(1000, update_timer)

        def toggle_timer():
            if timer_running[0]:
                timer_running[0] = False
                if timer_job[0] is not None:
                    self.after_cancel(timer_job[0])
                    timer_job[0] = None
                play_pause_button.configure(text="Play")
            else:
                timer_running[0] = True
                play_pause_button.configure(text="Pause")
                timer_started[0] = datetime.now(timezone.utc)
                update_timer()

        # def toggle_timer():
        #     timer_running[0] = not timer_running[0]
        #     if timer_running[0]:
        #         play_pause_button.configure(text="Pause")
        #         update_timer()
        #     else:
        #         play_pause_button.configure(text="Play")

        def reset_timer():
            timer_running[0] = False
            timer_seconds[0] = 0
            timer_started[0] = None
            timer_var.set("00:00:00")
            play_pause_button.configure(text="Play")

        # Reset button
        reset_button = ttk.Button(
            ticket_frame, text="Reset", command=reset_timer, bootstyle="danger"
        )
        reset_button.pack(side=LEFT, padx=5)

        # Play/Pause button
        play_pause_button = ttk.Button(
            ticket_frame, text="Play", command=toggle_timer, bootstyle="primary"
        )
        play_pause_button.pack(side=LEFT, padx=5)

        # Separator
        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, pady=10)

        # Transfer button
        def transfer_ticket():
            ticket_key = ticket_var.get()
            tracked_time = timer_var.get()
            print(f"Ticket: {ticket_key}, Time Tracked: {tracked_time}")

            ticket = jira.issue(ticket_key)
            print(ticket)

            worklog_entry = {
                'started': timer_started[0].strftime('%Y-%m-%dT%H:%M:%S.000%z'),
                'timeSpentSeconds': timer_seconds[0],
                'comment': 'Time tracked Hello',
            }
            print(worklog_entry)
            jira.issue_add_json_worklog(key=ticket_key, worklog=worklog_entry)

        transfer_button = ttk.Button(
            self, text="Transfer", command=transfer_ticket, bootstyle="success"
        )
        transfer_button.pack(side=TOP, pady=10)
