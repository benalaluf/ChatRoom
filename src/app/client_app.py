import sys
import threading

import qdarktheme
from PyQt5.QtWidgets import QApplication

from src.connections.client_conn import ClientConn
from src.gui.new.chat_page import MessageDelegate
from src.gui.new.client_gui import ClientGUI
from src.protocol.protocol import Packet, PacketType


class ClientApp(ClientConn):

    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.app = QApplication(sys.argv)
        qdarktheme.setup_theme()
        self.client_gui = ClientGUI()
        self.connect_front_to_back()

    def main(self):
        threading.Thread(target=super().main).start()
        self.run_gui()

    def connect_front_to_back(self):
        self.client_gui.login_page.login_button.clicked.connect(self._app_register)
        self.client_gui.chat_page.send_button.clicked.connect(self._send)

    def handle_packet(self, packet: Packet):
        if packet.packet_type == PacketType.MSG:
            self.client_gui.chat_page.add_msg_to_chat([packet.payload.decode()])
            print(packet.payload.decode())

        if packet.packet_type == PacketType.LOAD_CHAT:
            print('received chat history')
            chat = packet.payload.decode()
            chat = chat.split('\n')[:-1]
            self.client_gui.chat_page.add_msg_to_chat(chat)

        if packet.packet_type == PacketType.NEW_USER:
            payload = packet.payload.decode().split(':')
            username = payload[0]
            color = payload[1]
            MessageDelegate.update_usernames_color(username, color)
            print('new client', username, color)

    def run_gui(self):
        self.client_gui.show()
        sys.exit(self.app.exec_())

    def _send(self):
        message = self.client_gui.chat_page.get_input_text()
        self.send_message(message)

    def _app_register(self):
        username = self.client_gui.login_page.username_field.text()
        color = self.client_gui.login_page.color_field.text()
        super().register(username, color)
        self.client_gui.chat()
