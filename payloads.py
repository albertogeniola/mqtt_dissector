import struct
from myutils import Byte, parse_utf8_prefixed_string
from variable_headers import VariableHeader, ConnHeader
from protocol_constants import ControlType


class Payload(object):
    length = 0

    @staticmethod
    def parse(
            contorl_type,     # type:ControlType
            variable_header,  # type:VariableHeader
            data
    ):
        if contorl_type == ControlType.CONNECT:
            return ConnPayload(variable_header, data)
        else:
            raise Exception("Not Implemented")


class ConnPayload(Payload):
    client_identifier = None
    will_topic = None
    will_message = None
    user_name = None

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

    def __str__(self):
        pass
