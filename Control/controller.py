from datetime import datetime

from Control.aesys_controller import AesysController
from Control.buse_controller import BuseController

buse = BuseController()
aesys = AesysController()

class Controller:
    _instance = None

    display1 = True
    display2 = True
    com_port = 3
    delay_between_updates = 2
    speed = 4
    brightness = 0
    show_delay = True

    @classmethod
    def display_route(cls, data):
        routeID = data.get('routeID')
        remaining_stations = data.get('remaining_route_stations')
        destination_station = data.get('destination_station')
        train_state = data.get('state')
        train_delay = data.get('delay')

        print(train_state)

        if train_state == "before_station":
            buse.start_display_before_station(destination_station, cls.delay_between_updates)
            aesys.start_display_before_station(destination_station, cls.speed, cls.brightness)

        if train_state == "in_station":
            buse.start_display_in_station(routeID, destination_station, remaining_stations, train_delay, cls.delay_between_updates)
            aesys.start_display_in_station(routeID, destination_station, remaining_stations, train_delay, cls.speed, cls.brightness)

        if train_state == "after_station":
            buse.start_display_after_station(routeID, destination_station, cls.delay_between_updates)
            aesys.start_display_after_station(routeID, destination_station, cls.speed, cls.brightness)


    @classmethod
    def reset(cls):
        current_date = datetime.now()
        date_str = current_date.strftime("%d.%m.%Y")
        buse.start_display_simple_message(date_str, cls.delay_between_updates)
        aesys.reset()

        aesys.start_display_simple_message(date_str)

    @classmethod
    def set_settings(cls, display_1, display2, com_port, speed, brightness, show_delay):
        cls.display1 = display_1
        cls.display2 = display2
        cls.com_port = com_port
        cls.speed = speed
        cls.delay_between_updates = 6 - speed
        cls.brightness = brightness
        cls.show_delay = show_delay

        buse.set_com_port(cls.com_port)

        print("from controller:")
        print(cls.display1, cls.display2, cls.speed, cls.brightness, cls.com_port, cls.show_delay, cls.delay_between_updates)


    @classmethod
    def display_message(cls, message):
        buse.start_display_simple_message(message, cls.delay_between_updates)
        aesys.start_display_simple_message(message)

    @classmethod
    def test_ethernet_panel_connectivity(cls):
        return aesys.test_connectivity()

    @classmethod
    def test_ibis_panel_connectivity(cls):
        return buse.test_connectivity()