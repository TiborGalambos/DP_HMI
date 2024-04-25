import serial
import time

def format_message(upper_row, lower_row):
    # Base command for panel with address 1; change as needed
    command = 'aA1 '

    # Control sequence and command to set up the display attributes
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

    message_upper = f"aA1 {upper_message}"
    message_upper += '\x0D'

    message_lower = f'aA1 \x0A\x1Bx\x1Bd\x10\x1Bh\x19\x1Bt\x11{lower_message}'
    message_lower += '\x0D'

    print('RS232 message lower:', message_lower)

    ser = serial.Serial(port='COM3', baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
                        stopbits=serial.STOPBITS_TWO, timeout=1)

    message_lower = message_lower.encode()
    checksum = 0
    for byte in message_lower:
        checksum ^= byte
    checksum = 0x7F & ~checksum
    checksum_byte = chr(checksum).encode()
    message_lower += checksum_byte
    message_lower += b'\r'

    try:
        print(message_lower)
        ser.write(message_lower)

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