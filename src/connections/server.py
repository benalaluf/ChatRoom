__author__ = 'Ben'

import socket
import threading

from src.protocol.client_data import ClientData
from src.protocol.protocol import SendPacket, Packet, PacketType, HandelPacket
from src.gui.main import ChatGUI


class Server:

    def __init__(self, ip: str, port: int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)
        self.server.bind(self.addr)

        self.connected_clients = list()

        self.chat_messages = list()

        self.mutex = threading.Lock()

    def main(self):
        self.accept_connections()

    def accept_connections(self):
        self.server.listen()
        print(f'Listening... {self.addr}')
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handel_connection, args=(conn, addr)).start()
            print(f'connection from: {addr}')

    def broadcast(self, packet: Packet):
        for client in self.connected_clients:
            SendPacket.send_packet(client.conn, packet)

    def handel_connection(self, conn: socket.socket, addr):
        packet = HandelPacket.recv_packet(conn)
        if packet.packet_type == PacketType.REGISTER:
            payload = packet.payload.decode().split(':')
            username = payload[0]
            color = payload[1]

            client = ClientData(conn, addr, username, color)
            self.connected_clients.append(client)

            threading.Thread(target=self.handel_client, args=(client,)).start()

            packet = Packet(PacketType.NEW_USER, f'{username}:{color}'.encode())
            self.broadcast(packet)

            self.load_chat(client)

            print(f'New Client: {payload, addr}')

        else:
            print(f'refuse to register: {addr}')
            conn.close()

    def handel_packet(self, packet: Packet, client: ClientData):
        if packet.packet_type == PacketType.MSG:
            message = f'{client.username}: {packet.payload.decode()}'

            self.mutex.acquire()
            self.chat_messages.append(message)
            self.mutex.release()

            packet = Packet(PacketType.MSG, message.encode())
            self.broadcast(packet)

        if packet.packet_type == PacketType.LOAD_CHAT:
            self.load_chat(client)


    def handel_client(self, client: ClientData):
        while True:
            try:
                packet = HandelPacket.recv_packet(client.conn)

                self.handel_packet(packet, client)

            except Exception:
                print(f"{client.username}: Left")
                self.connected_clients.remove(client)
                client.conn.close()


    def load_chat(self, client: ClientData):
        if len(self.chat_messages) > 0:
            chat_history = ''
            for line in self.chat_messages:
                chat_history += line + '\n'
            packet = Packet(PacketType.LOAD_CHAT, chat_history.encode())
            SendPacket.send_packet(client.conn, packet)

        for user in self.connected_clients:
            packet = Packet(PacketType.NEW_USER, f'{user.username}:{user.color}'.encode())
            SendPacket.send_packet(client.conn, packet)
            print(packet.payload.decode(), client.username)