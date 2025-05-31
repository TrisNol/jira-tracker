import ttkbootstrap as ttk
from pages.login import Login
from pages.dashboard import Dashboard


class MainApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Jira Tracker")
        self.geometry("800x600")

        # Container for pages
        self.container = ttk.Frame(self)
        self.container.pack(fill=ttk.constants.BOTH, expand=True)

        # Dictionary to hold pages
        self.pages = {}

        # Map page names to their class references
        self.page_registry = {"Login": Login, "Dashboard": Dashboard}

        # Shared instances of Jira
        self.jira_instance = None

        # Initialize pages
        self.show_page("Login")

    def show_page(self, page_name_or_class):
        # Remove current page if it exists
        for page in self.pages.values():
            page.pack_forget()

        # Convert page name to class if it's a string
        if isinstance(page_name_or_class, str):
            if page_name_or_class not in self.page_registry:
                raise ValueError(f"Unknown page name: {page_name_or_class}")
            page_class = self.page_registry[page_name_or_class]
        else:
            page_class = page_name_or_class

        # Create or show the requested page
        if page_class not in self.pages:
            self.pages[page_class] = page_class(self.container, self)
        page = self.pages[page_class]
        page.pack(fill=ttk.constants.BOTH, expand=True)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
