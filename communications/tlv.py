from enum import IntEnum

class TLV(IntEnum):
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
