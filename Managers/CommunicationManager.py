
import socket
import requests

from Managers.DatabaseManager import DatabaseManager

# the communication manager is used for communication between the GUI and the controller, it sends http requests to
# the server running on the controller to manage and control displayed text on the panels
class CommunicationManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise Exception("singleton instance exists")
        else:
            CommunicationManager._instance = self

        self.use_display_1 = False
        self.use_display_2 = False

    def get_display_usage(self):
        return self.use_display_1, self.use_display_2

    # method for sending route information when switching between stations
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


    # method for sending settings
    def send_settings(self, display_1, display_2, show_delay):
        url = 'http://127.0.0.1:5555/settings'
        db_manager = DatabaseManager()
        results = db_manager.get_settings()[0]
        payload = {
            "display_1": display_1,
            "display_2": display_2,
            "show_delay": show_delay,
            "brightness": results[2],
            "speed": results[3],
            "com_port": results[1]
        }

        self.use_display_1 = display_1
        self.use_display_2 = display_2

        response = requests.post(url, json=payload)
        print(response.json())

    # def send_emergency_message(self, message):
    #     url = 'http://127.0.0.1:5555/emergency'
    #     payload = {"message": message}
    #     response = requests.post(url, json=payload)
    #     print(response.json())


    # method for setting basic text messages that will be displayed on the panels

    def send_basic_message(self, message):
        url = 'http://127.0.0.1:5555/basic_message'
        payload = {"message": message}
        response = requests.post(url, json=payload)
        print(response.json())


    # http request to reset the panels to default state and text
    def reset_message(self):
        url = 'http://127.0.0.1:5555/reset_message'
        response = requests.post(url)
        print(response.json())

    # connectivity test of the controller
    def controller_connectivity_test(self):
        url = 'http://127.0.0.1:5555/controller_connectivity_test'
        try:
            response = requests.get(url)
            print(response.status_code)
            if response.status_code == 200:
                return True

        except:
            return False

    # internet connectivity test of the controller
    def controller_internet_connectivity_test(self):
        url = 'http://127.0.0.1:5555/controller_internet_connectivity_test'
        try:
            response = requests.get(url)
            print(response.status_code)
            if response.status_code == 200:
                return True
        except:
            return False


    # connectivity test of panel 1 - aesys
    def display_panel_1_test(self):
        url = 'http://127.0.0.1:5555/controller_display_panel_1_test'
        try:
            response = requests.get(url)
            print(response.status_code)
            if response.status_code == 200:
                return True
        except:
            return False

    # connectivity test of panel 2 - buse
    def display_panel_2_test(self):
        url = 'http://127.0.0.1:5555/controller_display_panel_2_test'
        try:
            response = requests.get(url)
            print(response.status_code)
            if response.status_code == 200:
                return True
        except:
            return False




