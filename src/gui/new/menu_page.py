from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QMessageBox


class MainMenuPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        title_label = QLabel("ChatRoom")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 36px;")
        layout.addWidget(title_label)

        layout.addSpacing(150)

        button_layout = QVBoxLayout()
        self.join_button = QPushButton("Join")
        self.join_button.setToolTip("Join a chat")
        self.join_button.clicked.connect(self.parent.show_login)
        self.join_button.setFixedHeight(80)
        self.join_button.setStyleSheet(
            "height: 40px; background-color: #007ACC; color: white; font-weight: bold; font-size: 18px;border-radius: 20px;")
        button_layout.addWidget(self.join_button)


        layout.addLayout(button_layout)


