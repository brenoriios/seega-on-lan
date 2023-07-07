import tkinter as tk
import threading
import json

from src.settings import settings


class Board:
    def __init__(self, root, client_socket):
        self.root = root
        self.client_socket = client_socket
        self.widgets = {}
        self.draw_board()

    def connect_to_server(self):
        self.client_socket.connect((settings.HOST, settings.PORT))
        threading._start_new_thread(self.handle_message, (self.client_socket, "m"))

    def handle_message(self, socket, m):
        while True:
            from_server = json.loads(socket.recv(settings.BUFFER_SIZE).decode())

            if not from_server:
                return

            if from_server["type"] == "command":
                if from_server["head"] == "show_greetings_message":
                    message = from_server["body"]
                    self.widgets["status"]["label"].config(text=message[0])
                    self.widgets["bottom_status"]["label"].pack()
                    self.widgets["bottom_status"]["label"].config(text=message[1])
                    self.widgets["connect"]["frame"].pack_forget()

                if from_server["head"] == "countdown_start_game":
                    self.widgets["status"]["label"].config(text=from_server["body"])

                if from_server["head"] == "start_game":
                    board_data = from_server["body"]
                    self.re_draw(board_data[0], board_data[1])
                    self.widgets["board"]["frame"].pack()

                if from_server["head"] == "highlight_cell_move_options":
                    valid_move_options = from_server["body"]
                    self.highlight_cell_move_options(valid_move_options)

                if from_server["head"] == "re_draw":
                    board_data = from_server["body"]
                    self.re_draw(board_data[0], board_data[1])

                if from_server["head"] == "end_game":
                    self.widgets["status"]["label"].config(text=from_server["body"])
                    self.widgets["board"]["frame"].pack_forget()

    def make_play(self, row, column):
        self.make_command("make_play", [row, column])

    def make_command(self, action, args):
        command = json.dumps({"type": "command", "head": action, "body": args})
        self.client_socket.sendall(command.encode("UTF-8"))

    def get_cell_resource_image(self, piece_color):
        if piece_color == settings.PIECES[0]["letter"]:
            piece_image = tk.PhotoImage(file=settings.PIECES[0]["image_resource"])
        elif piece_color == settings.PIECES[1]["letter"]:
            piece_image = tk.PhotoImage(file=settings.PIECES[1]["image_resource"])
        else:
            piece_image = tk.PhotoImage(file=settings.EMPTY_CELL_RESOURCE_IMAGE)

        return piece_image

    def highlight_cell_move_options(self, valid_move_options):
        if not valid_move_options:
            return False

        for move in valid_move_options:
            coordenates = tuple(move)
            self.widgets[coordenates]["frame"].config(bg=settings.VALID_CELL_COLOR)
            self.widgets[coordenates]["label"].config(bg=settings.VALID_CELL_COLOR)

    def re_draw(self, current_player_message, board_info):
        self.widgets["status"]["label"].config(text=current_player_message)

        for row in range(settings.BOARD_SIZE):
            for col in range(settings.BOARD_SIZE):
                piece_color = board_info[row][col]
                board_cell_label_image = self.get_cell_resource_image(piece_color)
                cell_label = self.widgets[(row, col)]["label"]
                cell_label.config(
                    bg=settings.DEFAULT_CELL_COLOR, image=board_cell_label_image
                )
                cell_label.image = board_cell_label_image
                self.widgets[(row, col)]["frame"].config(bg=settings.DEFAULT_CELL_COLOR)

    def draw_board(self):
        status_bar = tk.Frame(self.root)
        game_board_frame = tk.Frame(self.root)
        game_board = tk.Frame(game_board_frame)
        connect_bar = tk.Frame(status_bar)
        bottom_status_bar = tk.Frame(self.root)

        status_label = tk.Label(
            status_bar,
            text="Aguardando jogadores...",
            pady=10,
            font=("Arial", 15),
        )
        status_label.pack()

        for row in range(settings.BOARD_SIZE):
            for col in range(settings.BOARD_SIZE):
                board_cell = tk.Frame(game_board, borderwidth=1, relief="solid")

                piece_color = ""
                board_cell_label_image = self.get_cell_resource_image(piece_color)

                board_cell_label = tk.Label(
                    board_cell, width=80, height=80, image=board_cell_label_image
                )
                board_cell_label.image = board_cell_label_image
                board_cell_label.pack()

                board_cell.grid(row=row, column=col)

                board_cell_label.bind(
                    "<Button-1>", lambda event, r=row, c=col: self.make_play(r, c)
                )
                self.widgets[(row, col)] = {
                    "frame": board_cell,
                    "label": board_cell_label,
                }

        connect_button = tk.Button(connect_bar, text="Conectar")
        connect_button.bind(
            "<Button-1>",
            lambda event, button=connect_button: self.connect_to_server(),
        )
        connect_button.pack()
        connect_bar.pack()

        bottom_status_label = tk.Label(
            bottom_status_bar,
            text="",
            pady=10,
            font=("Arial", 15),
        )

        self.widgets["status"] = {"frame": status_bar, "label": status_label}
        self.widgets["board"] = {"frame": game_board}
        self.widgets["connect"] = {"frame": connect_bar, "button": connect_button}
        self.widgets["bottom_status"] = {
            "frame": bottom_status_bar,
            "label": bottom_status_label,
        }

        # status_bar.pack()
        # connect_bar.pack()
        # bottom_status_bar.pack()

        status_bar.grid(row=0)
        game_board_frame.grid(row=1)
        bottom_status_bar.grid(row=2)
