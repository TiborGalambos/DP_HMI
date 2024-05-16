import datetime
import os
import customtkinter as ctk
from PIL import Image
from tkintermapview import osm_to_decimal

import io
import sys

import GLOBAL_VARS
from Managers.CommunicationManager import CommunicationManager
from Managers.DatabaseManager import DatabaseManager
import tkintermapview

class SubPage2(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.fourth_row_container = None
        self.delay_label = None
        self.stop_name3_label = None
        self.stop_name2_label = None
        self.stop_name1_label = None
        self.after_stop_label3 = None
        self.in_stop_label3 = None
        self.before_stop_label3 = None
        self.after_stop_label2 = None
        self.in_stop_label2 = None
        self.before_stop_label2 = None
        self.after_stop_label1 = None
        self.in_stop_label1 = None
        self.before_stop_label1 = None
        self.third_row_container = None
        self.second_row_container = None
        self.first_row_container = None
        self.down_button = None
        self.up_button = None
        self.path = None
        self.is_map_set = False
        self.controller = controller
        self.db_manager = DatabaseManager()
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.map_container = ctk.CTkFrame(self)
        self.map_container.grid(row=0, column=0, sticky="nwse", pady=20, padx=20)
        self.trip_stops_container = ctk.CTkFrame(self, fg_color="transparent")
        self.trip_stops_container.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        if hasattr(sys, '_MEIPASS'):
            base_path = os.path.join(sys._MEIPASS, "Pages")
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        bundled_path = os.path.join(base_path, "offline_map.db")
        working_dir = os.path.join(os.path.dirname(sys.executable), "Pages", "offline_map.db")

        if os.path.exists(bundled_path):
            self.database_path = bundled_path
        else:
            self.database_path = working_dir

        print("path:", self.database_path)

        self.map_widget = tkintermapview.TkinterMapView(self.map_container, width=1200, height=1190, corner_radius=30,
                                                        use_database_only=True,
                                                        database_path=self.database_path)
        self.map_widget.grid(sticky="news", row=0, column=0, ipadx=0, ipady=20)

        self.dbm = DatabaseManager()
        self.offline_map_db_path = self.database_path
        self.current_stop_seq = 0

        self.trip_coords = []
        self.trip_stops = []
        self.trip_stop_times = []

        # default position on map
        self.map_widget.set_position(43.19781111111, 17.306139)
        self.stops_box_position = 1

    def set_map_markers(self):

        for name, x, y, time in self.dbm.fetch_trip_stop_times_with_coords(GLOBAL_VARS.active_trip_id):
            marker = self.map_widget.set_marker(float(x), float(y))

            self.trip_coords.append((float(x), float(y)))
            self.trip_stops.append(name)
            self.trip_stop_times.append(time)

        self.path = self.map_widget.set_path(self.trip_coords)
        self.is_map_set = True
        self.set_stops_and_times()

    def unset_map_markers(self):

        self.path.delete()
        self.is_map_set = False

        self.trip_coords = []
        self.trip_stops = []
        self.trip_stop_times = []

        self.map_widget.delete_all_marker()
        self.first_row_container.destroy()
        self.second_row_container.destroy()
        self.third_row_container.destroy()
        self.up_button.destroy()
        self.down_button.destroy()

        self.current_stop_seq = 0
        self.stops_box_position = 1
        self.delay_label.configure(text="")


    def set_stops_and_times(self):

        base_path = os.path.dirname(os.path.abspath(__file__))
        icons_path = os.path.join(base_path, "icons", "arrows")

        self.trip_stops_container.grid_columnconfigure(0, weight=1)
        self.trip_stops_container.grid_columnconfigure(1, weight=1)

        arrow_down = Image.open(os.path.join(icons_path, "arrow_down.png"))
        arrow_down = arrow_down.resize((25, 25),
                                       Image.Resampling.LANCZOS)
        arrow_down_icon = ctk.CTkImage(arrow_down, size=(25, 25))

        arrow_up = Image.open(os.path.join(icons_path, "arrow_up.png"))
        arrow_up = arrow_up.resize((100, 100),
                                   Image.Resampling.LANCZOS)
        arrow_up_icon = ctk.CTkImage(arrow_up)

        self.up_button = ctk.CTkButton(self.trip_stops_container, text='', command=self.scroll_up, width=20, image=arrow_up_icon)
        self.down_button = ctk.CTkButton(self.trip_stops_container, text='', command=self.scroll_down, width=20, image=arrow_down_icon)

        self.first_row_container = ctk.CTkFrame(self.trip_stops_container, width =800)
        self.second_row_container = ctk.CTkFrame(self.trip_stops_container, width =800)
        self.third_row_container = ctk.CTkFrame(self.trip_stops_container, width =800)
        self.fourth_row_container = ctk.CTkFrame(self.trip_stops_container, width=800, fg_color="transparent")

        self.first_row_container.grid(row=0, column=0, sticky='nwse', ipadx=30, ipady=20, pady=(0, 10))
        self.second_row_container.grid(row=1, column=0, sticky='nwse', ipadx=30, ipady=20, pady=(0, 10))
        self.third_row_container.grid(row=2, column=0, sticky='nwse', ipadx=30, ipady=20, pady=0)
        self.fourth_row_container.grid(row=3, column= 0, sticky='s', ipadx=30)


        self.first_row_container.grid_columnconfigure(0, weight=1)
        self.first_row_container.grid_columnconfigure(1, weight=3)

        self.second_row_container.grid_columnconfigure(0, weight=1)
        self.second_row_container.grid_columnconfigure(1, weight=3)

        self.third_row_container.grid_columnconfigure(0, weight=1)
        self.third_row_container.grid_columnconfigure(1, weight=3)

        self.fourth_row_container.grid_columnconfigure(0, weight=1)

        for i in range (3):
            self.first_row_container.grid_rowconfigure(i, weight=1)
            self.second_row_container.grid_rowconfigure(i, weight=1)
            self.third_row_container.grid_rowconfigure(i, weight=1)

        self.fourth_row_container.grid_rowconfigure(0, weight=1)


        self.before_stop_label1 = ctk.CTkLabel(self.first_row_container, text="Príchod", font=('Arial', 18, 'bold'), text_color='green')
        self.in_stop_label1 = ctk.CTkLabel(self.first_row_container, text="V zastávke")
        self.after_stop_label1 = ctk.CTkLabel(self.first_row_container, text="Odchod")

        self.before_stop_label1.grid(row=0, column=1, sticky='nes', padx=(0, 50), pady=(20,0))
        self.in_stop_label1.grid(row=1, column=1, sticky='nes', padx=(0, 50))
        self.after_stop_label1.grid(row=2, column=1, sticky='nes', padx=(0, 50), pady=(0,20))


        self.before_stop_label2 = ctk.CTkLabel(self.second_row_container, text="Príchod")
        self.in_stop_label2 = ctk.CTkLabel(self.second_row_container, text="V zastávke")
        self.after_stop_label2 = ctk.CTkLabel(self.second_row_container, text="Odchod")

        self.before_stop_label2.grid(row=0, column=1, sticky='nes', padx=(0, 50), pady=(20,0))
        self.in_stop_label2.grid(row=1, column=1, sticky='nes', padx=(0, 50))
        self.after_stop_label2.grid(row=2, column=1, sticky='nes', padx=(0, 50), pady=(0,20))


        self.before_stop_label3 = ctk.CTkLabel(self.third_row_container, text="Príchod")
        self.in_stop_label3 = ctk.CTkLabel(self.third_row_container, text="V zastávke")
        self.after_stop_label3 = ctk.CTkLabel(self.third_row_container, text="Odchod")

        self.before_stop_label3.grid(row=0, column=1, sticky='nes', padx=(0, 50), pady=(20,0))
        self.in_stop_label3.grid(row=1, column=1, sticky='nes', padx=(0, 50))
        self.after_stop_label3.grid(row=2, column=1, sticky='nes', padx=(0, 50), pady=(0,20))

        self.stop_name1_label = ctk.CTkLabel(self.first_row_container, text='1.', font=('Arial', 35, 'bold'))
        self.stop_name2_label = ctk.CTkLabel(self.second_row_container, text='2.', font=('Arial', 25))
        self.stop_name3_label = ctk.CTkLabel(self.third_row_container, text='3.', font=('Arial', 25))

        self.stop_name1_label.grid(row=0, column=0, rowspan=3, pady = 100, padx = 10, sticky='nws')
        self.stop_name2_label.grid(row=0, column=0, rowspan=3, pady = 100, padx = 10, sticky='nws')
        self.stop_name3_label.grid(row=0, column=0, rowspan=3, pady = 100, padx = 10, sticky='nws')

        self.up_button.grid(row=0, column=1, sticky='swne', padx=10)
        self.down_button.grid(row=2, column=1, sticky='wsne', padx=10)

        self.first_row_container.grid_propagate(False)

        self.current_stop_seq = 0

        self.stop_name1_label.configure(text=f'1. {self.trip_stops[self.current_stop_seq]}')
        self.stop_name2_label.configure(text=f'2. {self.trip_stops[self.current_stop_seq+1]}')
        self.stop_name3_label.configure(text=f'3. {self.trip_stops[self.current_stop_seq+2]}')

        self.in_stop_label1.configure(text=f'{self.trip_stop_times[self.current_stop_seq]}')
        self.in_stop_label2.configure(text=f'{self.trip_stop_times[self.current_stop_seq + 1]}')
        self.in_stop_label3.configure(text=f'{self.trip_stop_times[self.current_stop_seq + 2]}')

        self.delay_label = ctk.CTkLabel(self.fourth_row_container, text='Aktuálne meškanie vlaku: 0 min.', font=('Arial', 20))
        self.delay_label.grid(row=0, column=0, sticky='nw', padx=10, pady=(25,10))

        communication = CommunicationManager.get_instance()
        communication.send_route_update(routeID=GLOBAL_VARS.selected_trip_name,
                                        train_state='before_station',
                                        remaining_stations=self.trip_stops,
                                        destination_station=self.trip_stops[-1])

        self.update_map_position()

    # Update the position when the station changes
    def update_map_position(self):
        loader = tkintermapview.OfflineLoader(path=self.offline_map_db_path)

        self.map_widget.set_position(self.trip_coords[self.current_stop_seq][0],
                                     self.trip_coords[self.current_stop_seq][1])
        self.map_widget.set_marker(self.trip_coords[self.current_stop_seq][0],
                                     self.trip_coords[self.current_stop_seq][1],
                                   text=self.trip_stops[self.current_stop_seq], font=('Arial', 40))
        self.offline_map_controller(loader)

    # Getting the tile of the station, if not available. Usage in case when new stations were added.
    def offline_map_controller(self, loader):
        current_position = self.map_widget.get_position()
        top_left_corner_of_map = osm_to_decimal(self.map_widget.upper_left_tile_pos[0],
                                         self.map_widget.upper_left_tile_pos[1], round(self.map_widget.zoom))
        bottom_right_corner_of_map = osm_to_decimal(self.map_widget.lower_right_tile_pos[0],
                                          self.map_widget.lower_right_tile_pos[1], round(self.map_widget.zoom))

        # temporarily redirect the input, to get the loaded section
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        loader.print_loaded_sections()
        sys.stdout = old_stdout
        tiles = new_stdout.getvalue()

        # using zoom 17 for download
        if not str(bottom_right_corner_of_map) + '\', 17, 17,' in tiles:
            print("The tile is not in db, so checking internet connection.")
            if DatabaseManager().check_internet():
                print("Internet connection available, downloading the tile")
                loader.save_offline_tiles(top_left_corner_of_map, bottom_right_corner_of_map, 17, 17)
            else:
                print("No internet connection.")

    # Method to handle scrolling up in the currently displayed stops.
    def scroll_up(self):

        communication = CommunicationManager.get_instance()

        if self.current_stop_seq == 1:
            # moving from second to first item
            self.stop_name1_label.configure(font=('Arial', 35, 'bold'))
            self.stop_name2_label.configure(font=('Arial', 20))
            self.current_stop_seq -= 1

            self.stops_box_position = 1

            self.before_stop_label2.configure(font=('Arial', 12), text_color='white')
            self.in_stop_label2.configure(font=('Arial', 12), text_color='white')
            self.after_stop_label2.configure(font=('Arial', 12), text_color='white')

            self.before_stop_label1.configure(font=('Arial', 18, 'bold'), text_color='green')

            print(f'1up {self.current_stop_seq}')

            communication.send_route_update(routeID=GLOBAL_VARS.selected_trip_name,
                                            train_state='before_station',
                                            remaining_stations=self.trip_stops[self.current_stop_seq:],
                                            destination_station=self.trip_stops[-1])


        elif self.current_stop_seq == len(self.trip_stops) - 1:
            # at the last item
            self.stop_name2_label.configure(font=('Arial', 35, 'bold'))
            self.stop_name3_label.configure(font=('Arial', 20))

            self.current_stop_seq -= 1
            self.stops_box_position = 1

            self.before_stop_label3.configure(font=('Arial', 12), text_color='white')
            self.in_stop_label3.configure(font=('Arial', 12), text_color='white')
            self.after_stop_label3.configure(font=('Arial', 12), text_color='white')

            self.in_stop_label2.configure(font=('Arial', 12), text_color='white')
            self.after_stop_label2.configure(font=('Arial', 12), text_color='white')

            self.before_stop_label2.configure(font=('Arial', 18, 'bold'), text_color='green')

            print(f'2up {self.current_stop_seq}')

            communication.send_route_update(routeID=GLOBAL_VARS.selected_trip_name,
                                            train_state='before_station',
                                            remaining_stations=self.trip_stops[self.current_stop_seq:],
                                            destination_station=self.trip_stops[-1])

        elif self.current_stop_seq > 1:
            self.stops_box_position = 1

            self.before_stop_label3.configure(font=('Arial', 12), text_color='white')
            self.in_stop_label3.configure(font=('Arial', 12), text_color='white')
            self.after_stop_label3.configure(font=('Arial', 12), text_color='white')

            self.before_stop_label2.configure(font=('Arial', 18, 'bold'), text_color='green')
            self.in_stop_label2.configure(font=('Arial', 12), text_color='white')
            self.after_stop_label2.configure(font=('Arial', 12), text_color='white')

            self.current_stop_seq -= 1
            self.update_stop_labels()

            print(f'3up {self.current_stop_seq}')

            communication.send_route_update(routeID=GLOBAL_VARS.selected_trip_name,
                                            train_state='before_station',
                                            remaining_stations=self.trip_stops[self.current_stop_seq:],
                                            destination_station=self.trip_stops[-1])

        self.update_map_position()

    # Method for handling scrolling down in the currently displayed stops.
    def scroll_down(self):

        communication = CommunicationManager.get_instance()

        if self.stops_box_position == 1 and self.current_stop_seq == 0:
            self.before_stop_label1.configure(font=('Arial', 12), text_color='white')
            self.in_stop_label1.configure(font=('Arial', 18, 'bold'), text_color='green')
            self.stops_box_position += 1
            print('1 if')

        elif self.stops_box_position == 2 and self.current_stop_seq == 0:
            self.in_stop_label1.configure(font=('Arial', 12), text_color='white')
            self.after_stop_label1.configure(font=('Arial', 18, 'bold'), text_color='green')
            self.stops_box_position += 1
            print('2 if')

        elif self.stops_box_position == 3 and self.current_stop_seq == 0:
            self.stop_name1_label.configure(font=('Arial', 20))
            self.stop_name2_label.configure(font=('Arial', 35, 'bold'))

            self.after_stop_label1.configure(font=('Arial', 12), text_color='white')
            self.stops_box_position = 4
            self.current_stop_seq += 1
            self.before_stop_label2.configure(font=('Arial', 18, 'bold'), text_color='green')
            print('3 if')

        elif self.stops_box_position == 1 and 0 < self.current_stop_seq < len(self.trip_stops) -1 :
            self.before_stop_label2.configure(font=('Arial', 12), text_color='white')
            self.in_stop_label2.configure(font=('Arial', 18, 'bold'), text_color='green')
            self.stops_box_position += 1
            print('4 if')

        elif self.stops_box_position == 2 and 0 < self.current_stop_seq < len(self.trip_stops) -1 :
            self.in_stop_label2.configure(font=('Arial', 12), text_color='white')
            self.after_stop_label2.configure(font=('Arial', 18, 'bold'), text_color='green')
            self.stops_box_position += 1
            print('5 if')

        elif self.stops_box_position == 3 and 0 < self.current_stop_seq < len(self.trip_stops) -1 :

            self.after_stop_label2.configure(font=('Arial', 12), text_color='white')
            self.before_stop_label2.configure(font=('Arial', 18, 'bold'), text_color='green')
            self.stops_box_position += 1
            self.current_stop_seq += 1
            if self.current_stop_seq < len(self.trip_stops) -1:
                self.update_stop_labels()
            if self.current_stop_seq == 2:
                self.before_stop_label1.configure(text='Na ceste')
            print('6 if')

        if self.stops_box_position == 4 and self.current_stop_seq == len(self.trip_stops) -1 :
            self.stop_name2_label.configure(font=('Arial', 20))
            self.stop_name3_label.configure(font=('Arial', 35, 'bold'))

            self.before_stop_label2.configure(font=('Arial', 12), text_color='white')
            self.after_stop_label2.configure(font=('Arial', 12), text_color='white')
            self.before_stop_label3.configure(font=('Arial', 18, 'bold'), text_color='green')
            print('7 if')

        elif self.stops_box_position == 1 and self.current_stop_seq == len(self.trip_stops) -1 :
            self.before_stop_label3.configure(font=('Arial', 12), text_color='white')
            self.in_stop_label3.configure(font=('Arial', 18, 'bold'), text_color='green')
            self.stops_box_position += 1
            print('8 if')

        elif self.stops_box_position == 2 and self.current_stop_seq == len(self.trip_stops) -1 :
            self.in_stop_label3.configure(font=('Arial', 12), text_color='white')
            self.after_stop_label3.configure(font=('Arial', 18, 'bold'), text_color='green')
            self.stops_box_position += 1
            print('9 if')

        if self.stops_box_position == 4:
            self.stops_box_position = 1
            self.update_map_position()

        if self.stops_box_position == 1:
            train_state = "before_station"

        delay = 0

        if self.stops_box_position == 2:
            scheduled = self.trip_stop_times[self.current_stop_seq]
            actual = datetime.datetime.now().time()

            delay = ((datetime.datetime.combine(datetime.date.today(), actual) -
                      datetime.datetime.combine(datetime.date.today(), scheduled)).total_seconds() / 60)

            print("delay ", delay)
            print("actual, scheduled:  ", actual, scheduled)

            if delay >= 0:
                delay_int = int(max(0, delay))
                self.delay_label.configure(text=f"Aktuálne meškanie vlaku: {delay_int} min.")
            else:
                self.delay_label.configure(text=f"Do odchodu ostáva: {int(abs(delay))} min.")

            train_state = "in_station"

        if self.stops_box_position == 3:
            train_state = "after_station"

        # send the update to the display controller
        communication.send_route_update(routeID=GLOBAL_VARS.selected_trip_name,
                                        train_state=train_state,
                                        remaining_stations=self.trip_stops[self.current_stop_seq:],
                                        destination_station=self.trip_stops[-1],
                                        delay=int(delay))

        print(self.current_stop_seq)
        print(self.stops_box_position)

    # Method to update the stop labels of the currently displayed trip stops - max 3 at a time
    def update_stop_labels(self):

        self.in_stop_label1.configure(text=f'{self.trip_stop_times[self.current_stop_seq -1]}')
        self.in_stop_label2.configure(text=f'{self.trip_stop_times[self.current_stop_seq + 0]}')
        self.in_stop_label3.configure(text=f'{self.trip_stop_times[self.current_stop_seq + 1]}')

        self.stop_name1_label.configure(
            text=f'{self.current_stop_seq}. {self.trip_stops[self.current_stop_seq - 1]}')
        self.stop_name2_label.configure(
            text=f'{self.current_stop_seq + 1}. {self.trip_stops[self.current_stop_seq + 0]}')
        self.stop_name3_label.configure(
            text=f'{self.current_stop_seq + 2}. {self.trip_stops[self.current_stop_seq + 1]}')



