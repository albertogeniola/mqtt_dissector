from abc import ABC

from myutils import Byte, parse_utf8_prefixed_string
from protocol_constants import ControlType, QoS
from variable_headers import VariableHeader


class Payload(ABC):
    def __init__(self, length):
        self.length = length

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
        elif fixed_header.control_packet_type == ControlType.SUBSCRIBE:
            return SubscribePayload(data)
        elif fixed_header.control_packet_type == ControlType.SUBACK:
            return SubackPayload(data)
        elif fixed_header.control_packet_type == ControlType.UNSUBSCRIBE:
            return SubackPayload(data)
        elif fixed_header.control_packet_type == ControlType.UNSUBACK:
            return EmptyPayload()
        elif fixed_header.control_packet_type == ControlType.PINGREQ:
            return EmptyPayload()
        elif fixed_header.control_packet_type == ControlType.PINGRESP:
            return EmptyPayload()
        elif fixed_header.control_packet_type == ControlType.DISCONNECT:
            return EmptyPayload()
        else:
            raise Exception("Not Implemented")


class EmptyPayload(Payload):
    def __init__(self):
        super().__init__(length=0)

    def __str__(self):
        return ""


class RawPayload(Payload):
    def __init__(self, data):
        super().__init__(length=len(data))
        self.length = len(data)
        self.data = data

    def __str__(self):
        return "%s" % self.data


class ConnPayload(Payload):
    def __init__(self, variable_header, data):
        super().__init__(length=0)

        self.client_identifier = None
        self.will_topic = None
        self.will_message = None
        self.user_name = None
        self.password = None

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

        # Update len
        self.length = cursor

    def __str__(self):
        return "ClientId: %s\n" \
               "WillTopic: %s\n" \
               "WillMessage: %s\n" \
               "Username: %s\n" \
               "Password: %s" % (self.client_identifier, self.will_topic, self.will_message, self.user_name, self.password)


class SubscribePayload(Payload):
    def __init__(self, data):
        super().__init__(length=0)
        self.topics = {}
        cursor = 0

        # The payload of a SUBSCRIBE Packet contains a list of Topic Filters indicating the Topics to which the Client
        # wants to subscribe. The Topic Filters in a SUBSCRIBE packet payload MUST be UTF-8 encoded strings
        # We will scan the whole data byte stream until we parse all the topics.
        while cursor < len(data):
            topic, topic_len = parse_utf8_prefixed_string(data[cursor:])
            cursor += topic_len

            # After each topic name, there is one BYTE that encodes the requested QoS for that topic subscription
            requested_qos = data[cursor]
            cursor += 1
            self.topics[topic] = QoS(requested_qos)

        # Update len
        self.length = cursor

    def __str__(self):
        return "Topics: " + ",".join([( "%s (%s)" % (x, self.topics[x])) for x in self.topics])


class SubackPayload(Payload):
    def __init__(self, data):

        super().__init__(length=0)
        self.return_codes = []
        self.return_codes_description = []
        cursor = 0
        for b in data:
            return_code = Byte(b).binary
            self.return_codes.append(return_code)

            if b'\x00' == b:
                self.return_codes_description.append("Success - Maximum QoS 0")
            elif b'\x01' == b:
                self.return_codes_description.append("Success - Maximum QoS 1")
            elif b'\x02' == b:
                self.return_codes_description.append("Success - Maximum QoS 2")
            elif b'\x80' == b:
                self.return_codes_description.append("Failure")
            else:
                self.return_codes_description.append("INVALID / Unrecognized code")

            cursor += 1

        # Update len
        self.length = cursor

    def __str__(self):
        res = "Return codes: "
        for i in range(0, len(self.return_codes)):
            res += "%s (%s)," % (self.return_codes[i], self.return_codes_description[i])
        return res


class UnsubscribePayload(Payload):
    def __init__(self, data):
        super().__init__(length=0)
        self.topics = []
        cursor = 0
        while cursor<len(data):
            topic, topic_len = parse_utf8_prefixed_string(data[cursor:])
            self.topics.append(topic)
            cursor += topic_len

        # Update len
        self.length = cursor

    def __str__(self):
        return "Topics: %s" % ",".join(self.topics)