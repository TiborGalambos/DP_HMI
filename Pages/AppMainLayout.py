import os
import time

import customtkinter as ctk
from screeninfo import get_monitors

import GLOBAL_VARS
from Managers.DatabaseManager import DatabaseManager
from Managers.PageControlManager import PageController
from Pages.SubPage5 import SubPage5
from Pages.SubPage4 import SubPage4
from Pages.SubPage3 import SubPage3
from Pages.SubPage2 import SubPage2
from Pages.SubPage1 import SubPage1
from Pages.MainPage import MainPage
from PIL import Image
fullscreen_mode = False

from Managers.CommunicationManager import CommunicationManager



# Main layout of the application that creates all the subpages and controls their basic functions

class AppMainLayout(ctk.CTk, PageController):

    def __init__(self):
        super().__init__()


        # defining the subpage names
        self.page_controller = PageController()
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
        communication = CommunicationManager.get_instance()
        try:
            communication.reset_message()
        except:
            pass

        # header row expand off by setting weight 0
        self.grid_rowconfigure(0, weight=0)
        # content / page row expand on by setting weight 1
        self.grid_rowconfigure(1, weight=1)
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

    # method that is used for helping to maximize the screen window
    def maximize_window(self):
        self.update_idletasks()
        self.update()
        self.state('zoomed')


    # development on two monitor setup, this method ensures that GUI will be opened on the second monitor
    def open_fullscreen_on_second_monitor(self):
        monitors = get_monitors()

        if len(monitors) > 1:
            second_monitor = monitors[0]
            self.geometry(f"{second_monitor.width}x{second_monitor.height}+{second_monitor.x}+{second_monitor.y}")
            print(f"{second_monitor.width}x{second_monitor.height}")
        else:
            print("Only one monitor detected. Opening fullscreen on the primary monitor.")
            self.attributes("-fullscreen", True)


    # container for navbar, that is always displayed at the bottom of the screen
    def navigation_bar_container(self):
        # Navigation bar
        self.nav_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.create_nav_bar()
        self.nav_bar.grid_rowconfigure(0, weight=0)
        self.nav_bar.grid_columnconfigure(index=0, weight=1)
        self.nav_bar.grid(row=2, column=0, sticky='s')

        self.page_controller.setup(self.pages, controller=self)
        self.page_controller.set_header_label(self.header_label)
        self.page_controller.show_page("MainPage")


    # container for all subpages
    def pages_container(self):
        self.pages_container = ctk.CTkFrame(self, width=300, height=300)
        self.pages_container.grid(row=0, column=0, sticky='nsew')

        self.pages = {}
        i = 0
        for F in (MainPage, SubPage1, SubPage2, SubPage3, SubPage4, SubPage5):
            page_name = F.__name__
            print(page_name)
            page = F(master=self.pages_container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.header_container()

        self.pages_container.grid(row=1, column=0, sticky='nsew')



    def header_container(self):
        self.header_frame = ctk.CTkFrame(self, height=100)
        self.header_frame.grid(row=0, column=0, sticky='ew')

        fixed_size = 300
        self.header_frame.grid_columnconfigure(0, weight=0)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=0)

        # route id label initialize
        self.route_label = ctk.CTkLabel(self.header_frame, text="Trasa nezvolená", padx=30, font=('Arial', 26, 'bold'), width=400, anchor='w')
        self.route_label.grid(row=0, column=0, sticky='news')

        # label for page name
        self.header_label = ctk.CTkLabel(self.header_frame, text="", font=('Arial', 35, 'bold'))
        self.header_label.grid(row=0, column=1, sticky='news')

        # frame for date and time labels
        self.datetime_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.datetime_frame.grid(row=0, column=2, sticky='e')

        # time
        self.time_label = ctk.CTkLabel(self.datetime_frame, text="", font=('Arial', 35, 'bold'), padx=10, width=400)
        self.time_label.grid(row=0, column=0, sticky='news')

        # date
        self.date_label = ctk.CTkLabel(self.datetime_frame, text="", font=('Arial', 20), padx=10)
        self.date_label.grid(row=1, column=0, sticky='news')

        self.update_datetime()


    # update the time every second
    def update_datetime(self):
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%d.%m.%Y')
        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)
        self.after(1000, self.update_datetime)

    # navbar initialization and icon placement
    def create_nav_bar(self):
        button_size = 100
        col_num = 0

        self.icons = self.get_icons()

        for text, page_name in self.page_display_names.items():
            button = ctk.CTkButton(self.nav_bar, text="", image=self.icons[col_num],
                                   command=lambda name=page_name: self.page_controller.show_page(
                                       name, self.header_label))
            button.image = self.icons[col_num]
            button.configure(font=("Arial", 15), width=button_size, height=button_size)
            button.grid(row=0, column=col_num, padx=50, pady=50, sticky="ew")

            self.nav_bar.grid_columnconfigure(col_num, minsize=button_size)
            col_num += 1


    # loading the icons to list for further usage
    def load_icons(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        icons_path = os.path.join(base_path, "icons", "navigation_bar")

        home_icon = ctk.CTkImage(dark_image=Image.open(os.path.join(icons_path, "menu_icon.png")), size=(50, 50))
        route_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "route_icon.png")), size=(50, 50))
        drive_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "drive_icon.png")), size=(50, 50))
        text_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "message_icon.png")), size=(50, 50))
        diagnostics_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "diagnostics_icon.png")), size=(65, 65))
        settings_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "settings_icon.png")), size=(50, 50))

        self.icons = [home_icon, route_icon, drive_icon, text_icon, diagnostics_icon, settings_icon]


    def set_route_label(self, route_name):
        self.route_label.configure(text=route_name)

    # method for further setting the route id label to default value
    def delete_route_label(self):
        self.route_label.configure(text='Trasa nezvolená')
        GLOBAL_VARS.active_trip_id = 0

    # method for switching between subpages using page controller
    def switch_page(self, page_name):
        self.page_controller.show_page(page_name)
        if page_name == 'SubPage2' and not self.pages['SubPage2'].is_map_set:
            self.pages['SubPage2'].set_map_markers()

     #method for unsetting the map markers on subpage2, that needs to be accessible globally
    def unset_subpage2_map_markers(self):
        self.pages['SubPage2'].unset_map_markers()


