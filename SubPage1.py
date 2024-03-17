
from DatabaseManager import DatabaseManager
from PIL import Image

import customtkinter as ctk

class SubPage1(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.db_manager = DatabaseManager()
        self.controller = controller
        self.current_index_trip = 0  # Keep track of the current index of the displayed route
        self.current_index_route = 0  # Keep track of the current index of the displayed route
        self.max_display_trip = 8  # Maximum number of routes to display at a time
        self.max_display_route = 6  # Maximum number of routes to display at a time

        self.selected_route_id = 0

        # Configure grid for the whole page
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        self.grid_rowconfigure(index=0, weight=1)

        self.routes_list_container = ctk.CTkFrame(self)
        self.routes_list_container.grid(row=0, column=0, sticky="nwse", padx=(20, 10), pady=20)
        self.routes_list_container.grid_columnconfigure(0, weight=1)
        self.routes_list_container.grid_rowconfigure(1, weight=1)

        self.trips_list_container = ctk.CTkFrame(self)
        self.trips_list_container.grid(row=0, column=1, sticky="nwes", padx=(20, 10), pady=20)
        self.trips_list_container.grid_columnconfigure(0, weight=1)
        self.trips_list_container.grid_rowconfigure(1, weight=1)



        # Right side container for selected route details
        self.details_container = ctk.CTkFrame(self)
        self.details_container.grid(row=0, column=3, sticky="news", padx=0, pady=20)
        self.details_container.grid_columnconfigure(0, weight=1)
        self.details_container.grid_columnconfigure(1, weight=1)
        self.details_container.grid_rowconfigure(index=0, weight=0)
        self.details_container.grid_rowconfigure(index=1, weight=1)

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
        self.trips_frame = ctk.CTkFrame(self.trips_list_container)
        self.trips_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        self.trips_frame.grid_columnconfigure(0, weight=1)

        # Container for trips
        self.routes_frame = ctk.CTkFrame(self.routes_list_container)
        self.routes_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        self.routes_frame.grid_columnconfigure(0, weight=1)


        self.selected_trip_header_label = ctk.CTkLabel(self.details_container, text="Detail spoja", width=500, font=("Arial", 30))
        self.selected_trip_header_label.grid(row=0, column=0, sticky="nws", pady=0)

        # Selected route details
        self.selected_trip_label = ctk.CTkLabel(self.details_container, text="Vyberte spoj!", width= 300, anchor='center', font=("Arial", 20))
        self.selected_trip_label.grid(row=1, column=0, sticky="nesw", pady=0)

        self.stop_name_labels = []
        self.stop_time_labels = []

        self.populate_trips()
        self.populate_routes()
        self.update_displayed_routes()

        self.selected_route_button = None  # This will hold the reference to the currently selected button

        self.selected_trip_button = None

        self.selected_trip_id = 0
        self.selected_route_id = 0

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
            print(i)
            self.display_trips(self.trip_data[i], i)

        print(f"update trips func - current_index_trip: {self.current_index_trip}")

        self.check_trips_button_state()

    def display_trips(self, route, index):
        button_color = "#0c2b43" if route[0] == getattr(self, 'selected_trip_id', None) else "#144870"  # Default color

        trip_button = ctk.CTkButton(self.trips_frame, text=f"{route[1]}", command=lambda r=route: self.select_trip(r), font=("Arial", 30), width=200, fg_color=button_color, hover_color="#0c2b43")
        trip_button.grid(row=index, column=0, sticky="ew", padx=10, pady=10, ipadx=5, ipady=20)

        print(route[0], self.current_index_trip)

    def select_trip(self, trip):

        trip_stop_times = self.db_manager.fetch_trip_stop_times(trip[0])

        # Clear existing labels if any
        for label in getattr(self, 'stop_name_labels', []):
            label.destroy()
        for label in getattr(self, 'stop_time_labels', []):
            label.destroy()

        self.selected_trip_label.destroy()

        self.stop_name_labels = []
        self.stop_time_labels = []

        # Starting row for displaying the labels
        row = 2

        for stop_name, stop_time in trip_stop_times:
            # Create a label for the stop name and align it to the left
            stop_name_label = ctk.CTkLabel(self.details_container, text=stop_name, anchor='n', font=("Arial", 25))
            stop_name_label.grid(row=row, column=0, sticky="w", pady=20, padx=20)

            # Create a label for the stop time and align it to the left
            stop_time_label = ctk.CTkLabel(self.details_container, text=stop_time, anchor='n', font=("Arial", 20))
            stop_time_label.grid(row=row, column=1, sticky="e", pady=20, padx=20)

            # Add the labels to the lists for future reference
            self.stop_name_labels.append(stop_name_label)
            self.stop_time_labels.append(stop_time_label)

            # Move to the next row for the next set of labels
            row += 1

        # Update the selected trip ID and any other necessary UI components
        self.selected_trip_id = trip[0]
        self.update_displayed_trips()

    def display_routes(self, route, index):
        button_color = "#0c2b43" if route[0] == getattr(self, 'selected_route_id', None) else "#144870"  # Default color

        route_button = ctk.CTkButton(self.routes_frame, text=f"{route[1]}\n{route[2]}", command=lambda r=route: self.select_route(r), font=("Arial", 30), width=200, fg_color=button_color, hover_color="#0c2b43")
        route_button.grid(row=index, column=0, sticky="ew", padx=10, pady=10, ipadx=5, ipady=17)

        print(route[0], self.current_index_route)

    def select_route(self, route):
        info = f"Selected Route: {route[0]}"
        print(info)
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

