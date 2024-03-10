

class PageController:
    def __init__(self, pages, controller):
        self.pages = pages
        self.controller = controller
        self.page_display_names = self.controller.page_display_names

    def show_page(self, page_name, header_label):
        '''Show a frame for the given page name and update header text'''
        page = self.pages[page_name]
        page.tkraise()
        # Use the display name from the mapping
        display_name = self.page_display_names.get(page_name, page_name)

        for key, value in dict(self.page_display_names).items():
            if value == page_name:
                display_name = key
        header_label.configure(text=display_name)

