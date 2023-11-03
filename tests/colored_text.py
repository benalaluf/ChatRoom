import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextDocument, QTextCharFormat, QTextCursor, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QLabel


class ColoredTextLabel(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.set_text(text)

    def set_text(self, text):
        document = QTextDocument()
        cursor = QTextCursor(document)

        # Create a text format for the word "Ben" to be colored blue
        ben_format = QTextCharFormat()
        ben_format.setForeground(QColor("blue"))

        # Set the text
        cursor.insertText(text)

        # Search for the word "Ben" and apply the blue color format
        cursor.movePosition(QTextCursor.Start)
        while True:
            cursor = document.find("Ben", cursor)
            if cursor.isNull():
                break
            cursor.mergeCharFormat(ben_format)
            cursor.movePosition(QTextCursor.NextWord)

        self.label.setText(document.toPlainText())
        self.adjustSize()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Colored Text in PyQt5 List')

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10, 10, 380, 280)

        # Add items with colored text
        self.addItemWithColoredText("Hello Ben, how are you?")
        self.addItemWithColoredText("Ben is here!")
        self.addItemWithColoredText("This is a test for Ben.")

    def addItemWithColoredText(self, text):
        item = QListWidgetItem(self.listWidget)
        colored_label = ColoredTextLabel(text)
        item.setSizeHint(colored_label.sizeHint())
        self.listWidget.setItemWidget(item, colored_label)


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
