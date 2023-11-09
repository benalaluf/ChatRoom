import sys

import qdarktheme
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QAction

from src.connections.client_conn import ClientConn
from src.gui.new.admin_page import AdminPage
from src.gui.new.chat_page import ChatPage
from src.gui.new.kick_page import KickPage
from src.gui.new.login_page import LoginPage
from src.gui.new.menu_page import MainMenuPage


class ClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.client_conn = None

        self.menu_page = MainMenuPage(self)
        self.login_page = LoginPage(self)
        self.chat_page = ChatPage(self)
        self.admin_page = AdminPage(self)
        self.kick_page = KickPage(self)

        self.stacked_widget = QStackedWidget()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle("ChatRoom")
        self.setGeometry(100, 100, 600, 800)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout()
        central_layout.addWidget(self.stacked_widget)

        central_widget.setLayout(central_layout)

        self.stacked_widget.addWidget(self.menu_page)

        self.stacked_widget.addWidget(self.chat_page)

        self.stacked_widget.addWidget(self.login_page)

        self.stacked_widget.addWidget(self.admin_page)

        self.stacked_widget.addWidget(self.kick_page)

    def connect_client_conn(self, client_conn: ClientConn):
        self.client_conn = client_conn

    def closeEvent(self, event):
        exit(0)

    def show_menu(self):
        self.stacked_widget.setCurrentWidget(self.menu_page)

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_chat(self):
        self.stacked_widget.setCurrentWidget(self.chat_page)

    def show_admin(self):
        self.admin_page.update_users()
        self.stacked_widget.setCurrentWidget(self.admin_page)

    def show_kick(self):
        self.stacked_widget.setCurrentWidget(self.kick_page)


    # def host(self):
    #     self.stacked_widget.setCurrentWidget(self.host_page)

