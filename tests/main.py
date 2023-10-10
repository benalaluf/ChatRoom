import threading
import tkinter as tk
import tkinter.scrolledtext
from tkinter import simpledialog


class ChatGUI:
    def __init__(self):
       

        self.nickname = 'ben'
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recv_thread = threading.Thread(target=self.recv)

        gui_thread.start()
        recv_thread.start()

    def gui_loop(self):
        self.win = tk.Tk()
        self.win.config(bg="lightgray")

        self.chat_label = tk.Label(self.win, text="Chat: ", bg="lightgray")
        self.chat_label.config(font=("Ariel", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tk.Label(self.win, text="Message: ", bg="lightgray")
        self.msg_label.config(font=("Ariel", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="send", command=self.write)
        self.send_button.config(font=('Ariel', 12))
        self.send_button.pack(padx=20, pady=10)

        self.gui_done = True

        self.win.protocol("VM_DELETE_WINDOW", self.stop)

    def stop(self):
        self.running = False
        self.win.destroy()
        exit(0)

    def write(self):
        pass

    def recv(self):
        pass


if __name__ == '__main__':
    ChatGUI()