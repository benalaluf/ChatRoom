import sys
from abc import ABC, abstractmethod

import qdarktheme
from PyQt5.QtGui import QTextDocument, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListView, QLineEdit, QPushButton, \
    QAbstractItemView, QStyledItemDelegate
from PyQt5.QtCore import Qt, QStringListModel


class MessageDelegate(QStyledItemDelegate):
    username_colors = dict()

    def __init__(self):
        super().__init__()

    @staticmethod
    def update_usernames_color(username, color):
        MessageDelegate.username_colors.update({username: color})

    def paint(self, painter, option, index):
        try:
            painter.save()

            message = index.data(Qt.DisplayRole)

            if message:
                if message[0] == '*':
                    message = f'<font color="gray">{message}</font>'
                parts = message.split(": ", 1)
                username = parts[0]
                content = parts[1]

                if username not in self.username_colors:
                    color = QColor(hash(username) % 256, hash(username + "color") % 256, hash(username + "text") % 256)
                    self.username_colors[username] = color.name()

                color = self.username_colors[username]
                username_colored = f'<font color="{color}">{username}</font>'

                formatted_message = f"{username_colored}: {content}"

                document = QTextDocument()
                document.setHtml(formatted_message)
                option.text = ""
                self.initStyleOption(option, index)
                painter.translate(option.rect.topLeft())
                document.drawContents(painter)

            painter.restore()
        except Exception as e:
            print(e)


class ClientGUI(ABC):
    def __init__(self):
        self.app = QApplication(sys.argv)
        qdarktheme.setup_theme()
        self.window = QWidget()
        self.initUI()
        self.messages = []

    def initUI(self):
        self.window.setWindowTitle('ChatRoom')
        self.window.setGeometry(100, 100, 600, 800)

        self.layout = QVBoxLayout()

        self.message_view = QListView(self.window)
        self.model = QStringListModel()
        self.message_view.setModel(self.model)
        self.message_view.setItemDelegate(MessageDelegate())
        self.message_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.layout.addWidget(self.message_view)

        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self.window)
        self.send_button = QPushButton('Send', self.window)
        self.send_button.clicked.connect(self.send)
        self.input_layout.addWidget(self.input_field)
        self.input_layout.addWidget(self.send_button)

        self.layout.addLayout(self.input_layout)

        self.window.setLayout(self.layout)

    def addMessageToGUI(self, message: list):
        self.messages.extend(message)
        self.model.setStringList(self.messages)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def get_input_text(self):
        text = self.input_field.text()
        self.input_field.clear()
        return text

    @abstractmethod
    def send(self):
        pass