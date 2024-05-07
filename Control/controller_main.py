import binascii
import threading
import time
from datetime import datetime

from unidecode import unidecode
import serial

from flask import Flask, request, jsonify
import socket
app = Flask(__name__)

class Controller:

    # display_one_row_on_eth_led_panel = None
    use_display_1 = False
    use_display_2 = True
    train_state = ''

    ser = None
    # stop_threads_checked = False

    stop_threads = False
    threads = []

    show_delays = False

    @staticmethod
    @app.route('/controller_connectivity_test', methods=['GET'])
    def self_test():
        return jsonify({"status": "success",}), 200

    @staticmethod
    @app.route('/controller_internet_connectivity_test', methods=['GET'])
    def test_internet():
        try:
            socket.setdefaulttimeout(5)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
            return jsonify({"internet_status": "success", }), 200
        except socket.error as e:
            print(e)
            return jsonify({"internet_status": "fail", }), 503

    @staticmethod
    @app.route('/controller_display_panel_1_test', methods=['GET'])
    def test_ethernet_panel():
        try:
            if Controller.test_ethernet_panel_connectivity():
                return jsonify({"ethernet_display_panel_connectivity": "success", }), 200
            else:
                return jsonify({"ethernet_display_panel_connectivity": "fail", }), 503
        except:
            return jsonify({"ethernet_display_panel_connectivity": "fail", }), 503

    @classmethod
    def test_ethernet_panel_connectivity(cls):

        xml_command = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n" \
                      "<Message Type=\"Aesys-PID\">\r\n" \
                      "<Command Type=\"CheckIfAlive\" IdCmd=\"1235\">\r\n" \
                      "</Message>"

        print("xml command:", xml_command)

        panel_ip = "172.16.4.121"
        panel_port = 80

        try:
            result = Controller.send_udp_command(panel_ip, panel_port, xml_command, timeout=1)
            print("returning true")
            if result is not None:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    @app.route('/controller_display_panel_2_test', methods=['GET'])
    def test_ibis_panel():
        try:
            if Controller.test_ibis_panel_connectivity():
                return jsonify({"ibis_display_panel_connectivity": "success", }), 200
            else:
                return jsonify({"ibis_display_panel_connectivity": "fail", }), 503
        except:
            return jsonify({"ibis_display_panel_connectivity": "fail", }), 503

    @classmethod
    def test_ibis_panel_connectivity(cls):

        diagnostic_message = "a 2"
        diagnostic_message += '\x0D'
        print(diagnostic_message)
        if Controller.ser is None:
            ser = serial.Serial(port='COM3', baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                                stopbits=serial.STOPBITS_TWO, timeout=3)
            Controller.ser = ser
        else:
            ser = Controller.ser
        message = diagnostic_message.encode()
        checksum = 0
        for byte in message:
            checksum ^= byte
        checksum = 0x7F & ~checksum
        checksum_byte = chr(checksum).encode()
        message += checksum_byte
        message += b'\r'
        print(message)
        try:
            ser.write(message)
            time.sleep(1)
            response = ser.read()
            if response:
                print('Received:', response.decode())
                return True
            else:
                print('No response received.')
                return False

        except serial.SerialException as e:
            # print(f"Error: {e}")
            return False






    @staticmethod
    @app.route('/route_update', methods=['POST'])
    def route_update():


        for thread in Controller.threads:
            thread.join(timeout=0.5)

        Controller.stop_threads = False

        Controller.threads = []

        data = request.json
        print(data)

        Controller.display_two_row_data(data)

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
        Controller.display_one_row_data(message)
        print(message)
        return jsonify({"status": "success", "message": "Basic message received"}), 200

    @staticmethod
    @app.route('/reset_message', methods=['POST'])
    def reset_message():

        current_date = datetime.now()
        date_str = current_date.strftime("%d.%m.%Y")
        # Controller.display_one_row_data(date_str, reset_message = True)

        Controller.reset_rs232(date_str)

        Controller.stop_threads = True
        for thread in Controller.threads:
            thread.join(timeout=1)

        Controller.stop_threads = False
        Controller.threads = []

        # time.sleep(1)

        return jsonify({"status": "success", "message": "Reset message received"}), 200


    # @staticmethod
    # @app.route('/reset', methods=['POST'])
    # def reset_route():
    #     message = request.json
    #     print(message)
    #
    #     if (message.get('reset')):
    #         Controller.use_display_1 = False
    #         Controlleruse_display_2 = False
    #         Controllershow_delays = False
    #         # TODO delete what is displayed on led panels
    #
    #     return jsonify({"status": "success", "message": "Basic message received"}), 200

    @staticmethod
    def reset_rs232(upper_row):
        ser = Controller.rs232_display_upper(upper_row)
        i = 0

        lower_row = ' '

        if Controller.stop_threads:
            return

        message = f'aA1 \x0A\x1Bx\x1Bd\x10\x1Bh\x19\x1Bt\x11{unidecode(lower_row)}\x0D'

        print("from cycle:", lower_row)

        message = message.encode()
        checksum = 0
        for byte in message:
            checksum ^= byte
        checksum = 0x7F & ~checksum
        checksum_byte = chr(checksum).encode()
        message += checksum_byte
        message += b'\r'

        try:
            print(message)
            ser.write(message)
            if Controller.stop_threads:
                return
            time.sleep(1)
            if Controller.stop_threads:
                return
            response = ser.read()
            if response:
                print('Received:', response.decode())
            else:
                print('No response received.')

        except serial.SerialException as e:
            print(f"Error: {e}")



    @staticmethod
    def encode_char(char, rs232):
        if ord(char) < 128:
            return char
        else:
            if rs232:
                return ''.join([f"{byte:02x}" for byte in char.encode('utf-8')])
            print("...")
            return ''.join([f"\\{byte:02x}" for byte in char.encode('utf-8')])

    @staticmethod
    def build_two_row_xml_command(message_row1, message_row2, lang="sk", font="A", scroll_speed="4", priority="1",
                                  timeout="30", bright="0", update_visualization_mode="Immediate"):

        # controller_instance = Controller()
        # converted_message_row1 = ''.join([Controller.encode_char(char, 0) for char in message_row1])
        # converted_message_row2 = ''.join([Controller.encode_char(char, 0) for char in message_row2])

        xml_command = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n" \
                      "<Message Type=\"Aesys-PID\">\r\n" \
                      f"<Command Type=\"Stop\" IdCmd=\"1235\" Priority=\"{priority}\" Bright=\"{bright}\" ScrollSpeed=\"{scroll_speed}\" UpdateVisualizationMode=\"{update_visualization_mode}\" Timeout=\"{timeout}\">\r\n" \
                      "<TripData DoorState=\"close\" TrainArea=\"InStop\"/>\r\n" \
                      "<Texts>\r\n" \
                      "<Text1>\r\n" \
                      "<Languages>\r\n" \
                      f"<Language Code=\"{lang}\" Font=\"{font}\">{message_row1}</Language>\r\n" \
                      "</Languages>\r\n" \
                      "</Text1>\r\n" \
                      "<Text2>\r\n" \
                      "<Languages>\r\n" \
                      f"<Language Code=\"{lang}\" Font=\"{font}\">{message_row2}</Language>\r\n" \
                      "</Languages>\r\n" \
                      "</Text2>\r\n" \
                      "</Texts>\r\n" \
                      "</Command>\r\n" \
                      "</Message>"

        return xml_command

    @staticmethod
    def build_one_row_xml_command(message, lang="sk", font="A", scroll_speed="4", priority="1",
                                  timeout="30", bright="0", update_visualization_mode="Immediate"):

        xml_command = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n" \
                      "<Message Type=\"Aesys-PID\">\r\n" \
                      f"<Command Type=\"Stop\" IdCmd=\"1235\" Priority=\"{priority}\" Bright=\"{bright}\" ScrollSpeed=\"{scroll_speed}\" UpdateVisualizationMode=\"{update_visualization_mode}\" Timeout=\"{timeout}\">\r\n" \
                      "<TripData DoorState=\"close\" TrainArea=\"InStop\"/>\r\n" \
                      "<Texts>\r\n" \
                      "<Text1>\r\n" \
                      "<Languages>\r\n" \
                      f"<Language Code=\"{lang}\" Font=\"{font}\">{message}</Language>\r\n" \
                      "</Languages>\r\n" \
                      "</Text1>\r\n" \
                      "</Texts>\r\n" \
                      "</Command>\r\n" \
                      "</Message>"

        return xml_command

    @staticmethod
    def send_udp_command(ip_address, port, command, buffer_size=1024, timeout=5):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            hex_command = command.encode()
            print("hex comm", hex_command)
            sock.sendto(hex_command, (ip_address, port))  # Send hex data
            try:
                response, _ = sock.recvfrom(buffer_size)
                print("Received response from the panel:")
                print(response.decode())  # Assuming response is also in text format
                return response.decode()
            except socket.timeout:
                print("No response received within the timeout period.")
                return None


    def display_two_row_on_eth_led_panel(self, data):
        print("eth")

        routeID = data.get('routeID')
        remaining_stations = data.get('remaining_route_stations')
        destination_station = data.get('destination_station')
        Controller.train_state = data.get('state')
        train_delay = data.get('delay')

        message_row1 = destination_station
        message_row2 = "cez " + ', '.join(remaining_stations)
        xml_command = Controller.build_two_row_xml_command(message_row1, message_row2, lang="sk", font="B", scroll_speed="5")
        print("xml command:", xml_command)

        panel_ip = "172.16.4.121"
        panel_port = 80

        Controller.send_udp_command(panel_ip, panel_port, xml_command)

        # TODO? neviem co
        return



    def display_two_row_on_rs232_ibis_panel(self, data):
        # print("eth")

        routeID = data.get('routeID')
        remaining_stations = data.get('remaining_route_stations')
        destination_station = data.get('destination_station')
        Controller.train_state = data.get('state')
        train_delay = data.get('delay')

        message_row1 = destination_station
        Controller.format_message_for_two_row_rs232(message_row1, remaining_stations, Controller.train_state)

        return

    @staticmethod
    def calculate_checksum(command):
        checksum = 0x7F
        for byte in command:
            checksum ^= byte
        checksum &= 0x7F
        return checksum

    @staticmethod
    def format_message_for_two_row_rs232(upper_row, lower_row_stops, state):

        print("current state:", state)

        sleep_between_show = 1

        if state == 'in_station':
            # cycling:
            # 1.
            # dest station
            # cez stanice
            # 2.
            # Meskanie
            # x min.
            # 3.
            # dest station
            # os x
            # 4.
            # Odchod o
            # x min.

            lower_row_stops.pop(0)

            while not Controller.stop_threads:

                # first cycle
                ser = Controller.rs232_display_upper(upper_row)
                i = 0


                for lower_row in lower_row_stops:
                    if Controller.stop_threads:
                        return
                    if i == 0:
                        lower_row = 'cez ' + lower_row

                    i += 1

                    message = f'aA1 \x0A\x1Bx\x1Bd\x10\x1Bh\x19\x1Bt\x11{unidecode(lower_row)}\x0D'

                    print("from cycle:", lower_row)

                    message = message.encode()
                    if Controller.stop_threads:
                        return
                    checksum = 0
                    for byte in message:
                        if Controller.stop_threads:
                            return
                        checksum ^= byte
                    if Controller.stop_threads:
                        return
                    checksum = 0x7F & ~checksum
                    checksum_byte = chr(checksum).encode()
                    message += checksum_byte
                    message += b'\r'

                    try:
                        print(message)
                        ser.write(message)
                        if Controller.stop_threads:
                            return
                        time.sleep(sleep_between_show)
                        if Controller.stop_threads:
                            return
                        response = ser.read()
                        if response:
                            print('Received:', response.decode())
                        else:
                            print('No response received.')

                    except serial.SerialException as e:
                        print(f"Error: {e}")


                # second cycle

                if Controller.stop_threads:
                    return

                ser = Controller.rs232_display_upper("Meskanie")

                lower_row = '2 min.'

                message = f'aA1 \x0A\x1Bx\x1Bd\x10\x1Bh\x19\x1Bt\x11{unidecode(lower_row)}\x0D'
                print("from str:", lower_row)
                message = message.encode()
                checksum = 0
                for byte in message:
                    checksum ^= byte
                checksum = 0x7F & ~checksum
                checksum_byte = chr(checksum).encode()
                message += checksum_byte
                message += b'\r'

                try:
                    print(message)
                    ser.write(message)
                    if Controller.stop_threads:
                        return
                    time.sleep(sleep_between_show)
                    if Controller.stop_threads:
                        return
                    response = ser.read()
                    if response:
                        print('Received:', response.decode())
                    else:
                        print('No response received.')

                except serial.SerialException as e:
                    print(f"Error: {e}")


                # time.sleep(1)


                # third cycle

                ser = Controller.rs232_display_upper(upper_row)
                i = 0

                lower_row = 'Os 3013'

                if Controller.stop_threads:
                    return

                message = f'aA1 \x0A\x1Bx\x1Bd\x10\x1Bh\x19\x1Bt\x11{unidecode(lower_row)}\x0D'

                print("from cycle:", lower_row)

                message = message.encode()
                checksum = 0
                for byte in message:
                    checksum ^= byte
                checksum = 0x7F & ~checksum
                checksum_byte = chr(checksum).encode()
                message += checksum_byte
                message += b'\r'

                try:
                    print(message)
                    ser.write(message)
                    if Controller.stop_threads:
                        return
                    time.sleep(sleep_between_show)
                    if Controller.stop_threads:
                        return
                    response = ser.read()
                    if response:
                        print('Received:', response.decode())
                    else:
                        print('No response received.')

                except serial.SerialException as e:
                    print(f"Error: {e}")


                # time.sleep(1)

                # fourth cycle

                ser = Controller.rs232_display_upper("Odchod o")
                i = 0

                lower_row = '1 min.'

                if Controller.stop_threads:
                    return

                message = f'aA1 \x0A\x1Bx\x1Bd\x10\x1Bh\x19\x1Bt\x11{unidecode(lower_row)}\x0D'

                print("from cycle:", lower_row)

                message = message.encode()
                checksum = 0
                for byte in message:
                    checksum ^= byte
                checksum = 0x7F & ~checksum
                checksum_byte = chr(checksum).encode()
                message += checksum_byte
                message += b'\r'

                try:
                    print(message)
                    ser.write(message)
                    if Controller.stop_threads:
                        return
                    time.sleep(sleep_between_show)
                    if Controller.stop_threads:
                        return
                    response = ser.read()
                    if response:
                        print('Received:', response.decode())
                    else:
                        print('No response received.')

                except serial.SerialException as e:
                    print(f"Error: {e}")

        if state == 'after_station' or state == 'before_station':
            # smer
            # os x

            ser = Controller.rs232_display_upper(upper_row)

            lower_row = 'Os 3013'

            message = f'aA1 \x0A\x1Bx\x1Bd\x10\x1Bh\x19\x1Bt\x11{unidecode(lower_row)}\x0D'

            print("from cycle:", lower_row)

            message = message.encode()
            checksum = 0
            for byte in message:
                checksum ^= byte
            checksum = 0x7F & ~checksum
            checksum_byte = chr(checksum).encode()
            message += checksum_byte
            message += b'\r'

            try:
                print(message)
                ser.write(message)
                time.sleep(2)
                response = ser.read()
                if response:
                    print('Received:', response.decode())
                else:
                    print('No response received.')

            except serial.SerialException as e:
                print(f"Error: {e}")
            return



    @staticmethod
    def rs232_display_upper(upper_row):
        message_upper = f"aA1 {unidecode(upper_row)}"
        message_upper += '\x0D'
        if Controller.ser is None:
            ser = serial.Serial(port='COM3', baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                                stopbits=serial.STOPBITS_TWO, timeout=3)
            Controller.ser = ser
        else:
            ser = Controller.ser
        message = message_upper.encode()
        checksum = 0
        for byte in message:
            checksum ^= byte
        checksum = 0x7F & ~checksum
        checksum_byte = chr(checksum).encode()
        message += checksum_byte
        message += b'\r'
        try:
            print(message)
            ser.write(message)
            time.sleep(1)
            response = ser.read()
            if response:
                print('Received:', response.decode())
            else:
                print('No response received.')

        except serial.SerialException as e:
            print(f"Error: {e}")
        return ser

    @staticmethod
    def display_two_row_data(data):
        # threads = []

        controller_instance = Controller()

        print(Controller.use_display_1, Controller.use_display_2)

        if Controller.use_display_1:
            ethernet_thread = threading.Thread(target=Controller.display_two_row_on_eth_led_panel, args=(controller_instance, data,))
            ethernet_thread.start()
            Controller.threads.append(ethernet_thread)


        if Controller.use_display_2:
            rs232_thread = threading.Thread(target=Controller.display_two_row_on_rs232_ibis_panel, args=(controller_instance, data,))
            rs232_thread.start()
            Controller.threads.append(rs232_thread)

        # for thread in Controller.threads:
        #     thread.join(timeout=1)
        #
        # if Controller.use_display_1 and Controller.use_display_2:
        #     print("ethernet and RS232")
        # elif Controller.use_display_1:
        #     print("only ethernet")
        # elif Controller.use_display_2:
        #     print("rS232")
        # else:
        #     print("no communication")



    # @staticmethod
    def display_one_row_on_eth_led_panel(self, message_data):

        print("eth")
        if message_data == ' ':
            message = ''
        else:
            message = message_data.get('message')
        # remaining_stations = message.get('remaining_route_stations')
        # destination_station = message.get('destination_station')
        # Controller.train_state = message.get('state')
        # train_delay = message.get('delay')

        message_row1 = message
        xml_command = Controller.build_one_row_xml_command(message_row1, lang="sk", font="B",
                                                           scroll_speed="5")
        print("xml command:", xml_command)

        panel_ip = "172.16.4.121"
        panel_port = 80

        Controller.send_udp_command(panel_ip, panel_port, xml_command)

        return

    # @staticmethod
    def display_one_row_on_rs232_led_panel(self, upper_row, reset_message):

        if not reset_message:
            upper_row = upper_row['message']

        print("one row", upper_row)

        message = f"aA1 {unidecode(upper_row)}"

        message += '\x0D'

        print('RS232 message:', message)

        if Controller.ser is None:
            ser = serial.Serial(port='COM3', baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                                stopbits=serial.STOPBITS_TWO, timeout=3)
            Controller.ser = ser
        else:
            ser = Controller.ser

        # Calculate checksum (simple exclusive OR of bytes)
        message = message.encode()

        checksum = 0
        for byte in message:
            checksum ^= byte

        # Apply mask and NOT operation to the checksum
        checksum = 0x7F & ~checksum

        # Convert checksum to a character and then encode it to bytes
        checksum_byte = chr(checksum).encode()

        message += checksum_byte

        message += b'\r'  # Carriage return as a byte

        try:

            print(message)
            ser.write(message)

            time.sleep(1)

            response = ser.read()
            if response:
                print('Received:', response.decode())
            else:
                print('No response received.')

        except serial.SerialException as e:
            print(f"Error: {e}")

        finally:
            if ser.is_open:
                print("closing")


    @staticmethod
    def display_one_row_data(message, reset_message = False):
        threads = []

        controller_instance = Controller()

        print(Controller.use_display_1, Controller.use_display_2)

        if Controller.use_display_1:
            ethernet_thread = threading.Thread(target=Controller.display_one_row_on_eth_led_panel,
                                               args=(controller_instance, message,))
            ethernet_thread.start()
            threads.append(ethernet_thread)

        if Controller.use_display_2:
            rs232_thread = threading.Thread(target=Controller.display_one_row_on_rs232_led_panel,
                                        args=(controller_instance, message, reset_message))
            rs232_thread.start()
            threads.append(rs232_thread)

        for thread in threads:
            thread.join(timeout=1)

        # print("ethernet and RS232")




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
