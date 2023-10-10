from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QColorDialog, QPushButton, QGridLayout


class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.layout = QGridLayout()
        self.parent = parent
        self.username = None
        self.color = None

        # Headline Label
        self.headline_label = QLabel("Login", self)
        self.headline_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.headline_label, 0, 0, 1, 2)  # Span two columns

        # Username Input
        self.username_label = QLabel("Username:", self)
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("enter your username")

        self.layout.addWidget(self.username_label, 1, 0, 1, 2)  # Span two columns
        self.layout.addWidget(self.username_field, 2, 0, 1, 3)  # Span two columns

        # Color Input
        self.color_label = QLabel("Color:", self)
        self.color_field = QLineEdit(self)
        self.color_field.setPlaceholderText("enter a color name or automatically pick")
        self.color_button = QPushButton('Pick Color', self)
        self.color_button.clicked.connect(self.openColorDialog)  # Connect the button to the dialog
        self.layout.addWidget(self.color_label, 3, 0, 1, 2)  # Span two columns
        self.layout.addWidget(self.color_field, 4, 0, 1, 3)  # Span two columns
        self.layout.addWidget(self.color_button, 4, 2, 1, 1)  # Span two columns

        # Login Button
        self.login_button = QPushButton('Login', self)
        self.layout.addWidget(self.login_button, 6, 0, 1, 3)  # Span two columns

        # Set column stretch to make it symmetrical
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

        # Set row stretch for spacing
        self.layout.setRowStretch(8, 1)

        self.setLayout(self.layout)

    def openColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            html_color_name = color.name(QColor.HexRgb)
            self.color_field.setText(html_color_name)

