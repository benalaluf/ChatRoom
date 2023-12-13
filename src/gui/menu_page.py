import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication


class MainMenuPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel("ChatRoom")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 36px; color: white; font-weight: bold;")
        layout.addWidget(title_label)

        layout.addSpacing(60)

        button_layout = QVBoxLayout()
        self.join_button = QPushButton("Join")
        self.join_button.setToolTip("Join a chat")
        self.join_button.clicked.connect(self.parent.show_login)
        self.join_button.setFixedHeight(80)
        self.join_button.setStyleSheet(
            "height: 40px; background-color: #007ACC; color: white; font-weight: bold; font-size: 18px;border-radius: 20px;"
        )
        button_layout.addWidget(self.join_button)

        layout.addLayout(button_layout)

        background_image_path = 'images/macos.jpeg'
        background = QPixmap(background_image_path)

        if not background.isNull():
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(background))
            self.setPalette(palette)
        else:
            print(f"Error: Could not load the image from {background_image_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenuPage(None)
    main_menu.show()
    sys.exit(app.exec_())
