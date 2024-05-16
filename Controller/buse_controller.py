import threading
import serial
import queue
import time

from unidecode import unidecode


class BuseController:
    thread = None
    running = None
    stop_thread = None
    command_queue = None
    _serial_comm_thread = None
    ser = None
    _instance = None
    com_port = "COM10"
    demo = False

    def __new__(cls):
        if cls._instance is None:
            cls.demo = False
            cls._instance = super(BuseController, cls).__new__(cls)
            cls.command_queue = queue.Queue()
            try:
                cls.ser = serial.Serial(port=cls.com_port, baudrate=1200, bytesize=serial.SEVENBITS,
                                                parity=serial.PARITY_EVEN,
                                                stopbits=serial.STOPBITS_TWO, timeout=3)
            except:
                cls.demo = True
            cls.running = threading.Event()
            cls.stop_thread = threading.Event()
            cls.thread = None

        return cls._instance

    @classmethod
    def __serial_comm_thread_in_station(cls, train_number, destination, remaining_train_stops, train_delay, delay_between_displays, show_delay):
        while not cls.stop_thread.is_set():

            if cls.running.is_set():
                try:

                    try:
                        # upper part
                        message = cls.upper_command(destination)
                        print(message)
                        if not cls.demo:
                            cls.ser.write(message)
                        time.sleep(1)
                        if not cls.demo:
                            cls.print_response()

                        if cls.stop_thread.is_set():
                            return

                            # lower part
                        for stop in remaining_train_stops:
                            print("1 -> remaining stops from the cycle:", stop)
                            message = cls.lower_command('cez ' + stop)
                            print(message)
                            if not cls.demo:
                                cls.ser.write(message)
                            time.sleep(delay_between_displays)
                            if not cls.demo:
                                cls.print_response()
                            if cls.stop_thread.is_set():
                                return

                    except serial.SerialException as e:
                        print("Demo mode or serial port not connected. Error: ", e)

                    if show_delay:
                        try:
                            # upper part
                            message = cls.upper_command('Meskanie')
                            print(message)
                            if not cls.demo:
                                cls.ser.write(message)
                            time.sleep(1)
                            if not cls.demo:
                                cls.print_response()

                            message = cls.lower_command(str(train_delay) + " min.")
                            print("2 -> train delay:", train_delay, " min")
                            print(message)
                            if not cls.demo:
                                cls.ser.write(message)
                            time.sleep(delay_between_displays)
                            if not cls.demo:
                                cls.print_response()

                            if cls.stop_thread.is_set():
                                return

                        except serial.SerialException as e:
                            print("Demo mode or serial port not connected. Error: ", e)


                    try:
                        # upper part
                        message = cls.upper_command(destination)
                        print(message)
                        if not cls.demo:
                            cls.ser.write(message)
                        time.sleep(1)
                        if not cls.demo:
                            cls.print_response()

                        message = cls.lower_command(train_number)
                        print(message)
                        if not cls.demo:
                            cls.ser.write(message)
                        time.sleep(delay_between_displays)
                        if not cls.demo:
                            cls.print_response()

                        if cls.stop_thread.is_set():
                            return

                    except serial.SerialException as e:
                        print("Demo mode or serial port not connected. Error: ", e)


                    time.sleep(delay_between_displays)

                except queue.Empty:
                    continue
            else:
                time.sleep(0.1)

    @classmethod
    def print_response(cls):
        response = cls.ser.read()
        if response:
            print('Received:', response.decode())
        else:
            print('No response received.')

    @classmethod
    def lower_command(cls, stop):

        message = f'aA1 \x0A\x1Bx\x1Bd\x10\x1Bh\x19\x1Bt\x11{unidecode(stop)}\x0D'
        message = message.encode()
        message = cls.checksum(message)
        return message

    @classmethod
    def checksum(cls, message):
        checksum = 0
        for byte in message:
            checksum ^= byte
        checksum = 0x7F & ~checksum
        checksum_byte = chr(checksum).encode()
        message += checksum_byte
        message += b'\r'
        return message

    @classmethod
    def upper_command(cls, destination):
        message_upper = f"aA1 {unidecode(destination)}"
        message_upper += '\x0D'
        message = message_upper.encode()
        message = cls.checksum(message)
        return message

    @classmethod
    def __serial_comm_thread_after_station(cls, train_number, destination, delay_between_displays):
        while not cls.stop_thread.is_set():

            if cls.running.is_set():
                try:

                    try:
                        # upper part
                        message = cls.upper_command('smer')
                        print(message)
                        if not cls.demo:
                            cls.ser.write(message)
                        time.sleep(1)
                        if not cls.demo:
                            cls.print_response()

                        message = cls.lower_command(destination)
                        print(message)
                        if not cls.demo:
                            cls.ser.write(message)
                        time.sleep(delay_between_displays)
                        if not cls.demo:
                            cls.print_response()

                        if cls.stop_thread.is_set():
                            return

                        # upper part
                        message = cls.upper_command(destination)
                        print(message)
                        if not cls.demo:
                            cls.ser.write(message)
                        time.sleep(1)
                        if not cls.demo:
                            cls.print_response()

                        message = cls.lower_command(train_number)
                        print(message)
                        if not cls.demo:
                            cls.ser.write(message)
                        time.sleep(delay_between_displays)
                        if not cls.demo:
                            cls.print_response()

                        if cls.stop_thread.is_set():
                            return

                    except serial.SerialException as e:
                        print("Demo mode or serial port not connected. Error: ", e)


                    time.sleep(delay_between_displays)

                except queue.Empty:
                    continue
            else:
                time.sleep(0.1)

    @classmethod
    def __serial_comm_thread_before_station(cls, destination, delay_between_displays):
        while not cls.stop_thread.is_set():

            if cls.running.is_set():
                try:

                    try:
                        # upper part
                        message1 = cls.upper_command('smer')
                        print(message1)
                        if not cls.demo:
                            cls.ser.write(message1)
                        time.sleep(1)
                        if not cls.demo:
                            cls.print_response()

                        message2 = cls.lower_command(destination)
                        print(message2)
                        if not cls.demo:
                            cls.ser.write(message2)
                        time.sleep(delay_between_displays)
                        if not cls.demo:
                            cls.print_response()

                        if cls.stop_thread.is_set():
                            return

                    except serial.SerialException as e:
                        print("Demo mode or serial port not connected. Error: ", e)

                    time.sleep(delay_between_displays)

                except queue.Empty:
                    continue
            else:
                time.sleep(0.1)


    @classmethod
    def __serial_comm_thread_one_row(cls, message, delay_between_displays):
        while not cls.stop_thread.is_set():

            if cls.running.is_set():
                try:

                    try:
                        # upper part
                        message1 = cls.upper_command(message)
                        print(message1)
                        if not cls.demo:
                            cls.ser.write(message1)
                        time.sleep(1)
                        if not cls.demo:
                            cls.print_response()

                        message2 = cls.lower_command(' ')
                        print(message2)
                        if not cls.demo:
                            cls.ser.write(message2)
                        time.sleep(delay_between_displays)
                        if not cls.demo:
                            cls.print_response()

                        return

                    except serial.SerialException as e:
                        print("Demo mode or serial port not connected. Error: ", e)

                    time.sleep(delay_between_displays)

                except queue.Empty:
                    continue
            else:
                time.sleep(0.1)

    @classmethod
    def start_display_in_station(cls, train_number, destination, train_stops, train_delay, delay_between_displays, show_delay):
        cls.shutdown()
        cls.stop_display()
        cls.running.set()
        cls.stop_thread.clear()
        if cls.thread is None or not cls.thread.is_alive():
            cls.thread = threading.Thread(target=cls.__serial_comm_thread_in_station, args=(train_number, destination, train_stops, train_delay, delay_between_displays, show_delay))
            cls.thread.start()

    @classmethod
    def start_display_after_station(cls, train_number, destination, delay_between_displays):
        cls.shutdown()
        cls.stop_display()
        cls.running.set()
        cls.stop_thread.clear()
        if cls.thread is None or not cls.thread.is_alive():
            cls.thread = threading.Thread(target=cls.__serial_comm_thread_after_station, args=(
            train_number, destination, delay_between_displays))
            cls.thread.start()

    @classmethod
    def start_display_before_station(cls, destination, delay_between_displays):
        cls.shutdown()
        cls.stop_display()
        cls.running.set()
        cls.stop_thread.clear()
        if cls.thread is None or not cls.thread.is_alive():
            cls.thread = threading.Thread(target=cls.__serial_comm_thread_before_station, args=(
                destination, 1))
            cls.thread.start()

    @classmethod
    def start_display_simple_message(cls, message, delay_between_displays):
        cls.shutdown()
        cls.stop_display()
        cls.running.set()
        cls.stop_thread.clear()
        if cls.thread is None or not cls.thread.is_alive():
            cls.thread = threading.Thread(target=cls.__serial_comm_thread_one_row, args=(
                message, delay_between_displays))
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
    def set_com_port(cls, com_port):
        cls.com_port = com_port
        try:
            cls.ser = serial.Serial(port=cls.com_port, baudrate=1200, bytesize=serial.SEVENBITS,
                                parity=serial.PARITY_EVEN,
                                stopbits=serial.STOPBITS_TWO, timeout=3)
            cls.demo = False
        except:
            cls.demo = True

    @classmethod
    def test_connectivity(cls):
        diagnostic_message = "a 2"
        diagnostic_message += '\x0D'
        print(diagnostic_message)

        message = diagnostic_message.encode()
        message = cls.checksum(message)
        print(message)
        try:
            cls.ser.write(message)
            time.sleep(1)
            response = cls.ser.read()
            if response:
                print('Received:', response.decode())
                return True
            else:
                print('No response received.')
                return False

        except serial.SerialException as e:
            return False


