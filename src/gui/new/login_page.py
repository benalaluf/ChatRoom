from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QColorDialog, QPushButton, \
    QGridLayout, QMessageBox


class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.grid = QGridLayout()
        self.parent = parent
        self.username = None
        self.color = None

        self.headline_label = QLabel("Login", self)
        self.headline_label.setStyleSheet("font-size: 36px; font-weight: bold;")
        self.headline_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.headline_label)

        self.username_label = QLabel("Username:", self)
        self.username_label.setStyleSheet("font-size: 18px;")
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Enter your username")

        self.username_field.setStyleSheet("height: 40px; font-size: 18px;")

        self.grid.addWidget(self.username_label, 1, 0, 1, 2)
        self.grid.addWidget(self.username_field, 2, 0, 1, 3)

        self.color_label = QLabel("Color:", self)
        self.color_label.setStyleSheet("font-size: 18px;")
        self.color_field = QLineEdit(self)
        self.color_field.setPlaceholderText("Enter a color name or automatically pick")
        self.color_button = QPushButton('Pick Color', self)
        self.color_button.clicked.connect(self.openColorDialog)
        self.color_button.setFixedHeight(50)

        self.color_field.setStyleSheet("height: 40px; font-size: 18px;")

        self.grid.addWidget(self.color_label, 3, 0, 1, 2)
        self.grid.addWidget(self.color_field, 4, 0, 1, 2)
        self.grid.addWidget(self.color_button, 4, 2, 1, 1)

        self.login_button = QPushButton('Login', self)

        self.login_button.setStyleSheet(
            "height: 40px; background-color: #007ACC; color: white; font-weight: bold; font-size: 18px;")

        self.grid.addWidget(self.login_button, 6, 0, 1, 3)

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)

        self.grid.setRowStretch(8, 1)
        self.layout.addLayout(self.grid)

        self.setLayout(self.layout)



    def openColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            html_color_name = color.name(QColor.HexRgb)
            self.color_field.setText(html_color_name)
