import ttkbootstrap as ttk

from pages.login import LoginPage


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

        # Shared instances of Jira
        self.jira_instance = None

        # Initialize pages
        self.show_page(LoginPage)

    def show_page(self, page_class):
        # Remove current page if it exists
        for page in self.pages.values():
            page.pack_forget()

        # Create or show the requested page
        if page_class not in self.pages:
            self.pages[page_class] = page_class(self.container, self)
        page = self.pages[page_class]
        page.pack(fill=ttk.constants.BOTH, expand=True)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
