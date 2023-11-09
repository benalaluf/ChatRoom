__author__ = 'Ben'

import threading
from abc import ABC, abstractmethod

from src.gui.main import MessageDelegate, ClientGUI
from src.protocol.client_data import ServerClientData, ClientClientData
from src.protocol.protocol import *
from src.utils.check_color import check_color


class ClientConn:

    def __init__(self, ip: str, port: int):
        self.server_addr = (ip, port)
        self.handle_packet_expansion = None
        self.username = None
        self.color = None


    def main(self):
        print("test")
        threading.Thread(target=self.receive).start()

    def init_client_conn(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connected_clients = list()
        self.was_connected_clients = list()

        self.is_muted = False

    def expand_handle_packet(self, handle_packet_func):
        self.handle_packet_expansion = handle_packet_func

    def connect_to_server(self):
        self.init_client_conn()
        try:
            self.client.connect(self.server_addr)
            print(f'CONNECTED {self.server_addr}')
            self.connected = True

        except Exception as e:
            self.client.close()
            print(e)

    def register(self, username, color):
        register = f"{username}:{color}"
        packet = Packet(PacketType.REGISTER, register.encode())
        SendPacket.send_packet(self.client, packet)
        self.username = username
        self.color = color

    def receive(self):
        while self.connected:
            try:
                packet = HandelPacket.recv_packet(self.client)
                self.handle_packet(packet)
            except Exception:
                print("disconnecting")
                break
        self.client.close()

    def handle_packet(self, packet: Packet):
        if packet.packet_type == PacketType.NEW_USER:
            self._new_user(packet)

        if packet.packet_type == PacketType.USER_DISCONNECTED:
            self._user_dissconnected(packet)

        if self.handle_packet_expansion:
            self.handle_packet_expansion(packet)

    def send_message(self, msg: str):
        packet = Packet(PacketType.MSG, msg.encode())
        SendPacket.send_packet(self.client, packet)

    def send_private_message(self, msg:str):
        msg = msg[1:]
        msg = msg.split(": ")
        msg=f"!{self.username},{msg[0]}:{msg[1]}"
        packet = Packet(PacketType.PRIVATE, msg.encode())
        SendPacket.send_packet(self.client, packet)

    def mute(self, username: str):
        packet = Packet(PacketType.MUTE, username.encode())
        SendPacket.send_packet(self.client, packet)

    def make_admin(self, username: str):
        packet = Packet(PacketType.MAKE_ADMIN, username.encode())
        SendPacket.send_packet(self.client, packet)

    def kick(self, username: str):
        packet = Packet(PacketType.KICK, username.encode())
        SendPacket.send_packet(self.client, packet)

    def quit(self):
        self.connected = False
        packet = Packet(PacketType.DISCONNECT)
        SendPacket.send_packet(self.client, packet)
        self.client.close()


    def _new_user(self, packet: Packet):
        payload = packet.payload.decode().split(':')
        username = payload[0]
        color = payload[1]

        new_client = ClientClientData(username, color)
        if new_client not in self.connected_clients:
            self.connected_clients.append(new_client)

    def _user_dissconnected(self, packet: Packet):
        payload = packet.payload.decode().split(':')
        username = payload[0]
        color = payload[1]

        old_client = ClientClientData(username, color)
        self.connected_clients.remove(old_client)
        self.was_connected_clients.append(old_client)
