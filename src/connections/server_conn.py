__author__ = 'Ben'

import socket
import threading

from src.protocol.client_data import ServerClientData
from src.protocol.protocol import SendPacket, Packet, PacketType, HandelPacket


class Server:

    def __init__(self, ip: str, port: int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)
        self.server.bind(self.addr)

        self.connected_clients = list()
        self.was_connected_clients = list()

        self.chat_messages = list()

        self.admins = ['ben', 'admin']
        self.muted = list()

        self.mutex = threading.Lock()

    def main(self):
        self.accept_connections()

    def accept_connections(self):
        self.server.listen()
        print(f'Listening... {self.addr}')
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handel_connection, args=(conn, addr)).start()

    def handel_connection(self, conn: socket.socket, addr):
        packet = HandelPacket.recv_packet(conn)
        if packet.packet_type == PacketType.REGISTER:
            payload = packet.payload.decode().split(':')
            username = payload[0]
            color = payload[1]

            client = ServerClientData(conn, addr, username, color)
            self.connected_clients.append(client)

            threading.Thread(target=self.handel_client, args=(client,)).start()

            packet = Packet(PacketType.NEW_USER, f'{username}:{color}'.encode())
            self._broadcast(packet)

            self._load_chat(client)

            message = f"*{client.username} joined"
            print(message)
            self.chat_messages.append(message)
            packet = Packet(PacketType.MSG, payload=message.encode())
            self._broadcast(packet)

        else:
            print(f'refuse to register: {addr}')
            conn.close()

    def handel_client(self, client: ServerClientData):
        while client in self.connected_clients:
            try:
                packet = HandelPacket.recv_packet(client.conn)

                self.handel_packet(packet, client)

            except Exception:
                self.client_dissconnected(client)
                break

    def handel_packet(self, packet: Packet, client: ServerClientData):
        if packet.packet_type == PacketType.MSG:
            self._handle_msg(packet, client)

        if packet.packet_type == PacketType.LOAD_CHAT:
            self._load_chat(client)

        if packet.packet_type == PacketType.KICK:
            self.kick_client(packet, client)

        if packet.packet_type == PacketType.MUTE:
            self.mute_client(packet, client)

        if packet.packet_type == PacketType.MAKE_ADMIN:
            self._make_admin(packet, client)

        if packet.packet_type == PacketType.DISCONNECT:
            self.client_dissconnected(client)

        if packet.packet_type == PacketType.PRIVATE:
            self._private_message(packet, client)

    def _broadcast(self, packet: Packet):
        for client in self.connected_clients:
            SendPacket.send_packet(client.conn, packet)

    def _handle_msg(self, packet: Packet, client: ServerClientData):
        if client.username in self.admins:
            message = f'@{client.username}: {packet.payload.decode()}'
        else:
            message = f'{client.username}: {packet.payload.decode()}'

        if client in self.connected_clients:
            self.mutex.acquire()
            self.chat_messages.append(message)
            self.mutex.release()

            packet = Packet(PacketType.MSG, message.encode())
            self._broadcast(packet)
            print(message)

    def _make_admin(self, packet: Packet, client: ServerClientData):
        if client.username in self.admins:
            client_to_make_admin = packet.payload.decode()
            for connected_client in self.connected_clients:
                if connected_client.username == client_to_make_admin:
                    self.admins.append(client_to_make_admin)
                    message = f"*{connected_client.username} is now admin"
                    packet = Packet(PacketType.MSG, payload=message.encode())
                    self._broadcast(packet)
                    self.chat_messages.append(message)
                    print(message)

    def _private_message(self, packet: Packet, client_p: ServerClientData):
        msg = packet.payload.decode()
        msg = msg[1:]
        msg = msg.split(":")
        users = msg[0].split(",")
        user_from = users[0]
        user_to = users[1]
        msg = f"!{user_from}: {msg[1]}"
        packet = Packet(PacketType.PRIVATE, msg.encode())
        for client in self.connected_clients:
            if client.username == user_to:
                SendPacket.send_packet(client.conn, packet)
                SendPacket.send_packet(client_p.conn, packet)

    def _load_chat(self, client: ServerClientData):
        if len(self.chat_messages) > 0:
            chat_history = ''
            for line in self.chat_messages:
                chat_history += line + '\n'
            packet = Packet(PacketType.LOAD_CHAT, chat_history.encode())
            SendPacket.send_packet(client.conn, packet)

        for user in self.connected_clients + self.was_connected_clients:
            packet = Packet(PacketType.NEW_USER, f'{user.username}:{user.color}'.encode())
            SendPacket.send_packet(client.conn, packet)

    def kick_client(self, packet: Packet, client: ServerClientData):
        if client.username in self.admins:
            client_to_kick = packet.payload.decode()
            for connected_client in self.connected_clients:
                if connected_client.username == client_to_kick:
                    packet = Packet(PacketType.KICK)
                    SendPacket.send_packet(connected_client.conn, packet)

                    message = f"*{connected_client.username} was kicked"
                    self.remove_client(connected_client)
                    packet = Packet(PacketType.MSG, payload=message.encode())
                    self._broadcast(packet)
                    self.chat_messages.append(message)
                    print(message)

    def mute_client(self, packet: Packet, client: ServerClientData):
        if client.username in self.admins:
            client_to_mute = packet.payload.decode()
            for connected_client in self.connected_clients:
                if connected_client.username == client_to_mute:
                    packet = Packet(PacketType.MUTE)
                    SendPacket.send_packet(connected_client.conn, packet)

                    message = f"*{connected_client.username} is muted"
                    packet = Packet(PacketType.MSG, payload=message.encode())
                    self._broadcast(packet)
                    self.chat_messages.append(message)
                    self.muted.append(client)
                    print(message)

    def client_dissconnected(self, client: ServerClientData):
        msg = f"{client.username}:{client.color}"
        packet = Packet(PacketType.USER_DISCONNECTED, payload=msg.encode())
        self.remove_client(client)
        self._broadcast(packet)
        message = f"*{client.username} Left"
        self.chat_messages.append(message)
        print(message)

    def remove_client(self, client: ServerClientData):
        if client in self.connected_clients:
            self.connected_clients.remove(client)

        if client not in self.was_connected_clients:
            self.was_connected_clients.append(client)
        client.conn.close()
