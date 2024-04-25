
import socket
import requests


class CommunicationManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CommunicationManager._instance = self

        self.use_display_1 = False
        self.use_display_2 = False

    def get_display_usage(self):
        return self.use_display_1, self.use_display_2

    def send_route_update(self, routeID, remaining_stations, destination_station, train_state, delay = 0):
        url = 'http://127.0.0.1:5555/route_update'
        payload = {
            "routeID": routeID,
            "remaining_route_stations": remaining_stations,
            "destination_station": destination_station,
            "state": train_state,
            "delay": delay,
            "display_1": self.use_display_1,
            "display_2": self.use_display_2
        }

        response = requests.post(url, json=payload)
        print(response.json())


    def send_settings(self, display_1, display_2, show_delay):
        url = 'http://127.0.0.1:5555/settings'
        payload = {
            "display_1": display_1,
            "display_2": display_2,
            "show_delay": show_delay
        }
        self.use_display_1 = display_1
        self.use_display_2 = display_2
        response = requests.post(url, json=payload)
        print(response.json())

    def send_emergency_message(self, message):
        url = 'http://127.0.0.1:5555/emergency'
        payload = {"message": message}
        response = requests.post(url, json=payload)
        print(response.json())

    def send_basic_message(self, message):
        url = 'http://127.0.0.1:5555/basic_message'
        payload = {"message": message}
        response = requests.post(url, json=payload)
        print(response.json())

    def reset_message(self):
        url = 'http://127.0.0.1:5555/reset_message'
        response = requests.post(url)
        print(response.json())

