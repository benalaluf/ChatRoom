import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextDocument, QColor
from PyQt5.QtWidgets import QApplication, QListView, QVBoxLayout, QWidget, QStyledItemDelegate


class MessageDelegate(QStyledItemDelegate):
    username_colors = dict()

    def __init__(self):
        super().__init__()

    @staticmethod
    def update_usernames_color(username, color):
        MessageDelegate.username_colors.update({username: color})

    def paint(self, painter, option, index):
        painter.save()

        message = index.data(Qt.DisplayRole)

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

class MessageApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Message List")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout(self)

        model = QStandardItemModel(self)
        messages = [
            "User1: Hello!",
            "User2: Hi there!",
            "User1: How are you?",
        ]
        for message in messages:
            item = QStandardItem(message)
            model.appendRow(item)

        listView = QListView(self)
        listView.setModel(model)
        listView.setItemDelegate(MessageDelegate())

        layout.addWidget(listView)

        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = MessageApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
