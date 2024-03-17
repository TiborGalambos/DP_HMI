import psycopg2
from psycopg2 import OperationalError

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




