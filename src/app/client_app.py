import threading

from src.connections.client_conn import ClientConn
from src.gui.main import ClientGUI, MessageDelegate
from src.protocol.protocol import Packet, PacketType


class ClientApp(ClientConn, ClientGUI):

    def __init__(self, ip, port):
        ClientConn.__init__(self, ip, port)
        ClientGUI.__init__(self)

    def handle_packet(self, packet: Packet):
        if packet.packet_type == PacketType.MSG:
            self.addMessageToGUI([packet.payload.decode()])
            print(packet.payload.decode())

        if packet.packet_type == PacketType.LOAD_CHAT:
            print('received chat history')
            chat = packet.payload.decode()
            chat = chat.split('\n')
            self.addMessageToGUI(chat)

        if packet.packet_type == PacketType.NEW_USER:
            payload = packet.payload.decode().split(':')
            username = payload[0]
            color = payload[1]
            MessageDelegate.update_usernames_color(username, color)
            print('new client', username, color)

    def send(self):
        message = self.get_input_text()
        self.send_message(message)


    def main(self):
        username= input()
        color = input()
        ClientConn.register(self, username,color)
        ClientConn.main(self)
        ClientGUI.run(self)