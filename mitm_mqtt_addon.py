import logging
from datetime import datetime
from mitmproxy import ctx, tcp
from messages import MQTTPacket
from variable_headers import PublishHeader
from csv import writer


def log_to_file(csv_writer, packet: MQTTPacket, client_ip: str, server_ip: str, direction: str, timestamp: datetime):
    # Compose the CSV line
    # Timestamp, Direction, MessageType, MessagePayload, Client IP, Server IP
    data = None
    if hasattr(packet.payload, 'data'):
        data = packet.payload.data.decode()
    csv_entry = [timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"), direction, packet.header.control_packet_type.name, data, client_ip, server_ip]
    csv_writer.writerow(csv_entry)


class MqttPacketDissector:
    def __init__(self):
        self.num = 0

    def load(self, entry):
        self.fd = open("mqtt.csv", "wt")
        self.writer = writer(self.fd)

    def done(self):
        self.fd.close()

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

            topic_info = ""
            if isinstance(packet.vheader, PublishHeader):
                topic_info = f"Topic: {packet.vheader.topic_name}\n"

            direction = f"{client} -> {server} " if message.from_client else f"{server} -> {client}"
            timestamp = datetime.now()
            log_msg = f"---------------------------\nDIRECTION: {direction}\n" \
                      f"timestamp: {timestamp}\n" \
                      f"{topic_info}" \
                      f"{packet.inline_str()}\n---------------------------\n"
            ctx.log.info(log_msg)
            log_to_file(self.writer, packet, client, server, direction, timestamp)

        except:
            logging.exception("Error")
            pass


addons = [
    MqttPacketDissector()
]
