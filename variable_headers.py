import struct
from myutils import Byte, parse_utf8_prefixed_string
from protocol_constants import ControlType


class VariableHeader(object):
    length = 0

    @staticmethod
    def parse(
            fixed_header, #  type:FixedHeader
            header_data
    ):
        if fixed_header.control_packet_type == ControlType.CONNECT:
            return ConnHeader(header_data)
        elif fixed_header.control_packet_type == ControlType.CONNACK:
            return ConnackHeader(header_data)
        elif fixed_header.control_packet_type == ControlType.PUBLISH:
            return PublishHeader(header_data, fixed_header.qos_level)
        elif fixed_header.control_packet_type == ControlType.PUBREC:
            return PubrecHeader(header_data)
        elif fixed_header.control_packet_type == ControlType.PUBREL:
            return PubrelHeader(header_data)
        elif fixed_header.control_packet_type == ControlType.PUBCOMP:
            return PubcompHeader(header_data)
        elif fixed_header.control_packet_type == ControlType.SUBSCRIBE:
            return SubscribeHeader(header_data)
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
        self.connect_flags.clean_session = flags[6] == '1'
        self.connect_flags.will = flags[5] == '1'
        self.connect_flags.will_qos = flags[3:5]
        self.connect_flags.will_retain = flags[2] == '1'
        self.connect_flags.user_name = flags[0] == '1'
        self.connect_flags.password = flags[1] == '1'

        # Keep Alive
        self.keep_alive = struct.unpack(">H", data[cursor:cursor+2])[0]
        cursor +=2

        self.length = cursor

    def __str__(self):
        return "ProtocolName: %s\n" \
               "ProtocolLevel: %s\n" \
               "ConnectionFlags: %s\n" \
               "KeepAlive: %d" % (str(self.protocol_name), str(self.protocol_level), str(self.connect_flags), self.keep_alive)


class ConnackHeader(VariableHeader):
    session_present = None
    return_code = None
    return_code_desc = None

    _RETURN_CODES = {
        0: "CONNECTION ACCEPTED",
        1: "CONNECTION REFUSED, unacceptable protocol version",
        2: "CONNECTION REFUSED, identifier rejected",
        3: "CONNECTION REFUSED, server unavailable",
        4: "CONNECTION REFUSED, bad username or password",
        5: "CONNECTION REFUSED, not authorized"
    }

    def __init__(self, data):
        # The Connack variable header should be 2 bytes long
        if len(data) != 2:
            #TODO warn if len is different
            pass

        first_byte_flags = Byte(data[0]) # TODO: Warn if some bits 1-7 are not 0
        self.session_present = first_byte_flags.binary[7] == '1'

        self.return_code = data[1]
        self.return_code_desc = self._RETURN_CODES[self.return_code]

    def __str__(self):
        return "Session Present: %s\n" \
               "Return Code: %d (%s)" % (self.session_present, self.return_code, self.return_code_desc)


class PublishHeader(VariableHeader):
    topic_name = None
    packet_identifier = None

    def __init__(self, data, qos):
        cursor = 0

        self.topic_name, data_len = parse_utf8_prefixed_string(data)
        cursor += data_len

        # Packet identifier is present only if QoS > 0
        if qos.value > 0:
            self.packet_identifier = struct.unpack(">H", data[cursor:cursor + 2])[0]
            cursor += 2

        self.length = cursor

    def __str__(self):
        return "Topic Name: %s\n" \
               "Packet Identifier: %d" % (self.topic_name, self.packet_identifier)


class PubackHeader(VariableHeader):
    packet_identifier = None

    def __init__(self, data):
        cursor = 0
        self.packet_identifier = struct.unpack(">H", data[cursor:cursor + 2])[0]
        cursor += 2
        self.length = cursor

    def __str__(self):
        return "Packet Identifier: %d (%s)" % self.packet_identifier


class PubrecHeader(VariableHeader):
    packet_identifier = None

    def __init__(self, data):
        cursor = 0
        self.packet_identifier = struct.unpack(">H", data[cursor:cursor + 2])[0]
        cursor += 2
        self.length = cursor

    def __str__(self):
        return "Packet Identifier: %d" % self.packet_identifier


class PubrelHeader(VariableHeader):
    packet_identifier = None

    def __init__(self, data):
        cursor = 0
        self.packet_identifier = struct.unpack(">H", data[cursor:cursor + 2])[0]
        cursor += 2
        self.length = cursor

    def __str__(self):
        return "Packet Identifier: %d" % self.packet_identifier


class PubcompHeader(VariableHeader):
    packet_identifier = None

    def __init__(self, data):
        cursor = 0
        self.packet_identifier = struct.unpack(">H", data[cursor:cursor + 2])[0]
        cursor += 2
        self.length = cursor

    def __str__(self):
        return "Packet Identifier: %d" % self.packet_identifier


class SubscribeHeader(VariableHeader):
    packet_identifier = None

    def __init__(self, data):
        cursor = 0
        self.packet_identifier = struct.unpack(">H", data[cursor:cursor + 2])[0]
        cursor += 2
        self.length = cursor

    def __str__(self):
        return "Packet Identifier: %d" % self.packet_identifier