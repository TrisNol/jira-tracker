import ttkbootstrap as ttk
import importlib


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
        self.page_registry = {}

        # Shared instances of Jira
        self.jira_instance = None

        # Initialize pages
        # Load the LoginPage without importing it at the module level
        self.show_page("Login")

    def register_page(self, page_name, page_class):
        """Register a page class with its name"""
        self.page_registry[page_name] = page_class

    def get_page_class(self, page_name):
        """Get a page class by name, importing it if necessary"""
        if page_name not in self.page_registry:
            # Dynamically import the page class
            module = importlib.import_module(f"pages.{page_name.lower()}")
            page_class = getattr(module, page_name)
            self.page_registry[page_name] = page_class
        return self.page_registry[page_name]

    def show_page(self, page_name_or_class):
        # Remove current page if it exists
        for page in self.pages.values():
            page.pack_forget()

        # Convert page name to class if it's a string
        if isinstance(page_name_or_class, str):
            page_class = self.get_page_class(page_name_or_class)
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
