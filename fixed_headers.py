from myutils import Byte
from protocol_constants import ControlType, QoS


class FixedHeader(object):
    length = 2  # Fixed length of 2 bytes!

    def __init__(self):
        self.control_packet_type = None
        self.flags = 0
        self.formatted_flags = None

        # The Remaining Length is the number of bytes remaining within the current packet, including data in the variable
        # header and the payload. The Remaining Length does not include the bytes used to encode the Remaining Length.
        self.remaining_length = 0

    @staticmethod
    def try_parse(data):
        if len(data) < 2:
            return False, None

        first_byte = Byte(data[0])
        try:
            control_packet_type = ControlType(first_byte._high_nibble())
            if control_packet_type == ControlType.PUBLISH:
                return True, PublishFixedHeader(data)
            # TODO: implement remaining fixed headers?
            else:
                return True, GenericFixedHeader(data)
        except:
            return False, None

    @staticmethod
    def parse(data):
        if len(data) < 2:
            raise Exception("Invalid data. Fixed header should be at least 2 bytes")

        first_byte = Byte(data[0])
        control_packet_type = ControlType(first_byte._high_nibble())

        if control_packet_type == ControlType.PUBLISH:
            return PublishFixedHeader(data)
        else:
            return GenericFixedHeader(data)

    @staticmethod
    def parse_remaining_length(data):
        counter = 0
        multiplier = 1
        value = 0
        while True:
            encodedByte = data[counter]
            value += (encodedByte & 127) * multiplier
            multiplier *= 128

            counter += 1

            if multiplier > (128 * 128 * 128):
                raise Exception("Malformed Remaining Length")
            if not ((encodedByte & 128) != 0):
                break

        return value, counter


class GenericFixedHeader(FixedHeader):
    def __init__(self, data):
        super().__init__()
        first_byte = Byte(data[0])
        self.control_packet_type = ControlType(first_byte._high_nibble())
        self.flags = first_byte._low_nibble()
        self.formatted_flags = first_byte.low_nibble
        self.remaining_length, remaining_length_count = FixedHeader.parse_remaining_length(data[1:])

        self.length = 1 +  remaining_length_count

    def __str__(self):
        res = "Type: %s\n" \
              "Flags: %s\n" \
              "Remaining length: %d" % (self.control_packet_type, self.formatted_flags, self.remaining_length)
        return res


class PublishFixedHeader(GenericFixedHeader):
    dup_flag = None
    qos_level = None  # type:QoS
    retain = None

    def __init__(self, data):
        super().__init__(data)

        self.dup_flag = self.formatted_flags[0] == '1'
        self.qos_level = QoS.parse(self.formatted_flags[1:3])
        self.retain = self.formatted_flags[3] == '1'

    def __str__(self):
        res = "%s\n" \
              "Dup: %s\n" \
              "QoS: %s\n" \
              "Retain: %s" % (super().__str__(), self.dup_flag, self.qos_level, self.retain)
        return res