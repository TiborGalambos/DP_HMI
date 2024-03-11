import socket
# import tkinter as tk
import xml.etree.ElementTree as ET

from AppMainLayout import AppMainLayout

# from AppMainLayout import AppMainLayout

HOST = 'localhost'
PORT = 65432
home_route_button = None
import psycopg2

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='localhost'  # or another hostname if your db is not on your local machine
)



def fetch_stops_for_route(trip_name):
    try:
        cursor = conn.cursor()
        query = """
        SELECT
            s.name,
            sch.arrival_time
        FROM
            Schedules sch
            JOIN Stops s ON sch.stop_id = s.stop_id
            JOIN Trips t ON sch.trip_id = t.trip_id
        WHERE
            t.trip_name = %s
        ORDER BY
            sch.arrival_time;
        """
        cursor.execute(query, (trip_name,))
        stops = cursor.fetchall()
        cursor.close()
        return stops
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def fetch_routes():
    try:
        cursor = conn.cursor()
        query = """
        SELECT
            t.trip_name,
            first_stop.name AS start_stop,
            last_stop.name AS end_stop,
            first_schedule.arrival_time AS start_arrival_time,
            last_schedule.arrival_time AS end_arrival_time
        FROM
            Trips t
        LEFT JOIN LATERAL (
            SELECT
                s.stop_id,
                sch.arrival_time
            FROM
                Schedules sch
            JOIN
                Stops s ON sch.stop_id = s.stop_id
            WHERE
                sch.trip_id = t.trip_id
            ORDER BY
                sch.arrival_time
            LIMIT 1
        ) first_schedule ON TRUE
        LEFT JOIN Stops first_stop ON first_schedule.stop_id = first_stop.stop_id
        LEFT JOIN LATERAL (
            SELECT
                s.stop_id,
                sch.arrival_time
            FROM
                Schedules sch
            JOIN
                Stops s ON sch.stop_id = s.stop_id
            WHERE
                sch.trip_id = t.trip_id
            ORDER BY
                sch.arrival_time DESC
            LIMIT 1
        ) last_schedule ON TRUE
        LEFT JOIN Stops last_stop ON last_schedule.stop_id = last_stop.stop_id;
        """
        cursor.execute(query)
        routes = cursor.fetchall()
        cursor.close()
        conn.close()
        return routes
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def print_stops(stops):
    for stop, time in stops:
        # Example processing: print each stop and time
        print(f"Stop: {stop}, Time: {time.strftime('%H:%M')}")


def create_xml_message(stops):
    root = ET.Element('stops')
    for stop, time in stops:
        stop_element = ET.SubElement(root, 'stop')
        stop_element.set('name', stop)
        stop_element.set('time', time.strftime('%H:%M'))
    return ET.tostring(root, encoding='utf8', method='xml')


def send_message_all_stops(stops):
    xml_message = create_xml_message(stops)
    print(xml_message)  # For demonstration purposes
    with socket.create_connection((HOST, PORT)) as sock:
        sock.sendall(xml_message)  # xml_message is already a bytes object


def route_selected(trip_name, route_window):
    global route_button
    print(f"Selected route: {trip_name}")
    # Here you can fetch and display stops for the selected route or send a message as needed

    route_window.destroy()  # Close the current route selection window

    if home_route_button:  # Check if the first button has been initialized
        home_route_button.configure(text=f"Selected: {trip_name}")  # Update the first button's text

    stops = fetch_stops_for_route(trip_name)

    print_stops(stops)
    send_message_all_stops(stops)


def create_route_buttons(routes):
    global home_route_button  # Reference the global variable

    route_window = tk.Tk()
    route_window.title("Select a Route")

    for index, route in enumerate(routes):
        trip_name, start_stop, end_stop, start_time, end_time = route
        btn_text = f"{trip_name}: {start_stop} to {end_stop}"
        btn_command = lambda tn=trip_name, rw=route_window: route_selected(tn, rw)

        if index == 0:  # For the first button, store its reference globally
            route_button = tk.Button(route_window, text=btn_text, height=2, width=30, command=btn_command)
            route_button.pack(pady=10)
        else:
            btn = tk.Button(route_window, text=btn_text, height=2, width=30, command=btn_command)
            btn.pack(pady=10)

    route_window.mainloop()


def pick_route():
    routes = fetch_routes()
    create_route_buttons(routes)

    # send_message(route)


def dummy_action():
    # Placeholder function for dummy buttons
    print("Dummy action")

import customtkinter as ckt

if __name__ == "__main__":
    app = AppMainLayout()
    app.mainloop()

    print()

# if __name__ == "__main__":
#     conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
#     cur = conn.cursor()
#
#     # Initialize the main Tkinter window
#     root = tk.Tk()
#     root.title("HMI Interface")
#     root.geometry("400x300")  # Adjust the size of the main window
#
#     # Create the route picker button on the main window
#     home_route_button = tk.Button(root, text="Pick a Route", height=3, width=20, command=pick_route)
#     home_route_button.pack(pady=10)  # Add some padding for visual separation
#
#     # Create three dummy buttons on the main window
#     for i in range(1, 4):
#         dummy_button = tk.Button(root, text=f"Dummy Button {i}", height=3, width=20, command=dummy_action)
#         dummy_button.pack(pady=10)
#
#     root.mainloop()

