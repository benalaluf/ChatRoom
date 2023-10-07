import threading

from src.connections.client import Client
from src.gui.main import ChatGUI
from src.utils.check_color import check_color


class ClientApp():
    def __init__(self):
        self.client_gui = ChatGUI()
        self.client_connection = Client('localhost', 8090)

        self.client_gui.connect_send_func(self.send_message)
        self.client_connection.set_on_new_message_func(self.client_gui.addMessageToGUI)

        username, color = self.get_client_credentials()

        self.client_connection.register(username, color)


    def main(self):
        threading.Thread(target=self.client_connection.main).start()
        self.client_gui.run()

    def send_message(self):
        msg = self.client_gui.get_input_text()
        self.client_connection.send_message(msg)

    def get_client_credentials(self):
        username = input("Please Enter Your Nickname: ")
        color = input("Please Enter Your Color: ")
        if not check_color(color):
            print("Invalid color")
            return self.get_client_credentials()
        return username, color


