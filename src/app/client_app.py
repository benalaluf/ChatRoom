import sys

import qdarktheme
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication

from src.connections.client_conn import ClientConn
from src.gui.client_gui import ClientGUI
from src.protocol.protocol import Packet, PacketType


class ClientApp:

    def __init__(self, ip, port):
        self.app = QApplication(sys.argv)
        qdarktheme.setup_theme()

        self.client_conn = ClientConn(ip, port)
        self.client_gui = ClientGUI()

        self.client_conn.expand_handle_packet(self.handle_packet)
        self.client_gui.connect_client_conn(self.client_conn)
        self.connect_buttons()

        self.mute = False

    def main(self):
        self.run_gui()

    def run_gui(self):
        self.client_gui.show()
        sys.exit(self.app.exec_())

    def handle_packet(self, packet: Packet):
        if packet.packet_type == PacketType.MSG:
            self.client_gui.chat_page.add_msg_to_chat([packet.payload.decode()]) #todo make to func
            print(packet.payload.decode())

        if packet.packet_type == PacketType.PRIVATE:
            self.client_gui.chat_page.add_msg_to_chat([packet.payload.decode()])  # todo make to func
            print(packet.payload.decode())

        if packet.packet_type == PacketType.USER_DISCONNECTED:
            payload = packet.payload.decode()
            payload = payload.split(":")
            self.client_gui.chat_page.add_msg_to_chat([f"*{payload[0]} Left"])

        if packet.packet_type == PacketType.LOAD_CHAT:
            print('received chat history')
            chat = packet.payload.decode()
            chat = chat.split('\n')[:-1]
            self.client_gui.chat_page.add_msg_to_chat(chat)

        if packet.packet_type == PacketType.KICK:
            self.on_kick()

        if packet.packet_type == PacketType.MUTE:
            self.on_mute()

    def connect_buttons(self):
        self.client_gui.login_page.login_button.clicked.connect(self.login_to_chat)
        self.client_gui.chat_page.send_button.clicked.connect(self._send)

        self.client_gui.admin_page.mute_button.clicked.connect(self._mute)
        self.client_gui.admin_page.kick_button.clicked.connect(self._kick)
        self.client_gui.admin_page.admin_button.clicked.connect(self._make_admin)

    def login_to_chat(self):
        self.client_conn.connect_to_server()
        self.client_conn.main()

        username = self.client_gui.login_page.username_field.text()
        color = self.client_gui.login_page.color_field.text()

        if color == '' or color is None:
            color = QColor(hash(username) % 256, hash(username + "color") % 256, hash(username + "text") % 256)
            color = color.name()

        self.client_conn.register(username, color)
        self.client_gui.show_chat()

    def _send(self):
        message = self.client_gui.chat_page.get_input_text()
        if message == '!quit':
            self.client_conn.quit()
            self.client_gui.show_menu()
        elif not self.mute:
            if message[0] == '!':
                self.client_conn.send_private_message(message)
            else:
                self.client_conn.send_message(message)

    def _kick(self):
        user = self.client_gui.admin_page.get_user()
        self.client_conn.kick(user.text())
        self.client_gui.show_chat()

    def _mute(self):
        user = self.client_gui.admin_page.get_user()
        self.client_conn.mute(user.text())
        self.client_gui.show_chat()

    def _make_admin(self):
        user = self.client_gui.admin_page.get_user()
        self.client_conn.make_admin(user.text())
        self.client_gui.show_chat()

    def on_kick(self):
        print("you have been kicked!!")
        self.client_gui.show_kick()

    def on_mute(self):
        print("you have been muted!!")
        self.client_gui.chat_page.set_muted()
        self.mute = True
