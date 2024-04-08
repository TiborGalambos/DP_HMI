import threading

from flask import Flask, request, jsonify

app = Flask(__name__)

class Controller:

    use_display_1 = False
    use_display_2 = False

    show_delays = False
    @staticmethod
    @app.route('/route_update', methods=['POST'])
    def route_update():
        data = request.json
        # Process the route update data
        print(data)

        Controller.display_data(data, Controller.use_display_1, Controller.use_display_2, Controller.show_delays)

        return jsonify({"status": "success", "message": "Route update received"}), 200

    @staticmethod
    @app.route('/settings', methods=['POST'])
    def update_settings():
        settings = request.json
        print(settings)
        Controller.use_display_1 = bool(settings.get("display_1"))
        Controller.use_display_2 = bool(settings.get("display_2"))

        print(Controller.use_display_1, Controller.use_display_2)
        return jsonify({"status": "success", "message": "Settings updated"}), 200

    @staticmethod
    @app.route('/emergency', methods=['POST'])
    def emergency_message():
        message = request.json
        print(message)

        return jsonify({"status": "success", "message": "Emergency message received"}), 200

    @staticmethod
    @app.route('/basic_message', methods=['POST'])
    def basic_message():
        message = request.json
        print(message)
        return jsonify({"status": "success", "message": "Basic message received"}), 200

    @staticmethod
    @app.route('/reset', methods=['POST'])
    def reset_route():
        message = request.json
        print(message)

        if (message.get('reset')):
            Controller.use_display_1 = False
            Controlleruse_display_2 = False
            Controllershow_delays = False
            # TODO delete what is displayed on led panels

        return jsonify({"status": "success", "message": "Basic message received"}), 200


    def display_on_eth_led_panel(self, data):
        print("eth", data)

        routeID = data.get('routeID')
        remaining_stations = data.get('remaining_route_stations')
        destination_station = data.get('destination_station')
        train_state = data.get('state')
        train_delay = data.get('delay')

        print(f"Route ID: {routeID}")
        print(f"Remaining stations: {remaining_stations}")
        print(f"Destination station: {destination_station}")
        print(f"Train state: {train_state}")
        print(f"Train delay: {train_delay}")
        # TODO
        return

    def display_on_rs232_led_panel(self, data):
        print("rs232", data)

        routeID = data.get('routeID')
        remaining_stations = data.get('remaining_route_stations')
        destination_station = data.get('destination_station')
        train_state = data.get('state')
        train_delay = data.get('delay')

        print(f"Route ID: {routeID}")
        print(f"Remaining stations: {remaining_stations}")
        print(f"Destination station: {destination_station}")
        print(f"Train state: {train_state}")
        print(f"Train delay: {train_delay}")
        # TODO
        return
    @staticmethod
    def display_data(data, use_display_1, use_display_2, show_delays):
        threads = []

        controller_instance = Controller()

        # Check if Ethernet communication (use_display_1) is enabled
        if use_display_1:
            print("in 1")
            ethernet_thread = threading.Thread(target=controller_instance.display_on_eth_led_panel, args=(data,))
            ethernet_thread.start()  # Start the thread
            threads.append(ethernet_thread)  # Add to the list for joining later


        # Check if RS232 communication (use_display_2) is enabled
        if use_display_2:
            print("in 2")
            rs232_thread = threading.Thread(target=controller_instance.display_on_rs232_led_panel, args=(data,))
            rs232_thread.start()  # Start the thread
            threads.append(rs232_thread)  # Add to the list for joining later

        # Wait for started threads to complete
        for thread in threads:
            thread.join(timeout=10)

        if use_display_1 and use_display_2:
            print("ethernet and RS232")
        elif use_display_1:
            print("only ethernet")
        elif use_display_2:
            print("rS232")
        else:
            print("no communication")




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
