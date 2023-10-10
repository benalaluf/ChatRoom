__author__ = "Ben"

import socket
import struct
from enum import Enum

# consept for a simple communication protocol info/questions contact iBen

class PacketConstants:

    # packet format
    # 0x/1 byte = type/4 byte = payload length/ payload

    TYPE_HEADER_FORMAT = '>B'  # big-big-endian unsigned char (1 byte)
    PAYLOAD_LENGTH_HEADER_FORMAT = '>I'  # big-endian unsigned int (4 byte)
    HEADER_LENGTH = 5  # bytes
    NO_DATA = b'None'


class PacketType(Enum):
    MSG = 1
    REGISTER = 2
    LOAD_CHAT = 3
    NEW_USER = 4
    DISCONNECT = 255


class Packet:
    def __init__(self, packet_type: PacketType, payload: bytes = PacketConstants.NO_DATA):
        self.packet_type = packet_type
        self.payload = payload
        self.packet_bytes = bytes()

    @classmethod
    def from_bytes(cls, data: bytearray):
        packet_type = PacketType(struct.unpack(PacketConstants.TYPE_HEADER_FORMAT, bytes(data[0:1]))[0])
        data_len = struct.unpack(PacketConstants.PAYLOAD_LENGTH_HEADER_FORMAT, bytes(data[1:5]))[0]
        payload = bytes(data[5:5 + data_len])

        return cls(packet_type, payload)

    def __bytes__(self):
        return self._build_packet()

    def _build_packet(self):
        self.packet_bytes = self._pack(PacketConstants.TYPE_HEADER_FORMAT, self.packet_type.value) + \
                            self._pack(PacketConstants.PAYLOAD_LENGTH_HEADER_FORMAT, (len(self.payload))) + \
                            self.payload
        return self.packet_bytes

    @staticmethod
    def _pack(pack_format: str, data):
        return struct.pack(pack_format, data)


class SendPacket:

    @staticmethod
    def send_packet(sock: socket.socket, packet: Packet):
        sock.sendall(bytes(packet))


class HandelPacket:

    @staticmethod
    def recv_packet(sock):
        return Packet.from_bytes(HandelPacket.__recv_raw_packet(sock))

    @staticmethod
    def __recv_raw_packet(sock):
        raw_header = HandelPacket.__recv_all(sock, PacketConstants.HEADER_LENGTH)

        if not raw_header:
            return None

        raw_data_len = raw_header[1:5]
        data_len = struct.unpack(PacketConstants.PAYLOAD_LENGTH_HEADER_FORMAT, raw_data_len)[0]
        data = HandelPacket.__recv_all(sock, data_len)
        return raw_header + data

    @staticmethod
    def __recv_all(sock, data_len):
        data = bytearray()
        while len(data) < data_len:
            packet = sock.recv(data_len - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
