import sys

from PyQt5.QtWidgets import QApplication

from src.app.client_app import ClientApp
from src.connections.client import Client
from src.gui.main import ChatGUI

if __name__ == '__main__':
    # Client('localhost', 6969).main()
    ClientApp().main()
