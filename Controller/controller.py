from datetime import datetime

from Controller.aesys_controller import AesysController
from Controller.buse_controller import BuseController
from celery import Celery
buse = BuseController()
aesys = AesysController()

app = Celery('tasks', broker='pyamqp://guest@localhost//')

class Controller:
    _instance = None

    display1 = True
    display2 = True
    com_port = 3
    delay_between_updates = 2
    speed = "4"
    brightness = "0"
    show_delay = True

    @classmethod
    @app.task
    def display_route(cls, data):
        routeID = data.get('routeID')
        remaining_stations = data.get('remaining_route_stations')
        destination_station = data.get('destination_station')
        train_state = data.get('state')
        train_delay = data.get('delay')
        cls.display1 = data.get('display_1')
        cls.display2 = data.get('display_2')

        print(train_state)

        if train_state == "before_station":
            if cls.display1:
                aesys.start_display_before_station(destination_station, cls.speed, cls.brightness)
            if cls.display2:
                buse.start_display_before_station(destination_station, cls.delay_between_updates)


        if train_state == "in_station":
            if cls.display1:
                aesys.start_display_in_station(routeID, destination_station, remaining_stations, train_delay, cls.speed, cls.brightness, cls.show_delay)
            if cls.display2:
                buse.start_display_in_station(routeID, destination_station, remaining_stations, train_delay, cls.delay_between_updates, cls.show_delay)


        if train_state == "after_station":
            if cls.display1:
                aesys.start_display_after_station(routeID, destination_station, cls.speed, cls.brightness)
            if cls.display2:
                buse.start_display_after_station(routeID, destination_station, cls.delay_between_updates)


    @classmethod
    @app.task
    def reset(cls):
        current_date = datetime.now()
        date_str = current_date.strftime("%d.%m.%Y")
        buse.start_display_simple_message(date_str, cls.delay_between_updates)
        aesys.reset()

        aesys.start_display_simple_message(date_str)


    @classmethod
    @app.task
    def set_settings(cls, display_1, display2, com_port, speed, brightness, show_delay):
        cls.display1 = display_1
        cls.display2 = display2
        cls.com_port = f"COM{com_port}"
        cls.speed = str(speed)
        cls.delay_between_updates = 6 - speed
        cls.brightness = str(brightness)
        cls.show_delay = show_delay

        buse.set_com_port(cls.com_port)

        print("from controller:")
        print(cls.display1, cls.display2, cls.speed, cls.brightness, cls.com_port, cls.show_delay, cls.delay_between_updates)


    @classmethod
    @app.task
    def display_message(cls, message):
        buse.start_display_simple_message(message, cls.delay_between_updates)
        aesys.start_display_simple_message(message)

    @classmethod
    @app.task
    def display_emergency(cls, message):
        buse.start_display_simple_message(message, cls.delay_between_updates)
        aesys.start_display_emergency_message(message)


    @classmethod
    @app.task
    def test_ethernet_panel_connectivity(cls):
        return aesys.test_connectivity()


    @classmethod
    @app.task
    def test_ibis_panel_connectivity(cls):
        return buse.test_connectivity()