from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtGui import QColor, QTextDocument, QFont
from PyQt5.QtWidgets import QWidget, QListView, QAbstractItemView, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, \
    QStyledItemDelegate, QMessageBox


class ChatPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.messages = []

        self.layout = QVBoxLayout()


        self.message_view = QListView()
        self.model = QStringListModel()
        self.message_view.setModel(self.model)
        self.message_view.setItemDelegate(MessageDelegate(parent))
        self.message_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.layout.addWidget(self.message_view)

        self.input_layout = QHBoxLayout()
        self.admin_page_button = QPushButton('@')
        self.admin_page_button.clicked.connect(parent.show_admin)
        self.admin_page_button.setStyleSheet("color: red; font-size: 16px; font-weight: bold; "
                                       "border-radius: 5px;")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Send a message...")
        self.send_button = QPushButton('Send')
        self.send_button.setStyleSheet("color: white; font-size: 14px; "
                                           "border-radius: 5px; font-weight: bold ; background-color: #007ACC")
        self.input_layout.addWidget(self.admin_page_button)
        self.input_layout.addWidget(self.input_field)
        self.input_layout.addWidget(self.send_button)
        self.input_layout.setSpacing(5)


        self.layout.addLayout(self.input_layout)
        self.setLayout(self.layout)



    def add_msg_to_chat(self, message: list):
        self.messages.extend(message)
        self.model.setStringList(self.messages)

    def get_input_text(self):
        text = self.input_field.text()
        self.input_field.clear()
        return text

    def set_muted(self):
        self.input_field.setPlaceholderText("you are muted!!!")




class MessageDelegate(QStyledItemDelegate):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def get_color_by_user(self, username):
        clients = self.parent.client_conn.connected_clients + self.parent.client_conn.was_connected_clients
        for client in clients:
            if client.username == username:
                return client.color
        color = QColor(hash(username) % 256, hash(username + "color") % 256, hash(username + "text") % 256)
        color = color.name()
        return color


    def paint(self, painter, option, index):

        try:
            painter.save()

            message = index.data(Qt.DisplayRole)
            if message:
                if message[0] == '*':
                    formatted_message = f'<font color="gray">{message[1:]}</font>'
                else:
                    parts = message.split(": ", 1)
                    username = parts[0]
                    content = parts[1]

                    color = self.get_color_by_user(username)

                    username_colored = ''
                    if username[0] == '@':
                        color = self.get_color_by_user(username[1:])
                        username_colored+=f'<font color="#ff2349">@</font>'
                        username_colored += f'<font color="{color}">{username[1:]}</font>'
                    elif username[0] == "!":
                        color = self.get_color_by_user(username[1:])
                        username_colored += f'<font color="#ff0000">Private </font>'
                        username_colored += f'<font color="{color}">{username[1:]}</font>'
                    else:
                        username_colored += f'<font color="{color}">{username}</font>'

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

