from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class KickPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        title_label = QLabel("You Have Been Kicked!!!")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 36px; color: red;")
        layout.addWidget(title_label)

        layout.addSpacing(150)

        button_layout = QVBoxLayout()
        self.back_to_main_menu_button = QPushButton("main menu")
        self.back_to_main_menu_button.setStyleSheet("color: white; font-size: 18px; "
                                           "border-radius: 10px;")
        self.back_to_main_menu_button.setToolTip("Join a chat")
        self.back_to_main_menu_button.clicked.connect(self.parent.show_menu)
        self.back_to_main_menu_button.setFixedHeight(60)
        button_layout.addWidget(self.back_to_main_menu_button)


        layout.addLayout(button_layout)


