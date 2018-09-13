from enum import IntEnum


# Constants
# Protocol Types
class MQTTProtocol(IntEnum):
    MQTTv31 = 3
    MQTTv311 = 4


# Message types
class ControlType(IntEnum):
    CONNECT = 1         # 0x10
    CONNACK = 2         # 0x20
    PUBLISH = 3         # 0x30
    PUBACK = 4          # 0x40
    PUBREC = 5          # 0x50
    PUBREL = 6          # 0x60
    PUBCOMP = 7         # 0x70
    SUBSCRIBE = 8       # 0x80
    SUBACK = 9          # 0x90
    UNSUBSCRIBE = 10    # 0xA0
    UNSUBACK = 11       # 0xB0
    PINGREQ = 12        # 0xC0
    PINGRESP = 13       # 0xD0
    DISCONNECT = 14     # 0xE0
