import threading

from flask import Flask, request, jsonify
import socket
app = Flask(__name__)

class Controller:

    use_display_1 = False
    use_display_2 = False
    train_state = ''

    show_delays = False
    @staticmethod
    @app.route('/route_update', methods=['POST'])
    def route_update():
        data = request.json
        print(data)

        Controller.display_data(data, Controller.use_display_1, Controller.use_display_2, Controller.show_delays)

        return jsonify({"status": "success", "message": "Route update received"}), 200

    @staticmethod
    @app.route('/settings', methods=['POST'])
    def update_settings():
        settings = request.json
        print(settings)
        # controller_instance = Controller()
        Controller.use_display_1 = bool(settings.get("display_1"))
        Controller.use_display_2 = bool(settings.get("display_2"))

        print(Controller.use_display_1, Controller.use_display_2)
        Controller.is_set = True
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

    @staticmethod
    def encode_char(char, rs232):
        if ord(char) < 128:
            return char
        else:
            if rs232:
                return ''.join([f"{byte:02x}" for byte in char.encode('utf-8')])
            return ''.join([f"\\{byte:02x}" for byte in char.encode('utf-8')])

    @staticmethod
    def build_xml_command(message_row1, message_row2, lang="sk", font="A", scroll_speed="4", priority="1",
                           timeout="30", bright="0", update_visualization_mode="Immediate"):

        # controller_instance = Controller()
        converted_message_row1 = ''.join([Controller.encode_char(char, 0) for char in message_row1])
        converted_message_row2 = ''.join([Controller.encode_char(char, 0) for char in message_row2])

        xml_command = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\\r\\n" \
                      "<Message Type=\"Aesys-PID\">\\r\\n" \
                      f"<Command Type=\"Stop\" IdCmd=\"1235\" Priority=\"{priority}\" Bright=\"{bright}\" ScrollSpeed=\"{scroll_speed}\" UpdateVisualizationMode=\"{update_visualization_mode}\" Timeout=\"{timeout}\">\\r\\n" \
                      "<TripData DoorState=\"close\" TrainArea=\"InStop\"/>\\r\\n" \
                      "<Texts>\\r\\n" \
                      "<Text1>\\r\\n" \
                      "<Languages>\\r\\n" \
                      f"<Language Code=\"{lang}\" Font=\"{font}\">{converted_message_row1}</Language>\\r\\n" \
                      "</Languages>\\r\\n" \
                      "</Text1>\\r\\n" \
                      "<Text2>\\r\\n" \
                      "<Languages>\\r\\n" \
                      f"<Language Code=\"{lang}\" Font=\"{font}\">{converted_message_row2}</Language>\\r\\n" \
                      "</Languages>\\r\\n" \
                      "</Text2>\\r\\n" \
                      "</Texts>\\r\\n" \
                      "</Command>\\r\\n" \
                      "</Message>"

        return xml_command

    @staticmethod
    def send_udp_command(ip_address, port, command, buffer_size=1024, timeout=1):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            sock.sendto(command.encode(), (ip_address, port))
            try:
                response, _ = sock.recvfrom(buffer_size)
                print("Received response from the panel:")
                print(response.decode())
            except socket.timeout:
                print("No response received within the timeout period.")

    def display_on_eth_led_panel(self, data):
        print("eth")

        routeID = data.get('routeID')
        remaining_stations = data.get('remaining_route_stations')
        destination_station = data.get('destination_station')
        Controller.train_state = data.get('state')
        train_delay = data.get('delay')

        message_row1 = destination_station
        message_row2 = "cez " + ', '.join(remaining_stations)
        xml_command = Controller.build_xml_command(message_row1, message_row2, lang="sk", font="B", scroll_speed="5")
        print(xml_command)

        panel_ip = "192.168.1.100"
        panel_port = 4000

        Controller.send_udp_command(panel_ip, panel_port, xml_command)

        # TODO
        return

    @staticmethod
    def calculate_checksum(command):
        checksum = 0x7F
        for byte in command:
            checksum ^= byte
        checksum &= 0x7F
        return checksum

    @staticmethod
    def format_message(upper_row, lower_row):
        encoded_upper_row = ''.join([Controller.encode_char(char, 1) for char in upper_row])
        encoded_lower_row = ''.join([Controller.encode_char(char, 1) for char in lower_row])
        # Convert textual representations of control characters to their binary equivalents
        control_chars = {
            '#1B': b'\x1B',  # prefix?
            '#E3': b'\xE3',  # font selection
            '#21': b'\x21',  # character spacing
            '#30': b'\x30',  # vertical positioning
            '#0A': b'\x0A',  # new line
            '#0B': b'\x0B',  # running text
            '#0D': b'\x0D',  # end code
        }

        # Base command with placeholders, without spaces and with binary control characters
        base_command = b'aA1' + control_chars['#1B'] + b"x" + control_chars['#E3'] + control_chars['#21'] + \
                       control_chars['#30'] + \
                       encoded_upper_row.encode() + control_chars['#0A'] + control_chars['#1B'] + b"x" + control_chars[
                           '#1B'] + b"d" + \
                       b'\x10' + control_chars['#1B'] + b"h" + b'\x19' + control_chars['#E3'] + control_chars['#21'] + \
                       control_chars['#1B'] + \
                       b"t" + b'\x11' + encoded_lower_row.encode() + control_chars['#0B']

        checksum = Controller.calculate_checksum(base_command)

        full_command = base_command + bytes([checksum]) + control_chars['#0D']

        return full_command

    def display_on_rs232_led_panel(self, data):
        print("rs232")

        routeID = data.get('routeID')
        remaining_stations = data.get('remaining_route_stations')
        destination_station = data.get('destination_station')
        Controller.train_state = data.get('state')
        train_delay = data.get('delay')


        message_row1 = destination_station
        message_row2 = "cez " + ', '.join(remaining_stations)
        formatted_command = Controller.format_message(message_row1, message_row2)
        print(formatted_command)

        printable_command = " ".join(f"{byte:02X}" for byte in formatted_command)
        print(printable_command)

        #dorobit posielanie na serial com port. formatted_command neviem ci je to spravne

        return




    @staticmethod
    def display_data(data):
        threads = []

        controller_instance = Controller()

        print(Controller.use_display_1, Controller.use_display_2)

        if Controller.use_display_1:
            ethernet_thread = threading.Thread(target=Controller.display_on_eth_led_panel, args=(controller_instance, data,))
            ethernet_thread.start()
            threads.append(ethernet_thread)


        if Controller.use_display_2:
            rs232_thread = threading.Thread(target=Controller.display_on_rs232_led_panel, args=(controller_instance, data,))
            rs232_thread.start()
            threads.append(rs232_thread)

        for thread in threads:
            thread.join(timeout=10)



        if Controller.use_display_1 and Controller.use_display_2:
            print("ethernet and RS232")
        elif Controller.use_display_1:
            print("only ethernet")
        elif Controller.use_display_2:
            print("rS232")
        else:
            print("no communication")




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
