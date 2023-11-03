from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QListWidget

from src.gui.main import MessageDelegate


class AdminPage(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.connected_client = []
        self.setup_ui()


    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        title_label = QLabel("AdminPage")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 36px;")
        layout.addWidget(title_label)

        layout.addSpacing(150)


        self.user_list = QListWidget()
        self.user_list.addItems(self.connected_client)
        layout.addWidget(self.user_list)

        button_layout = QVBoxLayout()

        self.mute_button = QPushButton("Mute")
        self.mute_button.setStyleSheet("color: white; font-size: 24px; "
                                           "border-radius: 10px;")
        self.mute_button.setToolTip("Mute a user")
        self.mute_button.setFixedHeight(80)
        button_layout.addWidget(self.mute_button)


        self.kick_button = QPushButton("Kick")
        self.kick_button.setStyleSheet("color: white; font-size: 24px; "
                                           "border-radius: 10px;")
        self.kick_button.setToolTip("Mute a user")
        self.kick_button.setFixedHeight(80)
        button_layout.addWidget(self.kick_button)

        layout.addLayout(button_layout)


    def get_user(self):
        return self.user_list.currentItem()

    def update_users(self,):
        self.user_list.clear()
        self.user_list.addItems(self.connected_client)
        print(self.connected_client)


