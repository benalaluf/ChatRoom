__author__ = 'Ben'

import threading
from abc import ABC

from src.gui.main import MessageDelegate, ChatGUI
from src.protocol.protocol import *
from src.utils.check_color import check_color


class Client(ChatGUI):

    def __init__(self, ip: str, port: int):
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (ip, port)
        self.connect_to_server()

    def main(self):
        username, color = self.get_client_credentials()
        register = f"{username}:{color}"
        packet = Packet(PacketType.REGISTER, register.encode())
        SendPacket.send_packet(self.client, packet)
        threading.Thread(target=self.receive).start()
        self.run()

    def connect_to_server(self):
        try:
            self.client.connect(self.server_addr)
            print(f'CONNECTED {self.server_addr}')
        except Exception as e:
            self.client.close()
            print(e)

    def get_client_credentials(self):
        username = input("Please Enter Your Nickname: ")
        color = input("Please Enter Your Color: ")
        if not check_color(color):
            print("Invalid color")
            self.get_client_credentials()
        return username, color

    def receive(self):
        while True:
            packet = HandelPacket.recv_packet(self.client)
            self.handle_packet(packet)

    def send_message(self):
        packet = Packet(PacketType.MSG, self.get_input_text().encode())
        SendPacket.send_packet(self.client, packet)

    def handle_packet(self, packet: Packet):
        if packet.packet_type == PacketType.MSG:
            self.addMessageToGUI(packet.payload.decode())

        if packet.packet_type == PacketType.LOAD_CHAT:
            print('received chat history')
            chat = packet.payload.decode()
            self.addMessageToGUI(chat)

        if packet.packet_type == PacketType.NEW_USER:
            payload = packet.payload.decode().split(':')
            username = payload[0]
            color = payload[1]
            MessageDelegate.update_usernames_color(username, color)
