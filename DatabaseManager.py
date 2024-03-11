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
            cur.execute(query)
            routes = cur.fetchall()
            cur.close()
            # conn.close()
            return routes
        except Exception as e:
            print(f"An error occurred: {e}")
            return []




