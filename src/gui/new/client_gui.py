import sys

import qdarktheme
from PyQt5.QtWidgets import QApplication, QMainWindow,QVBoxLayout, QWidget, QStackedWidget

from src.gui.new.chat_page import ChatPage
from src.gui.new.login_page import LoginPage
from src.gui.new.menu_page import MainMenuPage


class ClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.menu_page = MainMenuPage(self)
        self.login_page = LoginPage(self)
        self.chat_page = ChatPage(self)
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle("ChatRoom")
        self.setGeometry(100, 100, 600, 800)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.stacked_widget = QStackedWidget()

        central_layout = QVBoxLayout()
        central_layout.addWidget(self.stacked_widget)

        central_widget.setLayout(central_layout)

        self.stacked_widget.addWidget(self.menu_page)

        self.stacked_widget.addWidget(self.chat_page)

        self.stacked_widget.addWidget(self.login_page)



    def login(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def chat(self):
        self.stacked_widget.setCurrentWidget(self.chat_page)

    def host(self):
        self.stacked_widget.setCurrentWidget(self.host_page)

    def show_menu(self):
        self.stacked_widget.setCurrentWidget(self.menu_page)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = ClientGUI()
    window.show()

    sys.exit(app.exec_())
