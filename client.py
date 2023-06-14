import socket
import tkinter as tk

from src.views.Board import Board

client_socket = socket.socket()

root = tk.Tk()
root.title("Seega")

game_ui = Board(root, client_socket)

root.mainloop()
