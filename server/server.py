import socket
import threading
from asyncio import Queue

from protocol.protocol import SendPacket, Packet, PacketType, HandelPacket


class Server:

    def __init__(self, ip: str, port: int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ADDR = (ip, port)

        self.server.bind(self.ADDR)

        self.connected_clients_nicknames = dict()
        self.connected_clients = list()

        self.chat_messages = list()

        self.mutex = threading.Lock()

    def start(self):
        pass

    def broadcast(self, packet: Packet):
        for client in self.connected_clients:
            SendPacket.send_packet(client, packet)

    def accept_connections(self):
        self.server.listen()
        print(f'start listening at {self.ADDR}')
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handel_connection, args=(conn, addr)).start()
            print(f'connection from: {addr}')

    def handel_connection(self, conn: socket.socket, addr):
        packet = Packet(PacketType.REGISTER, "register".encode())
        SendPacket.send_packet(conn, packet)
        packet_type, response = HandelPacket.recv_packet(conn)
        if packet_type == PacketType.REGISTER.value:
            nickname = response.decode()
            self.connected_clients.append(conn)
            self.connected_clients_nicknames.update({str(conn): nickname})
            threading.Thread(target=self.handel_client, args=(conn,)).start()
            print(f'new client: {addr}')

        else:
            print(f'refuse to register: {addr}')
            conn.close()

    def handel_client(self, conn: socket.socket):
        while True:
            try:
                packet_type, payload = HandelPacket.recv_packet(conn)

                if packet_type == PacketType.MSG.value:
                    message = f'{self.connected_clients_nicknames[str(conn)]}: {payload.decode()}'

                    self.mutex.acquire()
                    self.chat_messages.append(message)
                    self.mutex.release()

                    packet = Packet(PacketType.MSG, message.encode())
                    self.broadcast(packet)

                if packet_type == PacketType.LOAD_CHAT.value:
                    if len(self.chat_messages) > 0 :
                        chat_history = ''
                        for line in self.chat_messages:
                            chat_history += line + '\n'
                        packet = Packet(PacketType.LOAD_CHAT, chat_history.encode())
                        SendPacket.send_packet(conn, packet)

            except Exception:
                print(conn.getpeername(), "left")
                self.connected_clients.remove(conn)
                self.connected_clients_nicknames.pop(str(conn))
                conn.close()


if __name__ == '__main__':
    server = Server('localhost', 4343)
    server.accept_connections()
