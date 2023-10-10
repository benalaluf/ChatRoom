__author__ = 'Ben'

import threading
from abc import ABC, abstractmethod

from src.gui.main import MessageDelegate, ClientGUI
from src.protocol.client_data import ClientData
from src.protocol.protocol import *
from src.utils.check_color import check_color


class ClientConn(ABC):

    def __init__(self, ip: str, port: int):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (ip, port)
        self.connect_to_server()

    def main(self):
        threading.Thread(target=self.receive).start()

    def connect_to_server(self):
        try:
            self.client.connect(self.server_addr)
            print(f'CONNECTED {self.server_addr}')
        except Exception as e:
            self.client.close()
            print(e)

    def register(self, username, color):
        register = f"{username}:{color}"
        packet = Packet(PacketType.REGISTER, register.encode())
        SendPacket.send_packet(self.client, packet)

    def receive(self):
        while True:
            packet = HandelPacket.recv_packet(self.client)
            self.handle_packet(packet)

    def send_message(self, msg: str):
        packet = Packet(PacketType.MSG, msg.encode())
        SendPacket.send_packet(self.client, packet)

    @abstractmethod
    def handle_packet(self, packet: Packet):
        if packet.packet_type == PacketType.MSG:
            print(packet.payload.decode())

        if packet.packet_type == PacketType.LOAD_CHAT:
            print('received chat history')
            chat = packet.payload.decode()
            chat = chat.split('\n')

        if packet.packet_type == PacketType.NEW_USER:
            payload = packet.payload.decode().split(':')
            username = payload[0]
            color = payload[1]
            MessageDelegate.update_usernames_color(username, color)
            print('new client', username, color)
