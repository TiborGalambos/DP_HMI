import psycopg2
from psycopg2 import OperationalError
import requests
import socket
import psycopg2
import time

# Database manager is used for querying the database.
# This class has methods that ensure the needs of gui are met in terms of accessing data from the database.
class DatabaseManager:
    def __init__(self):
        self.conn = None

    # Connectivity test to database
    def connection_test(self):
        try:
            self.conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
            cur = self.conn.cursor()
            cur.execute("SELECT 1")

            print("Database connection successful")
        except OperationalError as e:
            print(f"Error: {e}")
            self.conn = None
        finally:
            if self.conn is None:
                print("Database connection failed")


    # Method returns connection to db.
    def get_connection(self):
        if self.conn is None:
            self.connection_test()
            if self.conn is not None:
                return self.conn
        return self.conn


    # Method for initial route fetch
    def fetch_routes(self):
        try:

            conn = self.get_connection()
            cur = conn.cursor()
            query = """
            SELECT 
                r.route_id,
                ss.name AS start_stop_name,
                es.name AS end_stop_name
            FROM 
                routes r
            JOIN 
                stops ss ON r.start_stop_id = ss.stop_id
            JOIN 
                stops es ON r.end_stop_id = es.stop_id
            ORDER BY 
                ss.name;
            """
            cur.execute(query)
            trips = cur.fetchall()
            cur.close()
            return trips
        except Exception as e:
            print(f"Error: {e}")
            return []

    # Method that fetches trips by route id used to fill the table.
    def fetch_trip_by_route_id(self, route_id):
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            query = """
            SELECT
                trip_id,
                trip_name
            FROM
                trips
            WHERE
                route_id = %s;
            """

            cur.execute(query, (route_id,))
            routes = cur.fetchall()
            cur.close()
            return routes
        except Exception as e:
            print(f"Error: {e}")
            return []


    # Method for fetching stop times of selected trip.
    def fetch_trip_stop_times(self, trip_id):
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            query = """
            SELECT
                s.name AS stop_name,
                sch.arrival_time
            FROM
                Schedules sch
            JOIN
                Trips t ON sch.trip_id = t.trip_id
            JOIN
                Stops s ON sch.stop_id = s.stop_id
            WHERE
                t.trip_id = %s
            ORDER BY
                sch.arrival_time;
                        """

            cur.execute(query, (trip_id,))
            routes = cur.fetchall()
            cur.close()
            return routes
        except Exception as e:
            print(f"Error: {e}")
            return []


    # Method for fetching stop times with coords of selected trip.
    def fetch_trip_stop_times_with_coords(self, trip_id):
        try:
            conn = self.get_connection()
            cur = conn.cursor()

            query = """
            SELECT
                s.name AS stop_name,
                s.longitude AS longitude,
                s.latitude AS latitude,
                sch.arrival_time
            FROM
                Schedules sch
            JOIN
                Trips t ON sch.trip_id = t.trip_id
            JOIN
                Stops s ON sch.stop_id = s.stop_id
            WHERE
                t.trip_id = %s
            ORDER BY
                sch.arrival_time;
                        """

            cur.execute(query, (trip_id,))
            routes = cur.fetchall()
            cur.close()
            return routes
        except Exception as e:
            print(f"Error: {e}")
            return []


    # Method to check internet connectivity.
    def check_internet(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as e:
            print(e)
            return False

    # Method to update the coordinates in the database by open railway map api.
    # Used occasionally by running 'coordinates_update.py'.
    def update_coordinates(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
        except Exception as e:
            print(f"Database connection failed: {e}")
            return

        cursor.execute("SELECT stop_id, name FROM stops WHERE latitude IS NULL OR longitude IS NULL;")
        stops = cursor.fetchall()

        for stop_id, name in stops:
            response = requests.get(f"https://api.openrailwaymap.org/v2/facility?name={name}&limit=1")

            if response.status_code == 200 and response.json():
                data = response.json()[0]
                latitude = data.get('latitude')
                longitude = data.get('longitude')

                update_query = "UPDATE stops SET latitude = %s, longitude = %s WHERE stop_id = %s;"
                cursor.execute(update_query, (latitude, longitude, stop_id))
                conn.commit()
                print(f"Coords updated for {name}")

            else:
                print(f"Failed coords updated for {name}")

            # Sleep needed, as the open api cannot be commercially used, so there is a not specified rate limit.
            # You would maybe need to increase the sleep or run the py file multiple times to ensure you updated
            # every coordinate.
            time.sleep(3)

        cursor.close()

    def get_settings(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM application_settings"
            cursor.execute(query)
            records = cursor.fetchall()
            for record in records:
                print("theme:", record[0], "panel2 port number:", record[1], "panel1 brightness:",
                      record[2], "display speed:", record[3])
            cursor.close()
            return records

        except Exception as e:
            print("Error:", e)


    # Updating the settings will also update the database.
    def update_setting(self, theme, panel2_port_number, panel1_brightness, display_speed):

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = """
            UPDATE application_settings
            SET theme = %s, panel2_port_number = %s, panel1_brightness = %s, display_speed = %s
            WHERE id = 1;
            """
            data = (theme, panel2_port_number, panel1_brightness, display_speed)
            print("printing data from db manager")
            print(data)
            cursor.execute(query, data)
            conn.commit()

            if cursor.rowcount == 0:
                print("Fail")
            else:
                print("Update was successful")
            cursor.close()

        except Exception as e:
            print("Error:", e)
