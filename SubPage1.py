import GLOBAL_VARS
from CommunicationManager import CommunicationManager
from DatabaseManager import DatabaseManager
from PIL import Image

import customtkinter as ctk
import tkinter.ttk as ttk
import tkinter as tk

from SubPage2 import SubPage2


class SubPage1(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.panel2 = None
        self.panel1 = None
        self.show_delay = None
        self.db_manager = DatabaseManager()
        self.controller = controller
        self.current_index_trip = 0  # Keep track of the current index of the displayed route
        self.current_index_route = 0  # Keep track of the current index of the displayed route
        self.max_display_trip = 8  # Maximum number of routes to display at a time
        self.max_display_route = 6  # Maximum number of routes to display at a time

        self.selected_route_id = 0
        self.is_trip_selected = False
        self.selected_trip_name = ''

        # Configure grid for the whole page
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(index=0, weight=1)

        self.routes_list_container = ctk.CTkFrame(self)
        self.routes_list_container.grid(row=0, column=0, sticky="nwse", padx=(20, 10), pady=20)
        self.routes_list_container.grid_columnconfigure(0, weight=1)
        self.routes_list_container.grid_rowconfigure(1, weight=1)

        self.trips_list_container = ctk.CTkFrame(self)
        self.trips_list_container.grid(row=0, column=1, sticky="nwes", padx=(10, 10), pady=20)
        self.trips_list_container.grid_columnconfigure(0, weight=1)
        self.trips_list_container.grid_rowconfigure(1, weight=1)


        # Right side container for selected route details
        self.details_container = ctk.CTkFrame(self)
        self.details_container.configure(width=350)

        self.details_container.grid(row=0, column=2, sticky="news", padx=(10, 10), pady=20)

        self.details_container.grid_columnconfigure(0, weight=1)
        self.details_container.grid_columnconfigure(1, weight=1)

        self.details_container.grid_rowconfigure(index=0, weight=0)
        self.details_container.grid_rowconfigure(index=1, weight=1)

        self.details_container.grid_propagate(False)

        self.settings_container = ctk.CTkFrame(self)
        self.settings_container.grid(row=0, column=3, sticky="news", padx=(10, 20), pady=20)
        self.settings_container.grid_columnconfigure(0, weight=1)
        self.settings_container.grid_columnconfigure(1, weight=1)

        self.settings_container.grid_rowconfigure(0, weight=0)
        self.settings_container.grid_rowconfigure(1, weight=0)
        self.settings_container.grid_rowconfigure(2, weight=0)
        self.settings_container.grid_rowconfigure(3, weight=0)
        self.settings_container.grid_rowconfigure(4, weight=0)

        self.settings_container_header_label = ctk.CTkLabel(self.settings_container, text="Nastavenia trasy",
                                                            font=("Arial", 30), anchor='center')
        self.settings_container_header_label.grid(row=0, column=0, sticky="ew", pady=(0, 50), columnspan=2)

        self.display_panel_settings = ctk.CTkLabel(self.settings_container, text="Vybraná trasa", font=("Arial", 20),
                                                   anchor='w')
        self.display_panel_settings.grid(row=1, column=0, pady=(20, 0), padx=20)

        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=2, column=0, padx=100, pady=0, columnspan=2, sticky='news')

        self.settings_route_name = ctk.CTkLabel(self.settings_container, text="-", font=("Arial", 20),
                                                   anchor='w', height=100)
        self.settings_route_name.grid(row=3, column=0, pady=(20, 0), padx=20)




        self.display_panel_settings = ctk.CTkLabel(self.settings_container, text="Výber panelov", font=("Arial", 20),
                                                   anchor='w')
        self.display_panel_settings.grid(row=4, column=0, pady=(20, 0), padx=20)

        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=5, column=0, padx=100, pady=0, columnspan=2, sticky='news')




        # Create a CTkCheckBox



        self.switch_setting_1 = ctk.IntVar()  # This variable will hold the state of the checkbox, 0 for unchecked, 1 for checked

        self.switch1 = ctk.CTkSwitch(self.settings_container, text="Zapnúť zobrazenie trasy na vonk. paneli č.1", variable=self.switch_setting_1,
                                        onvalue=1, offvalue=0, command=self.switch1_callback, font=("Arial", 30))
        self.switch1.grid(row=6, column=0, pady=20, padx=20, columnspan=2)

        # Create a CTkCheckBox
        self.switch_setting_2 = ctk.IntVar()  # This variable will hold the state of the checkbox, 0 for unchecked, 1 for checked

        self.switch2 = ctk.CTkSwitch(self.settings_container, text="Zapnúť zobrazenie trasy na vonk. paneli č.2", variable=self.switch_setting_2,
                                     onvalue=1, offvalue=0, command=self.switch2_callback, font=("Arial", 30))
        self.switch2.grid(row=7, column=0, pady=20, padx=20, columnspan=2)



        self.drive_mode =  ctk.CTkLabel(self.settings_container, text="Zobraziť meškanie na paneli", font=("Arial", 20), anchor='w')

        self.drive_mode.grid(row=8, column=0, pady=(20,0), padx=20)

        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=9,column = 0, padx=100, pady=0, columnspan = 2, sticky='news')

        # Create a CTkCheckBox
        self.switch_setting_3 = ctk.IntVar()  # This variable will hold the state of the checkbox, 0 for unchecked, 1 for checked
        self.switch_setting_3.set(1)
        self.switch3 = ctk.CTkCheckBox(self.settings_container, text="Zobraziť", variable=self.switch_setting_3,
                                     onvalue=1, offvalue=0, command=self.switch3_callback, font=("Arial", 30))
        self.switch3.grid(row=10, column=0, pady=20, padx=20)

        # Create a CTkCheckBox
        self.switch_setting_4 = ctk.IntVar()  # This variable will hold the state of the checkbox, 0 for unchecked, 1 for checked
        self.switch_setting_4.set(0)
        self.switch4 = ctk.CTkCheckBox(self.settings_container, text="Nezobraziť", variable=self.switch_setting_4,
                                     onvalue=1, offvalue=0, command=self.switch4_callback, font=("Arial", 30))
        self.switch4.grid(row=10, column=1, pady=20, padx=20)

        self.settings_container.grid_rowconfigure(index=8, weight=1)

        self.cancel_button = ctk.CTkButton(self.settings_container, text="Zrušiť jazdu", fg_color='red', hover_color='darkred',
                                           font=("Arial", 30), width=200, command=self.stop)
        self.cancel_button.grid(row=11, column=0, sticky='ws', pady=50, padx=(100,0), ipadx=20, ipady=70)

        self.finish_button = ctk.CTkButton(self.settings_container, text="Začať jazdu", fg_color='green', font=("Arial", 30), width=200, hover_color='darkgreen', command=self.start_the_trip)
        self.finish_button.grid(row=11, column=1, sticky='es', pady = 50, padx= (0,100), ipadx=20, ipady=70)


        # Load the image (assuming it's in the same directory as your script)
        arrow_up = Image.open("icons/arrows/arrow_up.png")  # Replace 'your_image.png' with your image file
        arrow_up = arrow_up.resize((100, 100),
                                   Image.Resampling.LANCZOS)  # Resize the image to fit the button, if necessary
        arrow_up_icon = ctk.CTkImage(arrow_up)

        # Navigation buttons
        self.up_button_trip = ctk.CTkButton(self.trips_list_container, text="", command=self.scroll_up_trip, image=arrow_up_icon)
        self.up_button_trip.image = arrow_up_icon
        self.up_button_trip.grid(row=0, column=0, sticky="news", padx=20, pady=(0, 10), ipady = 20, ipadx=120)

        self.up_button_route = ctk.CTkButton(self.routes_list_container, text="", command=self.scroll_up_route, image=arrow_up_icon)
        self.up_button_route.image = arrow_up_icon
        self.up_button_route.grid(row=0, column=0, sticky="news", padx=20, pady=(0, 10), ipady=20, ipadx=120)

        arrow_down = Image.open("icons/arrows/arrow_down.png")  # Replace 'your_image.png' with your image file
        arrow_down = arrow_down.resize((25, 25),
                                   Image.Resampling.LANCZOS)  # Resize the image to fit the button, if necessary
        arrow_down_icon = ctk.CTkImage(arrow_down, size=(25, 25))

        self.down_button_trip = ctk.CTkButton(self.trips_list_container, text="", command=self.scroll_down_trip, image=arrow_down_icon)
        self.down_button_trip.image = arrow_down_icon
        self.down_button_trip.grid(row=2, column=0, sticky="news", padx=20, pady=(10, 0), ipady = 20, ipadx=120)

        self.down_button_route = ctk.CTkButton(self.routes_list_container, text="", command=self.scroll_down_route, image=arrow_down_icon)
        self.down_button_route.image = arrow_down_icon
        self.down_button_route.grid(row=2, column=0, sticky="news", padx=20, pady=(10, 0), ipady=20, ipadx=120)

        # Container for routes
        self.trips_frame = ctk.CTkFrame(self.trips_list_container, fg_color="transparent")
        self.trips_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        self.trips_frame.grid_columnconfigure(0, weight=1)

        # Container for trips
        self.routes_frame = ctk.CTkFrame(self.routes_list_container, fg_color="transparent")
        self.routes_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        self.routes_frame.grid_columnconfigure(0, weight=1)


        self.selected_trip_header_label = ctk.CTkLabel(self.details_container, text="Detail spoja", font=("Arial", 30), anchor='center')
        self.selected_trip_header_label.grid(row=0, column=0, sticky="ew", pady=0, columnspan = 2)

        # Selected route details
        self.selected_trip_label = ctk.CTkLabel(self.details_container, text="Vyberte spoj!", width= 300, anchor='center', font=("Arial", 20))
        self.selected_trip_label.grid(row=1, column=0, sticky="nesw", pady=0, columnspan = 2)

        self.stop_name_labels = []
        self.stop_time_labels = []

        self.populate_trips()
        self.populate_routes()
        self.update_displayed_routes()

        self.selected_route_button = None  # This will hold the reference to the currently selected button

        self.selected_trip_button = None

        self.selected_trip_id = 0

        self.selected_route_id = 0

        self.set_settings_button_state()



    def switch_window(self):
        self.controller.switch_page("SubPage2")
        # pass

    def start_the_trip(self):

        if self.finish_button.cget("text") != "Prebieha jazda":

            self.panel1 = False
            self.panel2 = False
            self.show_delay = False

            if self.is_trip_selected:

                if self.switch_setting_1.get() == 1:
                    self.panel1 = True

                if self.switch_setting_2.get() == 1:
                    self.panel2 = True


                self.controller.set_route_label(self.selected_trip_name)
            else:
                print("Cannot start, trip not selected!")


            print(self.switch_setting_3.get(), self.switch_setting_4.get())

            if self.switch_setting_3.get() and not self.switch_setting_4.get():
                print("Delay_display: ON")
                self.show_delay = True

            elif not self.switch_setting_3.get() and self.switch_setting_4.get():
                print("Delay_display: OFF")
                self.show_delay = False


            else:
                print("Something went wrong")
                pass


            # self.set_settings_button_state()
            self.finish_button.configure(state=ctk.DISABLED, fg_color="#A9C8A9")  # Darker color when disabled
            self.finish_button.configure(text="Prebieha jazda")
            GLOBAL_VARS.selected_trip_name = self.selected_trip_name

            communication = CommunicationManager.get_instance()
            communication.send_settings(display_1=self.panel1,
                                        display_2=self.panel2,
                                        show_delay=self.show_delay)

            # print("sleep?")

            self.switch_window()




    def stop(self):

        if self.is_trip_selected:

            self.controller.delete_route_label()
            self.settings_route_name.configure(text='-', font=("Arial", 30),
                                               anchor='center', height=100)
            self.is_trip_selected = False
        else:
            print("Cannot cancel, trip not selected!")

        self.set_settings_button_state()
        GLOBAL_VARS.active_trip_id = 0
        try:
            self.controller.unset_subpage2_map_markers()
        except:
            pass
        self.finish_button.configure(text="Začať jazdu")
        GLOBAL_VARS.selected_trip_name = ''

        com_man = CommunicationManager.get_instance()
        com_man.reset_message()


    def switch1_callback(self):
        print("Checkbox checkbox1 state changed:", self.switch_setting_1.get())

    def switch2_callback(self):
        print("Checkbox checkbox2 state changed:", self.switch_setting_2.get())

    def switch3_callback(self):
        print("Checkbox checkbox3 state changed:", self.switch_setting_3.get())
        if self.switch_setting_3.get() == 1:  # If switch3 is checked
            self.switch_setting_4.set(0)  # Uncheck switch4

        if self.switch_setting_3.get() == 0:  # If switch3 is checked
            self.switch_setting_4.set(1)

        # self.switch4_callback()


    def switch4_callback(self):
        print("Checkbox checkbox4 state changed:", self.switch_setting_4.get())
        if self.switch_setting_4.get() == 1:  # If switch4 is checked
            self.switch_setting_3.set(0)  # Uncheck switch3

        if self.switch_setting_4.get() == 0:  # If switch4 is checked
            self.switch_setting_3.set(1)  # Uncheck switch3


    def populate_trips(self):
        self.trip_data = self.db_manager.fetch_trip_by_route_id(self.selected_route_id)
        self.check_trips_button_state()

    def populate_routes(self):
        self.route_data = self.db_manager.fetch_routes()

    def update_displayed_routes(self):
        for widget in self.routes_frame.winfo_children():
            widget.destroy()

        for i in range(self.current_index_route, min(self.current_index_route + self.max_display_route, len(self.route_data))):
            self.display_routes(self.route_data[i], i)

        self.check_routes_button_state()

    def update_displayed_trips(self):
        for widget in self.trips_frame.winfo_children():
            widget.destroy()

        for i in range(self.current_index_trip, min(self.current_index_trip + self.max_display_trip, len(self.trip_data))):
            self.display_trips(self.trip_data[i], i)


        self.check_trips_button_state()

    def display_trips(self, route, index):
        button_color = "#0c2b43" if route[0] == getattr(self, 'selected_trip_id', None) else "#144870"  # Default color

        trip_button = ctk.CTkButton(self.trips_frame, text=f"{route[1]}", command=lambda r=route: self.select_trip(r), font=("Arial", 30), width=200, fg_color=button_color, hover_color="#0c2b43")
        trip_button.grid(row=index, column=0, sticky="ew", padx=10, pady=10, ipadx=5, ipady=20)


    def select_trip(self, trip):

        trip_stop_times = self.db_manager.fetch_trip_stop_times(trip[0])

        # Clear existing labels if any
        for label in getattr(self, 'stop_name_labels', []):
            label.destroy()
        for label in getattr(self, 'stop_time_labels', []):
            label.destroy()

        self.selected_trip_label.destroy()

        self.details_container.grid_rowconfigure(1,weight=0)

        self.stop_name_labels = []
        self.stop_time_labels = []

        # Starting row for displaying the labels
        row = 1


        for stop_name, stop_time in trip_stop_times:
            # Create a label for the stop name and align it to the left
            stop_name_label = ctk.CTkLabel(self.details_container, text=stop_name, anchor='w', font=("Arial", 15))
            stop_time_label = ctk.CTkLabel(self.details_container, text=stop_time, anchor='e', font=("Arial", 15))

            if row == 1:
                stop_name_label.grid(row=row, column=0, sticky="w", pady=(50,5), padx=(20, 0))
                stop_time_label.grid(row=row, column=1, sticky="e", pady=(50,5), padx=(0, 20))
            else:
                stop_name_label.grid(row=row, column=0, sticky="w", pady=5, padx=(20,0))
                stop_time_label.grid(row=row, column=1, sticky="e", pady=5, padx=(0, 20))

            # Create a label for the stop time and align it to the left



            # Add the labels to the lists for future reference
            self.stop_name_labels.append(stop_name_label)
            self.stop_time_labels.append(stop_time_label)

            # Move to the next row for the next set of labels
            row += 1

        # Update the selected trip ID and any other necessary UI components

        if self.finish_button.cget("text") != "Prebieha jazda":
            self.selected_trip_id = trip[0]
            GLOBAL_VARS.active_trip_id = trip[0]
            self.update_displayed_trips()

            self.is_trip_selected = True

            self.selected_trip_name = trip[1]

            self.settings_route_name.configure(text=self.selected_trip_name, font=("Arial", 30),
                                                    anchor='center', height=100)

            self.set_settings_button_state()


    def display_routes(self, route, index):
        button_color = "#0c2b43" if route[0] == getattr(self, 'selected_route_id', None) else "#144870"  # Default color

        route_button = ctk.CTkButton(self.routes_frame, text=f"{route[1]}\n{route[2]}", command=lambda r=route: self.select_route(r), font=("Arial", 30), width=200, fg_color=button_color, hover_color="#0c2b43")
        route_button.grid(row=index, column=0, sticky="ew", padx=10, pady=10, ipadx=5, ipady=17)


    def select_route(self, route):
        info = f"Selected Route: {route[0]}"
        self.selected_route_id = route[0]
        self.current_index_trip = 0
        self.populate_trips()
        self.update_displayed_trips()
        self.update_displayed_routes()


    def scroll_up_trip(self):
        if self.current_index_trip >= self.max_display_trip:
            self.current_index_trip -= self.max_display_trip
            self.update_displayed_trips()

    def scroll_down_trip(self):
        if self.current_index_trip + self.max_display_trip < len(self.trip_data):
            self.current_index_trip += self.max_display_trip
            self.update_displayed_trips()

    def check_trips_button_state(self):
        # Check "Up" button state
        if self.current_index_trip < self.max_display_trip:
            self.up_button_trip.configure(state=ctk.DISABLED, fg_color="#A9A9A9")  # Darker color when disabled
        else:
            self.up_button_trip.configure(state=ctk.NORMAL, fg_color="green")  # Original color when enabled

        # Check "Down" button state
        if self.current_index_trip + self.max_display_trip >= len(self.trip_data):
            self.down_button_trip.configure(state=ctk.DISABLED, fg_color="#A9A9A9")
        else:
            self.down_button_trip.configure(state=ctk.NORMAL, fg_color="green")



    def scroll_up_route(self):
        if self.current_index_route >= self.max_display_route:
            self.current_index_route -= self.max_display_route
            self.update_displayed_routes()

    def scroll_down_route(self):
        if self.current_index_route + self.max_display_route < len(self.route_data):
            self.current_index_route += self.max_display_route
            self.update_displayed_routes()

    def check_routes_button_state(self):
        if self.current_index_route < self.max_display_route:
            self.up_button_route.configure(state=ctk.DISABLED, fg_color="#A9A9A9")  # Darker color when disabled
        else:
            self.up_button_route.configure(state=ctk.NORMAL, fg_color="green")  # Original color when enabled

        # Check "Down" button state
        if self.current_index_route + self.max_display_route >= len(self.route_data):
            self.down_button_route.configure(state=ctk.DISABLED, fg_color="#A9A9A9")
        else:
            self.down_button_route.configure(state=ctk.NORMAL, fg_color="green")

    def set_settings_button_state(self):
        if not self.is_trip_selected:
            self.finish_button.configure(state=ctk.DISABLED, fg_color="#A9C8A9")  # Darker color when disabled
            self.cancel_button.configure(state=ctk.DISABLED, fg_color="#EBA9A9")
        else:
            self.finish_button.configure(state=ctk.NORMAL, fg_color="green")  # Darker color when disabled
            self.cancel_button.configure(state=ctk.NORMAL, fg_color="red")

