import serial
import time

def format_message(upper_row, lower_row):
    # Base command for panel with address 1; change as needed
    command = 'aA1 '

    # Controller sequence and command to set up the display attributes
    attributes = '#1Bx#E3#21#30'

    # Prepare upper and lower rows with required control characters for new line and continuity
    upper_command = f'#1Bh#19{upper_row}#0A'  # 0A is LF
    lower_command = f'#1Bd#10#1Bt#11{lower_row}#0B'  # 0B is VT

    # Combine parts of the message
    full_message = command + attributes + upper_command + lower_command

    # Calculate checksum (simple exclusive OR of bytes)
    checksum = 0x7F
    for char in full_message:
        checksum ^= ord(char)

    # Append CR and checksum to the command
    full_message += '#0D' + chr(checksum)

    return full_message

def display_two_row_on_rs232_ibis_panel():
    print("eth")
    # message = format_message("Bratislava", "cez Banská Bystrica – Košice – Poprad")

    message = "aA1 Nenastupovat"

    message += '\x0D'

    print('RS232 message:', message)


    ser = serial.Serial(port='COM3', baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                        stopbits=serial.STOPBITS_TWO, timeout=1)

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
            ser.close()


display_two_row_on_rs232_ibis_panel()