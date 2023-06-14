class Player:
    def __init__(self, address, socket, piece):
        self.address = address
        self.socket = socket
        self.piece = piece
        self.pieces_left = 0
