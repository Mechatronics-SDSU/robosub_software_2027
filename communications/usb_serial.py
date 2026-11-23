from tlv import TLV

import struct
import serial

BAUD_RATE = 115200
PORT = "/dev/ttyACM0"

"""
author: alice vo
discord: @alicvo

wrapper for usb serial transmission of data to the mcu.

the data sent will follow a TLV format as follows:
    - type: 1 byte, unsigned int, indicates the type of data being sent
    - length: 1 byte, unsigned int, indicates the length of the value field
    - value: variable length, the actual data being sent   

TLV ID table:
    MOTOR0 = 0x00
    MOTOR1 = 0x01
    MOTOR2 = 0x02
    MOTOR3 = 0x03
    MOTOR4 = 0x04
    MOTOR5 = 0x05
    MOTOR6 = 0x06
    MOTOR7 = 0x07
    KILL_STATE = 0x08
    POWER_OFF_STATE = 0x09
    SERVO1 = 0x0A
    SERVO2 = 0x0B
    DROPPER = 0x0C
    TORPEDO = 0x0D

"""

class USB:
    def __init__(self, port = PORT, baud_rate = BAUD_RATE):
        self.srl = serial.Serial(port, baud_rate, timeout=1, write_timeout=1)

    def send_data(self, id, data):
        """send tlv data to the mcu"""
        formatted_data = self.format(id, data)
        self.srl.write(formatted_data)

    def format(self, id, data):
        """
        encode integer value as a TLV field.
        
        TLV layout: [Type: 1 byte][Length: 1 byte][Value: Length bytes]
        Length counts only value bytes; multi-byte values use little-endian order.
        Example: MOTOR0 = 1500 -> 00 02 DC 05
        """
        try:
            id = TLV(id)
        except ValueError:
            raise ValueError(f"Unknown TLV type ID: {id}") from None
        is_state = id in (TLV.KILL_STATE, TLV.POWER_OFF_STATE)
        if is_state and data not in (0, 1):
            raise ValueError("State values must be 0 or 1")
        value = struct.pack("<B" if is_state else "<H", data)
        return struct.pack("<BB", id, len(value)) + value

if __name__ == "__main__":
    # example
    usb = USB(port=PORT, baud_rate=BAUD_RATE)
    
    usb.send_data(TLV.KILL_STATE, 0)
