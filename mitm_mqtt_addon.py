import mitmproxy
from mitmproxy import ctx
from messages import MQTTPacket


class MqttPacketDissector:
    def __init__(self):
        self.num = 0

    def tcp_message(self, flow: mitmproxy.tcp.TCPFlow):
        """
            A TCP connection has received a message. The most recent message
            will be flow.messages[-1]. The message is user-modifiable.
        """
        try:
            message = flow.messages[-1]
            data = MQTTPacket.parse(message)
            ctx.log.info(data)
        except:
            pass


addons = [
    MqttPacketDissector()
]