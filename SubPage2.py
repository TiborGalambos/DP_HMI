import customtkinter as ctk

import GLOBAL_VARS
from DatabaseManager import DatabaseManager
import tkintermapview

class SubPage2(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.path = None
        self.is_map_set = False
        self.controller = controller
        self.db_manager = DatabaseManager()
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.map_container = ctk.CTkFrame(self)
        self.map_container.grid(row=0, column=0, sticky="nwse", pady=20, padx=20)
        self.trip_stops_container = ctk.CTkFrame(self)
        self.trip_stops_container.grid(row=0, column=1, sticky="nwse", padx=20, pady=20)

        self.map_widget = tkintermapview.TkinterMapView(self.map_container, width=1200, height=1190, corner_radius=30)


        self.map_widget.grid(sticky="news", row=0, column=0, ipadx=0, ipady=20)


        self.label = ctk.CTkLabel(self.trip_stops_container, text="lol", anchor="center")

        self.label.grid(sticky="news", row=0, column=1)


        self.dbm = DatabaseManager()

        self.trip_coords = []
        self.map_widget.set_position(48.1978802998901, 17.306139)


    def set_map_markers(self):

        for name, x, y, time in self.dbm.fetch_trip_stop_times_with_coords(GLOBAL_VARS.active_trip_id):
            self.map_widget.set_marker(float(x), float(y))
            self.trip_coords.append((float(x), float(y)))

        self.path = self.map_widget.set_path(self.trip_coords)

        print(self.trip_coords)

        self.is_map_set = True

    def unset_map_markers(self):
        self.path.delete()
        self.is_map_set = False
        self.trip_coords = []
        self.map_widget.delete_all_marker()


















