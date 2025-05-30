import ttkbootstrap as ttk
import webbrowser
from datetime import datetime, timezone


class TicketRow:
    def __init__(self, parent, jira, row_index, ticket_options, work_package_options):
        self.parent = parent
        self.jira = jira
        self.row_index = row_index
        self.ticket_options = ticket_options
        self.work_package_options = work_package_options

        # Timer state for this row
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_job = None
        self.timer_started = None

        # Create the UI components
        self.frame = self.create_row()

    def create_row(self):
        # Create a frame for the ticket row
        ticket_frame = ttk.Frame(self.parent)
        ticket_frame.pack(
            side=ttk.constants.TOP, fill=ttk.constants.X, pady=10, padx=10
        )

        # Label for ticket selection
        ttk.Label(
            ticket_frame, text=f"Ticket {self.row_index+1}:", bootstyle="info"
        ).pack(side=ttk.constants.LEFT, padx=5)

        # Combobox for ticket selection with editable entry
        self.ticket_var = ttk.StringVar()
        ticket_combobox = ttk.Combobox(
            ticket_frame, textvariable=self.ticket_var, values=self.ticket_options
        )
        ticket_combobox.pack(side=ttk.constants.LEFT, padx=5)

        # Button to open the selected ticket in a browser
        open_button = ttk.Button(
            ticket_frame, text="Open", command=self.open_ticket, bootstyle="link"
        )
        open_button.pack(side=ttk.constants.LEFT, padx=5)

        # Timer input field
        self.timer_var = ttk.StringVar(value="00:00:00")  # Default timer value
        timer_entry = ttk.Entry(
            ticket_frame,
            textvariable=self.timer_var,
            width=10,
            justify=ttk.constants.CENTER,
        )
        timer_entry.pack(side=ttk.constants.LEFT, padx=5)

        # Reset button
        reset_button = ttk.Button(
            ticket_frame, text="Reset", command=self.reset_timer, bootstyle="danger"
        )
        reset_button.pack(side=ttk.constants.LEFT, padx=5)

        # Play/Pause button
        self.play_pause_button = ttk.Button(
            ticket_frame, text="Play", command=self.toggle_timer, bootstyle="primary"
        )
        self.play_pause_button.pack(side=ttk.constants.LEFT, padx=5)

        # Work package selection
        self.work_package_var = ttk.StringVar(value="Coding")  # Default work package

        # Label for work package selection
        ttk.Label(ticket_frame, text="Work Package:", bootstyle="info").pack(
            side=ttk.constants.LEFT, padx=5
        )

        # Dropdown for work package selection
        work_package_combobox = ttk.Combobox(
            ticket_frame,
            textvariable=self.work_package_var,
            values=self.work_package_options,
        )
        work_package_combobox.pack(side=ttk.constants.LEFT, padx=5)

        # Transfer button
        transfer_button = ttk.Button(
            ticket_frame,
            text="Transfer",
            command=self.transfer_ticket,
            bootstyle="success",
        )
        transfer_button.pack(side=ttk.constants.LEFT, padx=5)

        return ticket_frame

    def open_ticket(self):
        if ticket_key := self.ticket_var.get():
            ticket_url = f"{self.jira.url}/browse/{ticket_key}"
            webbrowser.open(ticket_url)

    def update_timer(self):
        if self.timer_running:
            self.timer_seconds += 1
            hours, remainder = divmod(self.timer_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_var.set(f"{hours:02}:{minutes:02}:{seconds:02}")
            self.timer_job = self.parent.after(1000, self.update_timer)

    def toggle_timer(self):
        if self.timer_running:
            self.timer_running = False
            if self.timer_job is not None:
                self.parent.after_cancel(self.timer_job)
                self.timer_job = None
            self.play_pause_button.configure(text="Play")
        else:
            self.timer_running = True
            self.play_pause_button.configure(text="Pause")
            self.timer_started = datetime.now(timezone.utc)
            self.update_timer()

    def reset_timer(self):
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_started = None
        self.timer_var.set("00:00:00")
        self.play_pause_button.configure(text="Play")
        if self.timer_job is not None:
            self.parent.after_cancel(self.timer_job)
            self.timer_job = None

    def transfer_ticket(self):
        ticket_key = self.ticket_var.get()
        tracked_time = self.timer_var.get()
        selected_work_package = self.work_package_var.get()
        print(
            f"Row {self.row_index+1} - Ticket: {ticket_key}, Time Tracked: {tracked_time}, Work Package: {selected_work_package}"
        )

        if ticket_key:
            try:
                ticket = self.jira.issue(ticket_key)
                print(ticket)

                worklog_entry = {
                    "started": self.timer_started.strftime("%Y-%m-%dT%H:%M:%S.000%z"),
                    "timeSpentSeconds": self.timer_seconds,
                    "comment": selected_work_package,
                }
                print(worklog_entry)
                self.jira.issue_add_json_worklog(key=ticket_key, worklog=worklog_entry)
                self.reset_timer()
            except Exception as e:
                print(f"Error adding worklog: {e}")
