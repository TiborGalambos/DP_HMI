import socket
import tkinter as tk
from tkinter import simpledialog
import xml.etree.ElementTree as ET

HOST = 'localhost'
PORT = 65432
route_button = None
import psycopg2

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='localhost'  # or another hostname if your db is not on your local machine
)


def create_xml_message(route):
    # Create the root element
    root = ET.Element("data")

    # Create a child element
    message = ET.SubElement(root, "route")
    message.text = f"{route}"

    # Convert the XML tree to a string
    xml_str = ET.tostring(root, encoding='utf8', method='xml')
    return xml_str


def send_message(route):
    xml_message = create_xml_message(route)
    with socket.create_connection((HOST, PORT)) as sock:
        sock.sendall(xml_message)


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
        # conn.close()
        return routes
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def route_selected(trip_name, route_window):
    global route_button  # Reference the global variable

    print(f"Selected route: {trip_name}")
    # Here you can fetch and display stops for the selected route or send a message as needed

    route_window.destroy()  # Close the current route selection window

    if route_button:  # Check if the first button has been initialized
        route_button.config(text=f"Selected: {trip_name}")  # Update the first button's text

def create_route_buttons(routes):
    global route_button  # Reference the global variable

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

if __name__ == "__main__":

    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()


    # Initialize the main Tkinter window
    root = tk.Tk()
    root.title("HMI Interface")
    root.geometry("400x300")  # Adjust the size of the main window

    # Create the route picker button on the main window
    route_button = tk.Button(root, text="Pick a Route", height=3, width=20, command=pick_route)
    route_button.pack(pady=10)  # Add some padding for visual separation

    # Create three dummy buttons on the main window
    for i in range(1, 4):
        dummy_button = tk.Button(root, text=f"Dummy Button {i}", height=3, width=20, command=dummy_action)
        dummy_button.pack(pady=10)

    root.mainloop()
