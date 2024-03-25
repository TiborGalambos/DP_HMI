
import GLOBAL_VARS
import customtkinter as ctk

from SubPage2 import SubPage2


class PageController:
    def __init__(self):
        
        self.header_label = None
        self.nav_bar = None
        self.page_display_names = None
        self.controller = None
        self.pages = None
        
    
    
    def setup(self, pages, controller):
        self.pages = pages
        self.controller = controller
        self.page_display_names = self.controller.page_display_names
        self.nav_bar = self.controller.nav_bar
        self.header_label = ctk.CTkLabel(master=controller)

    def set_header_label(self, header_label):
        self.header_label = header_label

    def show_page(self, page_name, header_label = None):
        '''Show a frame for the given page name and update header text'''
        page = self.pages[page_name]
        page.tkraise()
        # Use the display name from the mapping
        display_name = self.page_display_names.get(page_name, page_name)

        for key, value in dict(self.page_display_names).items():
            if value == page_name:
                display_name = key
                if value == "MainPage":
                    GLOBAL_VARS.home_page_active = True
                    self.controller.nav_bar.grid_forget()
                else:
                    GLOBAL_VARS.home_page_active = False
                    self.nav_bar.grid_rowconfigure(0, weight=0)
                    self.nav_bar.grid_columnconfigure(index=0, weight=1)
                    self.nav_bar.grid(row=2, column=0, sticky='s')


        if self.header_label is None:
            self.header_label = header_label

        self.header_label.configure(text=display_name)


