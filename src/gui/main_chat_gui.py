import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QHBoxLayout, \
    QStackedWidget


class ChatGUI(QMainWindow):

        def __init__(self):
            super().__init__()
            self.setWindowTitle("Multi-Page App")
            self.setGeometry(100, 100, 400, 300)

            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)

            self.init_ui()

        def init_ui(self):
            self.button_layout = QHBoxLayout()
            self.page_layout = QStackedWidget()

            self.page1_button = QPushButton("Page 1", self)
            self.page1_button.clicked.connect(self.show_page1)
            self.button_layout.addWidget(self.page1_button)

            self.page2_button = QPushButton("Page 2", self)
            self.page2_button.clicked.connect(self.show_page2)
            self.button_layout.addWidget(self.page2_button)

            self.page_layout.addWidget(MainMenu())
            self.page_layout.addWidget(Chat())

            self.central_layout = QVBoxLayout()
            self.central_layout.addLayout(self.button_layout)
            self.central_layout.addWidget(self.page_layout)

            self.central_widget.setLayout(self.central_layout)


        def show_page1(self):
            self.page_layout.setCurrentIndex(0)

        def show_page2(self):
            self.page_layout.setCurrentIndex(1)



class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("main menu", self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

class Chat(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("chat", self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatGUI()
    window.show()
    sys.exit(app.exec_())