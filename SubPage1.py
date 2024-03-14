
from DatabaseManager import DatabaseManager
from PIL import Image

import customtkinter as ctk

class SubPage1(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.db_manager = DatabaseManager()
        self.controller = controller
        self.current_index = 0  # Keep track of the current index of the displayed route
        self.max_display = 8  # Maximum number of routes to display at a time

        # Configure grid for the whole page
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        self.grid_rowconfigure(index=0, weight=1)

        # Left side container for the list and buttons
        self.list_container = ctk.CTkFrame(self)
        self.list_container.grid(row=0, column=0, sticky="nws", padx=(20, 10), pady=20)
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(1, weight=1)

        # Right side container for selected route details
        self.details_container = ctk.CTkFrame(self)

        self.details_container.grid(row=0, column=1, sticky="news", padx=0, pady=20)
        self.details_container.grid_columnconfigure(0, weight=1)
        self.details_container.grid_rowconfigure(index=0, weight=0)
        self.details_container.grid_rowconfigure(index=1, weight=1)

        # Load the image (assuming it's in the same directory as your script)
        arrow_up = Image.open("icons/arrows/arrow_up.png")  # Replace 'your_image.png' with your image file
        arrow_up = arrow_up.resize((100, 100),
                                   Image.Resampling.LANCZOS)  # Resize the image to fit the button, if necessary
        arrow_up_icon = ctk.CTkImage(arrow_up)

        # Navigation buttons
        self.up_button = ctk.CTkButton(self.list_container, text="", command=self.scroll_up, image=arrow_up_icon)
        self.up_button.image = arrow_up_icon
        self.up_button.grid(row=0, column=0, sticky="ew", padx=20, pady=(0, 10), ipady = 20)

        arrow_down = Image.open("icons/arrows/arrow_down.png")  # Replace 'your_image.png' with your image file
        arrow_down = arrow_down.resize((25, 25),
                                   Image.Resampling.LANCZOS)  # Resize the image to fit the button, if necessary
        arrow_down_icon = ctk.CTkImage(arrow_down, size=(25, 25))

        self.down_button = ctk.CTkButton(self.list_container, text="", command=self.scroll_down, image=arrow_down_icon)
        self.down_button.image = arrow_down_icon
        self.down_button.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 0), ipady = 20)

        # Container for routes
        self.routes_frame = ctk.CTkFrame(self.list_container)
        self.routes_frame.grid(row=1, column=0, sticky="nw", padx=20)
        self.routes_frame.grid_columnconfigure(0, weight=1)


        self.selected_route_header_label = ctk.CTkLabel(self.details_container, text="Detail spoja", width=300, font=("Arial", 30))
        self.selected_route_header_label.grid(row=0, column=0, sticky="nws", pady=0)

        # Selected route details
        self.selected_route_label = ctk.CTkLabel(self.details_container, text="Select a route", width= 300, anchor='w')
        self.selected_route_label.grid(row=1, column=0, sticky="nws", pady=0)

        self.populate_routes()
        self.update_displayed_routes()

        self.selected_button = None  # This will hold the reference to the currently selected button


    def populate_routes(self):
        self.route_data = self.db_manager.fetch_routes()
        self.check_button_state()

    def update_displayed_routes(self):
        # Clear the current routes
        for widget in self.routes_frame.winfo_children():
            widget.destroy()

        # Display up to 4 routes starting from the current index
        for i in range(self.current_index, min(self.current_index + self.max_display, len(self.route_data))):
            self.display_route(self.route_data[i], i)


        self.check_button_state()

    def display_route(self, route, index):
        button_color = "#0c2b43" if route[0] == getattr(self, 'selected_route_id', None) else "#144870"  # Default color

        route_button = ctk.CTkButton(self.routes_frame, text=f"{route[0]}", command=lambda r=route: self.select_route(r), font=("Arial", 30), width=200, fg_color=button_color, hover_color="#0c2b43")
        route_button.grid(row=index, column=0, sticky="ew", padx=10, pady=10, ipadx=5, ipady=20)

    def select_route(self, route):
        # Update the selected_route_label with more info about the route
        info = f"Selected Route: {route[0]}\nFrom: {route[1]} To: {route[2]}\nDeparture: {route[3]} Arrival: {route[4]}"
        start = route
        self.selected_route_label.configure(text=info, anchor='w')

        # Print the selected route to the console
        print(info)

        # Update the selected_route_id and refresh the display
        self.selected_route_id = route[0]
        self.update_displayed_routes()

    def scroll_up(self):
        if self.current_index >= self.max_display:
            self.current_index -= self.max_display
            self.update_displayed_routes()

    def scroll_down(self):
        if self.current_index + self.max_display < len(self.route_data):
            self.current_index += self.max_display
            self.update_displayed_routes()

    def check_button_state(self):
        # Check "Up" button state
        if self.current_index < self.max_display:
            self.up_button.configure(state=ctk.DISABLED, fg_color="#A9A9A9")  # Darker color when disabled
        else:
            self.up_button.configure(state=ctk.NORMAL, fg_color="green")  # Original color when enabled

        # Check "Down" button state
        if self.current_index + self.max_display >= len(self.route_data):
            self.down_button.configure(state=ctk.DISABLED, fg_color="#A9A9A9")
        else:
            self.down_button.configure(state=ctk.NORMAL, fg_color="green")
