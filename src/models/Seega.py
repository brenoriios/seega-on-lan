from src.settings import settings
import random


class Seega:
    board = []

    game_stage = settings.PLACING_STAGE
    from_is_not_set = True
    to_is_not_set = True

    from_row = None
    from_column = None
    to_row = None
    to_column = None

    def __init__(self):
        self.maximum_pieces = ((settings.BOARD_SIZE * settings.BOARD_SIZE) - 1) / 2
        self.board_center = {
            "row": (settings.BOARD_SIZE - 1) / 2,
            "column": (settings.BOARD_SIZE - 1) / 2,
        }

        self.board_init()

    def start_game(self, players):
        self.players = players
        random.shuffle(self.players)
        self.current_player = self.players[0]
        self.opponent = self.players[1]

    def board_init(self):
        for row in range(settings.BOARD_SIZE):
            line = []
            for column in range(settings.BOARD_SIZE):
                line.append("")
            self.board.append(line)

    def place_on_position(self, row, column):
        if (
            self.is_invalid(row, column)
            or self.is_full(row, column)
            or self.is_center(row, column)
        ):
            return False

        self.board[row][column] = self.current_player.piece["letter"]

        return True

    def move_to_position(self):
        self.board[self.from_row][self.from_column] = ""
        self.board[self.to_row][self.to_column] = self.current_player.piece["letter"]

        self.capture_on_position(self.to_row, self.to_column)

        print(
            f"From [{self.from_row}][{self.from_column}] to [{self.to_row}][{self.to_column}]"
        )
        print(
            f"Pieces remaining for {self.opponent.piece['name']}: {self.opponent.pieces_left}"
        )

        return True

    def capture_on_position(self, row, column):
        captures = (
            self.capture_on_top(row, column)
            + self.capture_on_right(row, column)
            + self.capture_on_bottom(row, column)
            + self.capture_on_left(row, column)
        )
        self.opponent.pieces_left = self.opponent.pieces_left - captures

    def is_center(self, row, column):
        if row == self.board_center["row"] and column == self.board_center["column"]:
            return True

        return False

    def is_full(self, row, column):
        if self.board[row][column] != "":
            return True

        return False

    def is_not_piece_owner(self, row, column):
        if self.board[row][column] != self.current_player.piece["letter"]:
            return True
        return False

    def is_invalid(self, row, column):
        if row < 0 or row >= settings.BOARD_SIZE:
            return True

        if column < 0 or column >= settings.BOARD_SIZE:
            return True

        return False

    def capture_on_top(self, row, column):
        if (
            self.is_invalid(row, column)
            or self.is_invalid(row - 1, column)
            or self.is_invalid(row - 2, column)
            or self.board[row - 1][column] == ""
        ):
            return 0

        if (
            self.board[row][column] != self.board[row - 1][column]
            and self.board[row][column] == self.board[row - 2][column]
        ):
            self.board[row - 1][column] = ""
            return 1

        return 0

    def capture_on_right(self, row, column):
        if (
            self.is_invalid(row, column)
            or self.is_invalid(row, column + 1)
            or self.is_invalid(row, column + 2)
            or self.board[row][column + 1] == ""
        ):
            return 0

        if (
            self.board[row][column] != self.board[row][column + 1]
            and self.board[row][column] == self.board[row][column + 2]
        ):
            self.board[row][column + 1] = ""
            return 1

        return 0

    def capture_on_bottom(self, row, column):
        if (
            self.is_invalid(row, column)
            or self.is_invalid(row + 1, column)
            or self.is_invalid(row + 2, column)
            or self.board[row + 1][column] == ""
        ):
            return 0

        if (
            self.board[row][column] != self.board[row + 1][column]
            and self.board[row][column] == self.board[row + 2][column]
        ):
            self.board[row + 1][column] = ""
            return 1

        return 0

    def capture_on_left(self, row, column):
        if (
            self.is_invalid(row, column)
            or self.is_invalid(row, column - 1)
            or self.is_invalid(row, column - 2)
            or self.board[row][column - 1] == ""
        ):
            return 0

        if (
            self.board[row][column] != self.board[row][column - 1]
            and self.board[row][column] == self.board[row][column - 2]
        ):
            self.board[row][column - 1] = ""
            return 1

        return 0

    def set_next_player(self):
        print("---------")
        print("current player: " + self.current_player.piece["name"])
        print("opponent player: " + self.opponent.piece["name"])
        self.current_player, self.opponent = self.opponent, self.current_player
        print("swapped")
        print("current player: " + self.current_player.piece["name"])
        print("opponent player: " + self.opponent.piece["name"])

    def is_valid_move_option(self, row, column):
        if not self.is_invalid(row, column) and not self.is_full(row, column):
            return True

        return False

    def get_move_options(self, row, column):
        if self.is_not_piece_owner(row, column) or not self.is_full(row, column):
            return False

        valid_move_options = []

        if self.is_valid_move_option(row + 1, column):
            valid_move_options.append((row + 1, column))

        if self.is_valid_move_option(row, column + 1):
            valid_move_options.append((row, column + 1))

        if self.is_valid_move_option(row - 1, column):
            valid_move_options.append((row - 1, column))

        if self.is_valid_move_option(row, column - 1):
            valid_move_options.append((row, column - 1))

        return valid_move_options

    def placing_stage_action(self, row, column):
        if self.place_on_position(row, column):
            self.current_player.pieces_left = self.current_player.pieces_left + 1
            self.set_next_player()

            if (
                self.players[0].pieces_left == self.maximum_pieces
                and self.players[1].pieces_left == self.maximum_pieces
            ):
                self.game_stage = settings.PLAYING_STAGE

            return True

        return False

    def playing_stage_action(self, row, column):
        if self.from_is_not_set:
            if not self.is_full(row, column) or self.is_not_piece_owner(row, column):
                return False

            self.from_row = row
            self.from_column = column
            self.from_is_not_set = False
            return True

        if self.to_is_not_set:
            if self.is_invalid(row, column) or self.is_full(row, column):
                self.from_is_not_set = True
                return False

            self.to_row = row
            self.to_column = column

        self.from_is_not_set = True
        self.to_is_not_set = True

        self.move_to_position()
        self.set_next_player()

        return True

    def is_stuck(self):
        for row in range(settings.BOARD_SIZE):
            for column in range(settings.BOARD_SIZE):
                if self.current_player.piece["letter"] == self.board[row][column]:
                    if len(self.get_move_options(row, column)) > 0:
                        return False

        return True

    def make_play(self, row, column):
        if self.game_stage == settings.PLACING_STAGE:
            self.placing_stage_action(row, column)

        if self.game_stage == settings.PLAYING_STAGE:
            self.playing_stage_action(row, column)
            if self.is_stuck():
                self.set_next_player()

    def check_winner(self):
        if self.game_stage != settings.PLAYING_STAGE:
            return False

        if self.current_player.pieces_left == 0:
            return self.opponent

        if self.opponent.pieces_left == 0:
            return self.current_player

        return False
