import time

import customtkinter as ctk
from screeninfo import get_monitors

from DatabaseManager import DatabaseManager
from PageController import PageController
from SubPage5 import SubPage5
from SubPage4 import SubPage4
from SubPage3 import SubPage3
from SubPage2 import SubPage2
from SubPage1 import SubPage1
from MainPage import MainPage
from PIL import Image
fullscreen_mode = False


class AppMainLayout(ctk.CTk, PageController):

    def __init__(self):
        super().__init__()

        self.page_controller = None
        self.icons = list()
        self.page_display_names = {
            "Výber aplikácie": "MainPage",
            "Výber trasy": "SubPage1",
            "Poloha vlaku": "SubPage2",
            "Textové spravy": "SubPage3",
            "Diagnostika": "SubPage4",
            "Nastavenia": "SubPage5",
        }

        self.title('HMI')


        self.grid_rowconfigure(0, weight=0)  # Header row should not expand
        self.grid_rowconfigure(1, weight=1)  # Content row should expand
        # self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.route_label = None
        self.header_frame = None


        self.pages_container()

        self.navigation_bar_container()

        self.db_manager = DatabaseManager()

        self.maximize_window()

        self.load_icons()



    def get_icons(self):
        return self.icons

    def maximize_window(self):
        self.update_idletasks()
        self.update()
        self.state('zoomed')

    def open_fullscreen_on_second_monitor(self):
        monitors = get_monitors()

        if len(monitors) > 1:
            second_monitor = monitors[0]  # Assuming the second monitor is the target
            self.geometry(f"{second_monitor.width}x{second_monitor.height}+{second_monitor.x}+{second_monitor.y}")
            # self.update_idletasks()  # Update the window state to ensure it has moved
            print(f"{second_monitor.width}x{second_monitor.height}")
            # self.attributes("-fullscreen", True)
        else:
            print("Only one monitor detected. Opening fullscreen on the primary monitor.")
            self.attributes("-fullscreen", True)



    def navigation_bar_container(self):
        # Navigation bar
        self.nav_bar = ctk.CTkFrame(self)
        self.create_nav_bar()
        self.nav_bar.grid_rowconfigure(0, weight=0)
        self.nav_bar.grid_columnconfigure(index=0, weight=1)
        self.nav_bar.grid(row=2, column=0, sticky='s')
        self.page_controller = PageController(self.pages, controller=self)
        self.page_controller.show_page("SubPage1", self.header_label)

    def pages_container(self):
        # Container for all pages
        self.pages_container = ctk.CTkFrame(self, width=300, height=300)
        self.pages_container.grid(row=0, column=0, sticky='nsew')

        # Pages
        self.pages = {}
        i = 0
        for F in (MainPage, SubPage1, SubPage2, SubPage3, SubPage4, SubPage5):
            page_name = F.__name__
            print(page_name)
            page = F(master=self.pages_container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.header_container()

        # Container for all pages
        self.pages_container.grid(row=1, column=0, sticky='nsew')

    def header_container(self):
        # Header frame
        self.header_frame = ctk.CTkFrame(self, height=100)
        self.header_frame.grid(row=0, column=0, sticky='ew')  # place at the top

        # Set fixed sizes for columns 0 and 2, and make column 1 expandable
        fixed_size = 300  # Adjust this value as needed for your layout
        self.header_frame.grid_columnconfigure(0, weight=0)  # Fixed size for column 0
        self.header_frame.grid_columnconfigure(1, weight=1)  # Column 1 expands
        self.header_frame.grid_columnconfigure(2, weight=0)  # Fixed size for column 2

        # self.header_frame.grid_propagate(False)

        # Left label with dummy text
        self.route_label = ctk.CTkLabel(self.header_frame, text="Trasa nezvolená", padx=30, font=('Arial', 26, 'bold'), width=400, anchor='w')
        self.route_label.grid(row=0, column=0, sticky='news')

        # Center label for page name
        self.header_label = ctk.CTkLabel(self.header_frame, text="", font=('Arial', 35, 'bold'))
        self.header_label.grid(row=0, column=1, sticky='news')

        # Right frame for date and time labels
        self.datetime_frame = ctk.CTkFrame(self.header_frame)
        self.datetime_frame.grid(row=0, column=2, sticky='e')

        # Time label with larger font
        self.time_label = ctk.CTkLabel(self.datetime_frame, text="", font=('Arial', 35, 'bold'), padx=10, width=400)
        self.time_label.grid(row=0, column=0, sticky='news')

        # Date label with smaller font
        self.date_label = ctk.CTkLabel(self.datetime_frame, text="", font=('Arial', 20), padx=10)
        self.date_label.grid(row=1, column=0, sticky='news')

        self.update_datetime()




    def update_datetime(self):
        '''Update the date and time display'''
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%d.%m.%Y')
        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)
        # Schedule the `update_datetime` method to be called after 1000ms
        self.after(1000, self.update_datetime)

    def create_nav_bar(self):
        button_size = 100
        col_num = 0

        icon_size = (200, 200)




        self.icons = self.get_icons()

        for text, page_name in self.page_display_names.items():
            button = ctk.CTkButton(self.nav_bar, text="", image=self.icons[col_num], command=lambda name=page_name: self.page_controller.show_page(name, self.header_label))
            button.image = self.icons[col_num]
            button.configure(font=("Arial", 15), width=button_size, height=button_size)
            button.grid(row=0, column=col_num, padx=50, pady=50, sticky="ew")

            self.nav_bar.grid_columnconfigure(col_num, minsize=button_size)
            col_num += 1  # Increment counter for each button

    def load_icons(self):
        home_icon = ctk.CTkImage(dark_image=Image.open("icons/navigation_bar/menu_icon.png"), size=(50, 50))
        route_icon = ctk.CTkImage(Image.open("icons/navigation_bar/route_icon.png"), size=(50, 50))
        drive_icon = ctk.CTkImage(Image.open("icons/navigation_bar/drive_icon.png"), size=(50, 50))
        text_icon = ctk.CTkImage(Image.open("icons/navigation_bar/message_icon.png"), size=(50, 50))
        diagnostics_icon = ctk.CTkImage(Image.open("icons/navigation_bar/diagnostics_icon.png"), size=(65, 65))
        settings_icon = ctk.CTkImage(Image.open("icons/navigation_bar/settings_icon.png"), size=(50, 50))

        self.icons = [home_icon, route_icon, drive_icon, text_icon, diagnostics_icon, settings_icon]

    def set_route_label(self, route_name):
        self.route_label.configure(text=route_name)

    def delete_route_label(self):

        self.route_label.configure(text='Trasa nezvolená')
