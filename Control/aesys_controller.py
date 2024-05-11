import queue
import socket
import threading
import time


class AesysController:
    _instance = None

    thread = None
    running = None
    stop_thread = None
    command_queue = None

    panel_ip = "172.16.4.121"
    panel_port = 80

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AesysController, cls).__new__(cls)
            cls.command_queue = queue.Queue()
            cls.running = threading.Event()
            cls.stop_thread = threading.Event()
            cls.thread = None
        return cls._instance

    @classmethod
    def __thread_in_station(cls, train_number, destination_station, remaining_stations, train_delay, speed, brightness):
        while not cls.stop_thread.is_set():

            if cls.running.is_set():
                try:

                    message_row1 = str(destination_station)
                    message_row2 = "cez " + ', '.join(remaining_stations)

                    xml_command = cls.build_two_row_xml_command(message_row1=message_row1,
                                                                message_row2=message_row2,
                                                                scroll_speed=speed,
                                                                update_visualization_mode='WaitScrolling',
                                                                bright=brightness,
                                                                priority='3')
                    # print("xml command:", xml_command)
                    cls.send_udp_packet(cls.panel_ip, cls.panel_port, xml_command, timeout=1)


                    message_row1 = "Meškanie"
                    message_row2 = str(train_delay) + " min."

                    xml_command = cls.build_two_row_xml_command(message_row1=message_row1,
                                                                message_row2=message_row2,
                                                                scroll_speed=speed,
                                                                update_visualization_mode='WaitScrolling',
                                                                bright=brightness,
                                                                priority='3',
                                                                timeout='2')
                    # print("xml command:", xml_command)
                    cls.send_udp_packet(cls.panel_ip, cls.panel_port, xml_command, timeout=1)

                    message_row1 = str(destination_station)
                    message_row2 = str(train_number)

                    xml_command = cls.build_two_row_xml_command(message_row1=message_row1,
                                                                message_row2=message_row2,
                                                                scroll_speed=speed,
                                                                update_visualization_mode='WaitScrolling',
                                                                bright=brightness,
                                                                priority='3',
                                                                timeout='2')
                    # print("xml command:", xml_command)
                    cls.send_udp_packet(cls.panel_ip, cls.panel_port, xml_command, timeout=1)


                    time.sleep(10)

                    if cls.stop_thread.is_set():
                        return

                except queue.Empty:
                    continue
            else:
                time.sleep(0.1)

    @classmethod
    def __thread_after_station(cls, train_number, destination_station, speed, brightness):
        while not cls.stop_thread.is_set():

            if cls.running.is_set():
                try:

                    message_row1 = "smer"
                    message_row2 = str(destination_station)

                    xml_command = cls.build_two_row_xml_command(message_row1=message_row1,
                                                                message_row2=message_row2,
                                                                scroll_speed=speed,
                                                                update_visualization_mode='WaitScrolling',
                                                                bright=brightness,
                                                                priority='3',
                                                                timeout='2')
                    # print("xml command:", xml_command)
                    cls.send_udp_packet(cls.panel_ip, cls.panel_port, xml_command, timeout=1)

                    message_row1 = str(destination_station)
                    message_row2 = str(train_number)

                    xml_command = cls.build_two_row_xml_command(message_row1=message_row1,
                                                                message_row2=message_row2,
                                                                scroll_speed=speed,
                                                                update_visualization_mode='WaitScrolling',
                                                                bright=brightness,
                                                                priority='3',
                                                                timeout='2')
                    # print("xml command:", xml_command)
                    cls.send_udp_packet(cls.panel_ip, cls.panel_port, xml_command, timeout=1)

                    time.sleep(5)

                    if cls.stop_thread.is_set():
                        return

                except queue.Empty:
                    continue
            else:
                time.sleep(0.1)

    @classmethod
    def build_two_row_xml_command(cls, message_row1, message_row2, lang="sk", font="A", priority="1",
                                  timeout="0", update_visualization_mode="Immediate", scroll_speed = 4, bright=0):

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

    @classmethod
    def build_one_row_xml_command(cls, message_row1, lang="sk", font="A", priority="1",
                                  timeout="0", update_visualization_mode="Immediate", scroll_speed = 4, bright=0):

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
                      "</Texts>\r\n" \
                      "</Command>\r\n" \
                      "</Message>"

        return xml_command


    @classmethod
    def start_display_before_station(cls, destination_station, speed, brightness):
        cls.shutdown()
        cls.stop_display()

        xml_command = cls.build_two_row_xml_command("smer",
                                                    destination_station,
                                                    scroll_speed=speed,
                                                    bright=brightness,
                                                    priority='3')
        print("xml command:", xml_command)
        cls.send_udp_packet(cls.panel_ip, cls.panel_port, xml_command, timeout=1)

    @classmethod
    def start_display_in_station(cls, train_number, destination_station, remaining_stations, train_delay, speed, brightness):
        cls.shutdown()
        cls.stop_display()
        cls.running.set()
        cls.stop_thread.clear()
        if cls.thread is None or not cls.thread.is_alive():
            cls.thread = threading.Thread(target=cls.__thread_in_station, args=(
            train_number, destination_station, remaining_stations, train_delay, speed, brightness))
            cls.thread.start()

    @classmethod
    def start_display_after_station(cls, train_number, destination_station, speed, brightness):
        cls.shutdown()
        cls.stop_display()
        cls.running.set()
        cls.stop_thread.clear()
        if cls.thread is None or not cls.thread.is_alive():
            cls.thread = threading.Thread(target=cls.__thread_in_station, args=(
                train_number, destination_station, speed, brightness))
            cls.thread.start()


    @classmethod
    def stop_display(cls):
        cls.running.clear()

    @classmethod
    def shutdown(cls):
        cls.stop_thread.set()
        if cls.thread:
            cls.thread.join()

    @classmethod
    def start_display_simple_message(cls, message):
        cls.shutdown()
        cls.stop_display()

        xml_command = cls.build_one_row_xml_command(message,priority='3')
        print("xml command:", xml_command)
        cls.send_udp_packet(cls.panel_ip, cls.panel_port, xml_command, timeout=1)

    @classmethod
    def reset(cls):
        cls.shutdown()
        cls.stop_display()

        xml_command = cls.build_one_row_xml_command('', priority='1')
        print("xml command:", xml_command)
        cls.send_udp_packet(cls.panel_ip, cls.panel_port, xml_command, timeout=1)

        xml_command = cls.build_one_row_xml_command('', priority='3')
        print("xml command:", xml_command)
        cls.send_udp_packet(cls.panel_ip, cls.panel_port, xml_command, timeout=1)

    @classmethod
    def test_connectivity(cls):

        xml_command = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n" \
                      "<Message Type=\"Aesys-PID\">\r\n" \
                      "<Command Type=\"CheckIfAlive\" IdCmd=\"1235\">\r\n" \
                      "</Message>"

        print("xml command:", xml_command)

        try:
            result = cls.send_udp_packet(cls.panel_ip, cls.panel_port, xml_command, timeout=1)
            if result is not None:
                return True
            else:
                return False
        except:
            return False

    @classmethod
    def send_udp_packet(cls, ip_address, port, command, buffer_size=1024, timeout=5):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            hex_command = command.encode()
            print("hex comm", hex_command)
            sock.sendto(hex_command, (ip_address, port))
            try:
                response, _ = sock.recvfrom(buffer_size)
                print("Received response from the panel:")
                print(response.decode())
                return response.decode()
            except socket.timeout:
                print("No response received after timeout")
                return None








