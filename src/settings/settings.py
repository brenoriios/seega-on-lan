# HOST = "192.168.1.9"
HOST = "localhost"
PORT = 11523

BUFFER_SIZE = 4096

COMMAND_PREFIX = "command::"
COMMAND_SEPARATOR = "/"
COMMAND_ARGS_SEPARATOR = "&"

NUMBER_OF_PLAYERS = 2
BOARD_SIZE = 5
PLACING_STAGE = "placing_stage"
PLAYING_STAGE = "playing_stage"

DEFAULT_CELL_COLOR = "white"
VALID_CELL_COLOR = "lightgreen"

PIECES = [
    {
        "name": "Vermelhas",
        "letter": "V",
        "image_resource": "src/images/red_piece.png",
    },
    {
        "name": "Azuis",
        "letter": "A",
        "image_resource": "src/images/blue_piece.png",
    },
]

RED_PIECE = "Vermelhas"
BLUE_PIECE = "Azuis"
RED_PIECE_LETTER = "V"
BLUE_PIECE_LETTER = "A"

RED_PIECE_RESOURCE_IMAGE = "src/images/red_piece.png"
BLUE_PIECE_RESOURCE_IMAGE = "src/images/blue_piece.png"
EMPTY_CELL_RESOURCE_IMAGE = "src/images/empty_cell.png"
