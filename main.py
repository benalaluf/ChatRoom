import sys

from PyQt5.QtGui import QTextDocument, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListView, QLineEdit, QPushButton, \
    QAbstractItemView, QStyledItemDelegate
from PyQt5.QtCore import Qt, QStringListModel


class MessageDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()
        self.username_colors = {'You': QColor('cyan')}

    def paint(self, painter, option, index):
        painter.save()

        message = index.data(Qt.DisplayRole)
        parts = message.split(": ", 1)
        username = parts[0]
        content = parts[1]

        if username not in self.username_colors:
            # Generate a color based on the hash of the username
            color = QColor(hash(username) % 256, hash(username + "color") % 256, hash(username + "text") % 256)
            self.username_colors[username] = color

        color = self.username_colors[username]
        username_colored = f'<font color="{color.name()}">{username}</font>'

        formatted_message = f"{username_colored}: {content}"

        document = QTextDocument()
        document.setHtml(formatted_message)
        option.text = ""
        self.initStyleOption(option, index)
        painter.translate(option.rect.topLeft())
        document.drawContents(painter)

        painter.restore()


class ChatGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.messages = []

    def initUI(self):
        self.setWindowTitle('Modern Chat GUI')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.message_view = QListView(self)
        self.model = QStringListModel()
        self.message_view.setModel(self.model)
        self.message_view.setItemDelegate(MessageDelegate())
        self.message_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.layout.addWidget(self.message_view)

        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.sendMessage)
        self.input_layout.addWidget(self.input_field)
        self.input_layout.addWidget(self.send_button)

        self.layout.addLayout(self.input_layout)

        self.setLayout(self.layout)

    def sendMessage(self):
        message = self.input_field.text()
        if message:
            self.messages.append("You: " + message)
            self.model.setStringList(self.messages)
            self.input_field.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_window = ChatGUI()
    chat_window.show()
    sys.exit(app.exec_())
