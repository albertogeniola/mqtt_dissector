from variable_headers import VariableHeader
from payloads import Payload
from fixed_headers import FixedHeader


class MQTTPacket(object):
    header = None  # type:FixedHeader
    vheader = None
    payload = None

    @staticmethod
    def parse(data):
        res = MQTTPacket()
        cursor = 0

        # Parse the fixed header. The fixed header is 2 bytes long
        res.header = FixedHeader.parse(data[cursor:])
        cursor += res.header.length

        # Parse the variable header.
        res.vheader = VariableHeader.parse(res.header, data[cursor:])
        cursor += res.vheader.length

        # Parse the payload
        res.payload = Payload.parse(res.header, res.vheader, data[cursor:])

        return res

    def __str__(self):
        return "================================\n" \
               "-----------FIXED HEADER---------\n" \
               "[Length]: %d bytes\n" \
               "%s\n" \
               "--------VARIABLE HEADER---------\n" \
               "[Length]: %d bytes\n" \
               "%s\n" \
               "------------PAYLOAD-------------\n" \
               "[Length]: %d bytes\n" \
               "%s\n" \
               "================================\n" % (self.header.length, str(self.header), self.vheader.length,  str(self.vheader), self.payload.length, str(self.payload))


if __name__ == '__main__':
    # Interpret the message as binary data
    data = [
        b"\x10\x7f\x00\x04MQTT\x04\xc2\x00\x1e\x008fmware:18050329735693251a0234298f1178ce_K6sC3PCs9b360000\x00\x1134:29:8f:11:78:ce\x00&46884_858d2e3a3a1aab502657d3a0473d95f3",
        b" \x02\x00\x00",
        b"\x82:\x00\x02\x005/appliance/18050329735693251a0234298f1178ce/subscribe\x01",
        b'2\xe5\x02\x003/appliance/18050329735693251a0234298f1178ce/publish\x00\x03{"header":{"messageId":"d19e855336c00c455de6f3aa1216bcfb","namespace":"Appliance.System.Clock","method":"PUSH","payloadVersion":1,"from":"/appliance/18050329735693251a0234298f1178ce/publish","timestamp":9,"timestampMs":530,"sign":"75655abdc21d99d5d11188ef86c946e0"},"payload":{"clock":{"timestamp":9}}}']

    for p in data:
        packet = MQTTPacket.parse(p)
        print(packet)

    # Missing:
    # At http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718039
    # From 3.8 SUBSCRIBE.

