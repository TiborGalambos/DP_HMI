import time

import customtkinter as ctk

from PageController import PageController
from SubPage5 import SubPage5
from SubPage4 import SubPage4
from SubPage3 import SubPage3
from SubPage2 import SubPage2
from SubPage1 import SubPage1
from MainPage import MainPage

fullscreen_mode = False


class AppMainLayout(ctk.CTk, PageController):

    def __init__(self):
        super().__init__()

        self.page_display_names = {
            "Výber aplikácie": "MainPage",
            "Výber trasy": "SubPage1",
            "Poloha vlaku": "SubPage2",
            "Textové spravy": "SubPage3",
            "Diagnostika": "SubPage4",
            "Nastavenia": "SubPage5",
        }

        self.title('HMI')

        self.fullscreen()

        self.grid_rowconfigure(0, weight=0)  # Header row should not expand
        self.grid_rowconfigure(1, weight=1)  # Content row should expand
        # self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.pages_container()

        self.navigation_bar_container()

    def fullscreen(self):
        if (fullscreen_mode):
            self.attributes("-fullscreen", True)
        else:
            self.geometry('1300x900')

    def navigation_bar_container(self):
        # Navigation bar
        self.nav_bar = ctk.CTkFrame(self)
        self.create_nav_bar()
        self.nav_bar.grid_rowconfigure(0, weight=0)
        self.nav_bar.grid_columnconfigure(index=0, weight=1)
        self.nav_bar.grid(row=2, column=0, sticky='s')
        self.page_controller = PageController(self.pages, controller=self)
        self.page_controller.show_page("MainPage", self.header_label)

    def pages_container(self):
        # Container for all pages
        self.pages_container = ctk.CTkFrame(self, width=300, height=300)
        self.pages_container.grid(row=0, column=0, sticky='nsew')

        # Pages
        self.pages = {}
        i = 0
        for F in (MainPage, SubPage1, SubPage2, SubPage3, SubPage4, SubPage5):
            page_name = F.__name__
            page = F(master=self.pages_container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.header_container()

        # Container for all pages
        self.pages_container.grid(row=1, column=0, sticky='nsew')

    def header_container(self):
        # Header frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky='ew')  # place at the top

        # Set fixed sizes for columns 0 and 2, and make column 1 expandable
        fixed_size = 300  # Adjust this value as needed for your layout
        self.header_frame.grid_columnconfigure(0, minsize=fixed_size)  # Fixed size for column 0
        self.header_frame.grid_columnconfigure(1, weight=1)  # Column 1 expands
        self.header_frame.grid_columnconfigure(2, minsize=fixed_size)  # Fixed size for column 2

        # Left label with dummy text
        self.dummy_label = ctk.CTkLabel(self.header_frame, text="Trasa 0000", padx=10)
        self.dummy_label.grid(row=0, column=0, sticky='w')

        # Center label for page name
        self.header_label = ctk.CTkLabel(self.header_frame, text="", font=('Arial', 26, 'bold'))
        self.header_label.grid(row=0, column=1, sticky='news')

        # Right label for date and time
        self.datetime_label = ctk.CTkLabel(self.header_frame, text="", padx=10)
        self.datetime_label.grid(row=0, column=2, sticky='e')
        self.update_datetime()

    def update_datetime(self):
        '''Update the date and time display'''
        current_time = time.strftime('%d.%m.%Y - %H:%M:%S')
        self.datetime_label.configure(text=current_time, font=('Arial', 16, 'bold'))
        # Schedule the `update_datetime` method to be called after 1000ms
        self.after(1000, self.update_datetime)

    def create_nav_bar(self):
        button_size = 100
        col_num = 0
        for text, page_name in self.page_display_names.items():
            button = ctk.CTkButton(self.nav_bar, text=text, command=lambda name=page_name: self.page_controller.show_page(name, self.header_label))
            button.configure(font=("Arial", 12), width=button_size, height=button_size)
            button.grid(row=0, column=col_num, padx=50, pady=50, sticky="ew")

            self.nav_bar.grid_columnconfigure(col_num, minsize=button_size)
            col_num += 1  # Increment counter for each button
