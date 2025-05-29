class Piece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol
        self.moved = False

    def get_legal_moves(self, pos, board):
        return []

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "p")

    def get_legal_moves(self, pos, board):
        row, col = pos
        direction = -1 if self.color == "w" else 1
        moves = []

        if board.get_piece((row + direction, col)) is None:
            moves.append((row + direction, col))
            if not self.moved and board.get_piece((row + 2 * direction, col)) is None:
                moves.append((row + 2 * direction, col))

        for dx in [-1, 1]:
            nx, ny = row + direction, col + dx
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece((nx, ny))
                if target and target.color != self.color:
                    moves.append((nx, ny))

        if board.en_passant_target:
            ep_row, ep_col = board.en_passant_target
            if ep_row == row + direction and abs(ep_col - col) == 1:
                adjacent = board.get_piece((row, ep_col))
                if adjacent and adjacent.color != self.color and adjacent.symbol.lower() == "p":
                    moves.append((ep_row, ep_col))

        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "r")
        self.has_moved = False

    def get_legal_moves(self, pos, board):
        return self._linear_moves(pos, board, directions=[(1, 0), (-1, 0), (0, 1), (0, -1)])

    def _linear_moves(self, pos, board, directions):
        moves = []
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr
                c += dc
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                target = board.get_piece((r, c))
                if target is None:
                    moves.append((r, c))
                else:
                    if target.color != self.color:
                        moves.append((r, c))
                    break
        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "n")

    def get_legal_moves(self, pos, board):
        row, col = pos
        moves = []
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece((r, c))
                if not target or target.color != self.color:
                    moves.append((r, c))
        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "b")

    def get_legal_moves(self, pos, board):
        return self._linear_moves(pos, board, directions=[(1, 1), (1, -1), (-1, 1), (-1, -1)])

    def _linear_moves(self, pos, board, directions):
        moves = []
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr
                c += dc
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                target = board.get_piece((r, c))
                if target is None:
                    moves.append((r, c))
                else:
                    if target.color != self.color:
                        moves.append((r, c))
                    break
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "q")

    def get_legal_moves(self, pos, board):
        return self._linear_moves(pos, board, directions=[
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ])

    def _linear_moves(self, pos, board, directions):
        moves = []
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr
                c += dc
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                target = board.get_piece((r, c))
                if target is None:
                    moves.append((r, c))
                else:
                    if target.color != self.color:
                        moves.append((r, c))
                    break
        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color, "k")
        self.has_moved = False

    def get_legal_moves(self, pos, board):
        row, col = pos
        directions = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if dr != 0 or dc != 0]
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece((r, c))
                if target is None or target.color != self.color:
                    moves.append((r, c))
        if not self.has_moved and not board.is_in_check(self.color):
            if self.can_castle_kingside(board, pos):
                moves.append((row, 6))
            if self.can_castle_queenside(board, pos):
                moves.append((row, 2))
        return moves
    def can_castle_kingside(self, board, pos):
        row = pos[0]
        rook = board.get_piece((row, 7))
        if not isinstance(rook, Rook) or rook != self.color or rook.has_moved:
            return False
        for col in [5, 6]:
            if board.get_piece((row, col)) is not None or board.square_attacked((row, col), self.color):
                return False
        return True
    def can_castle_queenside(self, board, pos):
        row = pos[0]
        rook = board.get_piece((row, 0))
        if not isinstance(rook, Rook) or rook != self.color or rook.has_moved:
            return False
        for col in [1, 2, 3]:
            if board.get_piece((row, col)) is not None or (col != 1 and board.square_attacked((row, col), self.color)):
                return False
        return True

def create_initial_board():
    board = [[None] * 8 for _ in range(8)]

    for col in range(8):
        board[1][col] = Pawn("b")
        board[6][col] = Pawn("w")

    board[0][0] = Rook("b")
    board[0][1] = Knight("b")
    board[0][2] = Bishop("b")
    board[0][3] = Queen("b")
    board[0][4] = King("b")
    board[0][5] = Bishop("b")
    board[0][6] = Knight("b")
    board[0][7] = Rook("b")

    board[7][0] = Rook("w")
    board[7][1] = Knight("w")
    board[7][2] = Bishop("w")
    board[7][3] = Queen("w")
    board[7][4] = King("w")
    board[7][5] = Bishop("w")
    board[7][6] = Knight("w")
    board[7][7] = Rook("w")

    return board
