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
    fs.name AS first_stop_name,
    ls.name AS last_stop_name,
    fst.arrival_time AS first_stop_time,
    lst.arrival_time AS last_stop_time
FROM
    trips t
JOIN
    routes r ON t.route_id = r.route_id
JOIN
    stops fs ON r.start_stop_id = fs.stop_id
JOIN
    stops ls ON r.end_stop_id = ls.stop_id
JOIN
    schedules fst ON fs.stop_id = fst.stop_id
JOIN
    schedules lst ON ls.stop_id = lst.stop_id
WHERE
    fst.trip_id = t.trip_id AND
    lst.trip_id = t.trip_id
ORDER BY
    t.trip_id, fst.arrival_time, lst.arrival_time;
            """
            cur.execute(query)
            routes = cur.fetchall()
            cur.close()
            # conn.close()
            return routes
        except Exception as e:
            print(f"An error occurred: {e}")
            return []




