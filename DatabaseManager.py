import psycopg2
from psycopg2 import OperationalError
import requests
import socket
import psycopg2
import time

class DatabaseManager:
    def __init__(self):
        self.conn = None

    def connection_test(self):
        try:
            # Attempt to establish a connection to the database
            self.conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
            cur = self.conn.cursor()
            cur.execute("SELECT 1")

            print("Connection to the database was successful.")
        except OperationalError as e:
            print(f"An error occurred: {e}")
            self.conn = None
        finally:
            if self.conn is None:
                print("Failed to connect to the database.")

    def get_connection(self):
        if self.conn is None:
            self.connection_test()
            if self.conn is not None:
                return self.conn
        return self.conn

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
            # conn.close()
            return trips
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

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
            print(f"An error occurred: {e}")
            return []

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
            print(f"An error occurred: {e}")
            return []


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
            print(f"An error occurred: {e}")
            return []



    # Function to check internet connectivity
    def check_internet(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            print(ex)
            return False

    # Function to update the database with coordinates
    def update_coordinates(self):
        # Establish a database connection
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
        except Exception as e:
            print(f"Database connection failed: {e}")
            return

        # Select rows where latitude or longitude is NULL
        cursor.execute("SELECT stop_id, name FROM stops WHERE latitude IS NULL OR longitude IS NULL;")
        stops = cursor.fetchall()

        for stop_id, name in stops:
            # Call the API
            response = requests.get(f"https://api.openrailwaymap.org/v2/facility?name={name}&limit=1")

            # If the API call is successful and returns data
            if response.status_code == 200 and response.json():
                data = response.json()[0]
                latitude = data.get('latitude')
                longitude = data.get('longitude')

                # Update the database row
                update_query = "UPDATE stops SET latitude = %s, longitude = %s WHERE stop_id = %s;"
                cursor.execute(update_query, (latitude, longitude, stop_id))
                conn.commit()
                print(f"Coordinates updated for {name}")

            else:
                print(f"Failed to get data for {name}")

            time.sleep(1)

        # Close the connection
        cursor.close()
        conn.close()

