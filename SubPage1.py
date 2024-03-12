import datetime
from tkinter import Canvas, Scrollbar

import customtkinter as ctk
from DatabaseManager import DatabaseManager


# Vyber trasy Page
# class SubPage1(ctk.CTkFrame):
#     def __init__(self, master, controller):
#         super().__init__(master)
#         # master.grid_columnconfigure(0, weight=1)
#         # master.grid_rowconfigure(0, weight=1)
#         self.controller = controller
#
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(index=1, weight=2)
#
#         self.routes_container = ctk.CTkFrame(self)
#         self.routes_container.grid(row=0, column=0, sticky="nsew", padx = 50, pady = 50)
#
#
#         self.selected_route_container = ctk.CTkFrame(self)
#         self.selected_route_container.grid(row=0, column=1, sticky="nsew", padx = 50, pady = 50)
#
#
#         self.label1 = ctk.CTkLabel(self.routes_container, text="box 1")
#         self.label1.grid(row=0, column=0)
#         self.label2 = ctk.CTkLabel(self.selected_route_container, text="box 2")
#         self.label2.grid(row=0, column=1)

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class SubPage1(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.db_manager = DatabaseManager()
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # Scrollable container for routes
        self.routes_container = ctk.CTkFrame(self)
        self.routes_container.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
        self.routes_canvas = tk.Canvas(self.routes_container, bg='#2b2b2b')
        self.routes_scrollbar = ttk.Scrollbar(self.routes_container, orient="vertical",
                                              command=self.routes_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.routes_canvas)
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.routes_canvas.configure(scrollregion=self.routes_canvas.bbox("all")))
        self.routes_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.routes_canvas.configure(yscrollcommand=self.routes_scrollbar.set)
        self.routes_canvas.pack(side="left", fill="both", expand=True)
        self.routes_scrollbar.pack(side="right", fill="y")

        # Container for selected route details
        self.selected_route_container = ctk.CTkFrame(self)
        self.selected_route_container.grid(row=0, column=1, sticky="nsew", padx=50, pady=50)
        self.selected_route_label = ctk.CTkLabel(self.selected_route_container, text="Select route")
        self.selected_route_label.pack(pady=10)

        self.populate_routes()
        self.add_scroll_by_dragging()

    def populate_routes(self):
        route_data = self.db_manager.fetch_routes()

        for route in route_data:
            route_frame = ttk.Frame(self.scrollable_frame)
            route_frame.pack(pady=10, padx=10, fill="x", expand=True)

            route_number_label = ttk.Label(route_frame, text=route[0], font=('Arial', 30, 'bold'))
            route_number_label.grid(row=0, column=0, rowspan=4, sticky="ns", padx=10)
            route_number_label.bind("<Button-1>", lambda e, r=route: self.select_route(r))

            start_stop_label = ttk.Label(route_frame, text=route[1], font=('Arial', 20))
            start_stop_label.grid(row=0, column=1, sticky="w")
            start_stop_label.bind("<Button-1>", lambda e, r=route: self.select_route(r))

            start_time_label = ttk.Label(route_frame, text=route[3].strftime('%H:%M'), font=('Arial', 16))
            start_time_label.grid(row=1, column=1, sticky="w")
            start_time_label.bind("<Button-1>", lambda e, r=route: self.select_route(r))

            destination_stop_label = ttk.Label(route_frame, text=route[2], font=('Arial', 20))
            destination_stop_label.grid(row=2, column=1, sticky="w")
            destination_stop_label.bind("<Button-1>", lambda e, r=route: self.select_route(r))

            destination_time_label = ttk.Label(route_frame, text=route[4].strftime('%H:%M'), font=('Arial', 16))
            destination_time_label.grid(row=3, column=1, sticky="w")
            destination_time_label.bind("<Button-1>", lambda e, r=route: self.select_route(r))

            # Here is the corrected line with the default argument in the lambda function
            route_frame.bind("<Button-1>", lambda e, r=route: self.select_route(r))
            self.routes_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

            if route != route_data[-1]:  # Check if not the last route
                separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
                separator.pack(fill='x', padx=10, pady=5)

    def select_route(self, route):
        self.selected_route_label.configure(
            text=f"Selected Route: {route[0]}\nFrom: {route[1]} To: {route[2]}\nDeparture: {route[3]} Arrival: {route[4]}")

    def on_mousewheel(self, event):
        # The following factor 120 is typically used on Windows to normalize the event.delta.
        # On MacOS, you might need to use 1 instead of 120. For Linux, you will use the event.num.
        scroll_step = -1 * (event.delta // 120)
        self.routes_canvas.yview_scroll(scroll_step, "units")

    def add_scroll_by_dragging(self):
        self.canvas_last_y = 0
        self.canvas_scroll_start_y = 0

        self.routes_canvas.bind("<ButtonPress-1>", self.start_drag)
        self.routes_canvas.bind("<B1-Motion>", self.dragging)
        self.routes_canvas.bind("<ButtonRelease-1>", self.stop_drag)

    def start_drag(self, event):
        self.canvas_scroll_start_y = event.y
        self.canvas_last_y = event.y

    def dragging(self, event):
        delta_y = event.y - self.canvas_last_y
        self.routes_canvas.yview_scroll(int(-delta_y / 50),
                                        "units")  # The division factor can be adjusted for smoother scrolling
        self.canvas_last_y = event.y

    def stop_drag(self, event):
        self.canvas_last_y = 0
        self.canvas_scroll_start_y = 0

    # For Windows and MacOS
