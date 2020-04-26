import logging

from mitmproxy import ctx, tcp

from messages import MQTTPacket


class MqttPacketDissector:
    def __init__(self):
        self.num = 0

    def tcp_message(self, flow: tcp.TCPFlow):
        """
            A TCP connection has received a message. The most recent message
            will be flow.messages[-1]. The message is user-modifiable.
        """
        try:
            message = flow.messages[-1]
            packet = MQTTPacket.parse(message.content)

            client = f"client ({flow.client_conn.address})"
            server = f"server ({flow.server_conn.address})"

            direction = f"{client} -> {server} " if message.from_client else f"{server} -> {client}"

            log_msg = f"---------------------------\nDIRECTION: {direction}\n{packet.inline_str()}\n---------------------------\n"
            ctx.log.info(log_msg)
        except:
            logging.exception("Error")
            pass

addons = [
    MqttPacketDissector()
]