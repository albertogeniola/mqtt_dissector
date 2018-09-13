
from myutils import Byte, parse_utf8_prefixed_string
from variable_headers import VariableHeader, ConnHeader
from protocol_constants import ControlType


class Payload(object):
    length = 0

    @staticmethod
    def parse(
            fixed_header,     # type:FixedHeader
            variable_header,  # type:VariableHeader
            data
    ):
        if fixed_header.control_packet_type == ControlType.CONNECT:
            return ConnPayload(variable_header, data)
        elif fixed_header.control_packet_type == ControlType.CONNACK:
            return EmptyPayload()
        elif fixed_header.control_packet_type == ControlType.PUBLISH:
            return RawPayload(data[:fixed_header.remaining_length - variable_header.length])
        elif fixed_header.control_packet_type == ControlType.PUBACK:
            return EmptyPayload()
        elif fixed_header.control_packet_type == ControlType.PUBREC:
            return EmptyPayload()
        elif fixed_header.control_packet_type == ControlType.PUBREL:
            return EmptyPayload()
        elif fixed_header.control_packet_type == ControlType.PUBCOMP:
            return EmptyPayload()
        else:
            raise Exception("Not Implemented")


class EmptyPayload(Payload):
    def __init__(self):
        self.length = 0

    def __str__(self):
        return ""


class RawPayload(Payload):
    data = None
    def __init__(self, data):
        self.length = len(data)
        self.data = data

    def __str__(self):
        return "%s" % self.data


class ConnPayload(Payload):
    client_identifier = None
    will_topic = None
    will_message = None
    user_name = None
    password = None

    def __init__(self,
                 variable_header,  # type:ConnHeader
                 data):
        cursor = 0

        # The payload of the CONNECT Packet contains one or more length-prefixed fields, whose presence is
        # determined by the flags in the variable header. These fields, if present, MUST appear in the order
        # Client Identifier, Will Topic, Will Message, User Name, Password [MQTT-3.1.3-1].
        # Client identifier
        self.client_identifier, field_len = parse_utf8_prefixed_string(data[cursor:])
        cursor += field_len

        if variable_header.connect_flags.will:
            self.will_topic, field_len = parse_utf8_prefixed_string(data[cursor:])
            cursor += field_len

            self.will_message, field_len = parse_utf8_prefixed_string(data[cursor:])
            cursor += field_len

        if variable_header.connect_flags.user_name:
            self.user_name, field_len = parse_utf8_prefixed_string(data[cursor:])
            cursor += field_len

        if variable_header.connect_flags.password:
            self.password, field_len = parse_utf8_prefixed_string(data[cursor:])
            cursor += field_len

        self.length = cursor

    def __str__(self):
        return "ClientId: %s\n" \
               "WillTopic: %s\n" \
               "WillMessage: %s\n" \
               "Username: %s\n" \
               "Password: %s" % (self.client_identifier, self.will_topic, self.will_message, self.user_name, self.password)
