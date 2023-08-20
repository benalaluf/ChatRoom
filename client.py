import socket
import threading

from protocol.protocol import SendPacket, Packet, PacketType, HandelPacket

__author__ = 'iBen'

import socket


class Client:

    def __init__(self, ip: str, port: int):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (ip, port)
        self.nickname = input("Please Enter Your Nickname: ")

    def main(self):
        while True:
            packet_type, payload = HandelPacket.recv_packet(self.client)

            if packet_type == PacketType.MSG.value:
                print(payload.decode())

            if packet_type == PacketType.REGISTER.value:
                packet = Packet(PacketType.REGISTER, self.nickname.encode())
                SendPacket.send_packet(self.client, packet)

                packet = Packet(PacketType.LOAD_CHAT, 'loadchat'.encode())
                SendPacket.send_packet(self.client, packet)

            if packet_type == PacketType.LOAD_CHAT.value:
                chat = payload.decode()
                print(chat)

    def transmit(self):
        while True:
            msg = input()
            packet = Packet(PacketType.MSG, msg.encode())
            SendPacket.send_packet(self.client, packet)

    def start(self):
        try:
            self.client.connect(self.server_addr)
            threading.Thread(target=self.main).start()
            threading.Thread(target=self.transmit).start()
            print('done.')
        except Exception as e:
            self.client.close()
            print(e)


if __name__ == '__main__':
    Client('localhost', 3232).start()