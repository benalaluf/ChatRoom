from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtGui import QColor, QTextDocument
from PyQt5.QtWidgets import QWidget, QListView, QAbstractItemView, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, \
    QStyledItemDelegate


class ChatPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.messages = []

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

    def add_msg_to_chat(self, message: list):
        self.messages.extend(message)
        self.model.setStringList(self.messages)

    def get_input_text(self):
        text = self.input_field.text()
        self.input_field.clear()
        return text


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
                    # Generate a color based on the hash of the username
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

