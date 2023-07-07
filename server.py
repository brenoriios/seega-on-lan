import socket
import random
import json
import threading
import time

from src.settings import settings
from src.models.Seega import Seega
from src.models.Player import Player


def make_command(action, args):
    return json.dumps({"type": "command", "head": action, "body": args}).encode("UTF-8")


def make_play(row, column):
    global winner
    game_instance.make_play(row, column)

    if not game_instance.from_is_not_set and game_instance.to_is_not_set:
        move_options = game_instance.get_move_options(row, column)
        print(move_options)
        highlight_command = make_command("highlight_cell_move_options", move_options)
        game_instance.current_player.socket.sendall(highlight_command)

    if game_instance.from_is_not_set and game_instance.to_is_not_set:
        re_draw_current_player_command = make_command(
            "re_draw", ["Sua vez", game_instance.board]
        )
        re_draw_opponent_command = make_command(
            "re_draw", ["Vez do seu adversário", game_instance.board]
        )
        game_instance.current_player.socket.sendall(re_draw_current_player_command)
        game_instance.opponent.socket.sendall(re_draw_opponent_command)

    winner = game_instance.check_winner()
    if winner:
        winner = winner.piece["name"]
        end_game_command = make_command("end_game", f"Vencedor: {winner}!")
        game_instance.current_player.socket.sendall(end_game_command)
        game_instance.opponent.socket.sendall(end_game_command)


def handle_message(socket, m):
    while True:
        message = json.loads(socket.recv(settings.BUFFER_SIZE).decode())

        if not message:
            return

        if message["type"] == "command":
            if message["head"] == "make_play":
                if (
                    socket.getpeername()
                    == game_instance.current_player.socket.getpeername()
                ):
                    print(game_instance.game_stage)
                    args = message["body"]
                    make_play(args[0], args[1])


server_socket = socket.socket()
server_socket.bind((settings.HOST, settings.PORT))
server_socket.listen()

players = []
game_instance = Seega()

while len(players) < 2:
    client_socket, client_address = server_socket.accept()
    new_player = Player(client_address, client_socket, settings.PIECES.pop())
    players.append(new_player)
    player_piece = new_player.piece["name"]
    greetings_message = make_command(
        "show_greetings_message",
        ["Bem Vindo(a)!", f"Você está jogando com {player_piece}"],
    )
    client_socket.sendall(greetings_message)

game_instance.start_game(players)

threading._start_new_thread(handle_message, (game_instance.current_player.socket, "m"))
threading._start_new_thread(handle_message, (game_instance.opponent.socket, "m"))

for count in range(3, 0, -1):
    command = make_command(
        "countdown_start_game", f"O jogo vai começar em \n {count} \n segundo(s)!"
    )
    game_instance.current_player.socket.sendall(command)
    game_instance.opponent.socket.sendall(command)
    time.sleep(1)

start_game_current_player = make_command(
    "start_game", ["Você Começa!", game_instance.board]
)
start_game_opponent = make_command(
    "start_game", ["Seu adversário começa", game_instance.board]
)
game_instance.current_player.socket.sendall(start_game_current_player)
game_instance.opponent.socket.sendall(start_game_opponent)

winner = False

while not winner:
    pass
