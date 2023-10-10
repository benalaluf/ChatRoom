import sys

from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QHBoxLayout, \
    QStackedWidget, QListView, QAbstractItemView, QLineEdit, QFormLayout, QGridLayout, QColorDialog
from PyQt5.uic.properties import QtCore

from src.gui.main import MessageDelegate


class ChatGUI(QMainWindow):

        def __init__(self):
            super().__init__()
            self.setWindowTitle("ChatRoom")
            self.setGeometry(100, 100, 600, 800)

            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)

            self.init_ui()

        def init_ui(self):
            self.page_layout = QStackedWidget()

            self.page_layout.addWidget(MainMenu())
            self.page_layout.addWidget(Chat())

            self.central_layout = QVBoxLayout()
            self.central_layout.addWidget(self.page_layout)

            self.central_widget.setLayout(self.central_layout)
            self.page_layout.setCurrentIndex(1)


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.message_view = QListView()
        self.model = QStringListModel()
        self.message_view.setModel(self.model)
        self.message_view.setItemDelegate(MessageDelegate())
        self.message_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.layout.addWidget(self.message_view)

        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.send_button = QPushButton('Send')
        self.input_layout.addWidget(self.input_field)
        self.input_layout.addWidget(self.send_button)

        self.layout.addLayout(self.input_layout)
        self.setLayout(self.layout)


    def addMessageToGUI(self, message: list):
        self.messages.extend(message)
        self.model.setStringList(self.messages)

    def get_input_text(self):
        text = self.input_field.text()
        self.input_field.clear()
        return text


class Chat(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        # Headline Label
        self.headline_label = QLabel("Login", self)
        self.headline_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.headline_label, 0, 0, 1, 2)  # Span two columns

        # Username Input
        self.username_label = QLabel("Username:", self)
        self.username_field = QLineEdit(self)
        self.layout.addWidget(self.username_label, 1, 0, 1, 2)  # Span two columns
        self.layout.addWidget(self.username_field, 2, 0, 1, 2)  # Span two columns

        # Color Input
        self.color_label = QLabel("Color:", self)
        self.color_field = QLineEdit(self)
        self.color_field.setReadOnly(True)  # Make it read-only
        self.color_button = QPushButton('Pick Color', self)
        self.color_button.clicked.connect(self.openColorDialog)  # Connect the button to the dialog
        self.layout.addWidget(self.color_label, 3, 0, 1, 2)  # Span two columns
        self.layout.addWidget(self.color_field, 4, 0, 1, 2)  # Span two columns
        self.layout.addWidget(self.color_button, 5, 0, 1, 2)  # Span two columns

        # Login Button
        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button, 6, 0, 1, 2)  # Span two columns

        # Set column stretch to make it symmetrical
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

        # Set row stretch for spacing
        self.layout.setRowStretch(7, 1)

        self.setLayout(self.layout)

    def openColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            html_color_name = color.name(QColor.HexRgb)
            self.color_field.setText(html_color_name)

    def login(self):
        print('login')
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatGUI()
    window.show()
    sys.exit(app.exec_())