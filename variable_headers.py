import struct
from myutils import Byte, parse_utf8_prefixed_string
from protocol_constants import ControlType


class VariableHeader(object):
    length = 0

    @staticmethod
    def parse(
            contorl_type,   # type:ControlType
            hedaer_data
    ):
        if contorl_type == ControlType.CONNECT:
            return ConnHeader(hedaer_data)
        else:
            raise Exception("Not Implemented")


class ConnHeader(VariableHeader):
    class ConnectionFlags(object):
        user_name = 0
        password = 0
        will_retain = 0
        will_qos = 0
        will = 0
        clean_session = 0
        reserved = 0

        def __str__(self):
            return str(self.__dict__)

    protocol_name = None
    protocol_level = None
    connect_flags = ConnectionFlags()
    keep_alive = None

    def __init__(self, data):
        cursor = 0

        # Parse the protocol name: it's a UTF-8 string, prepended with a 2 bytes length
        self.protocol_name, data_len = parse_utf8_prefixed_string(data[cursor:])
        cursor += data_len

        # The following byte is the Protocol Level. For MQTT 3.1.1 should be 0x04
        self.protocol_level = data[cursor]
        cursor += 1

        # Connection flags
        flags = Byte(data[cursor]).binary
        cursor += 1

        # Populate connection flags
        self.connect_flags.clean_session = flags[1] == '1'
        self.connect_flags.will = flags[2] == '1'
        self.connect_flags.will_qos = flags[3:5]
        self.connect_flags.will_retain = flags[5] == '1'
        self.connect_flags.user_name = flags[7] == '1'
        self.connect_flags.password = flags[6] == '1'

        # Keep Alive
        self.keep_alive = struct.unpack(">H", data[cursor:cursor+2])[0]
        cursor +=2

        self.length = cursor

    def __str__(self):
        return "ProtocolName: %s\n" \
               "ProtocolLevel: %s\n" \
               "ConnectionFlags: %s\n" \
               "KeepAlive: %d" % (str(self.protocol_name), str(self.protocol_level), str(self.connect_flags), self.keep_alive)
