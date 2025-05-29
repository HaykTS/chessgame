from copy import deepcopy
from core.pieces import create_initial_board
from core.pieces import King, Rook

class Board:
    def __init__(self):
        self.state = create_initial_board()
        self.last_move = None
        self.en_passant_target = None

    def get_piece(self, pos):
        row, col = pos
        return self.state[row][col]

    def move_piece(self, start, end):
        piece = self.get_piece(start)
        if not piece:
            return False

        legal_moves = piece.get_legal_moves(start, self)
        if end not in legal_moves:
            return False

        captured = self.get_piece(end)
        self.state[end[0]][end[1]] = piece
        self.state[start[0]][start[1]] = None
        self.last_move = (start, end)

        if isinstance(piece, (King, Rook)):
            piece.has_moved = True
        if isinstance(piece, King):
            row, col_start = start
            col_end = end[1]
            if col_start == 4 and col_end == 6:
                rook = self.get_piece((row, 7))
                self.state[row][5] = rook
                self.state[row][7] = None
                rook.has_moved = True
            if col_start == 4 and col_end == 2:
                rook = self.get_piece((row, 0))
                self.state[row][3] = rook
                self.state[row][0] = None
                rook.has_moved = True
    
        if piece.symbol.lower() == "p":
            if (piece.color == 'w' and end[0] == 0) or (piece.color == 'b' and end[0] == 7):
                self.state[end[0]][end[1]] = piece
            if abs(start[0] - end[0]) == 2:
                self.en_passant_target = ((start[0] + end[0]) // 2, start[1])
            else:
                if end == self.en_passant_target and self.get_piece(end) is None:
   
                    self.state[start[0]][end[1]] = None
                self.en_passant_target = None
        else:
            self.en_passant_target = None


        piece.moved = True
        return True

    def get_legal_moves(self, pos, ignore_check=False):
        piece = self.get_piece(pos)
        if not piece:
            return []
        
        pseudo_moves = piece.get_legal_moves(pos, self)

        if ignore_check:
            return pseudo_moves
        legal_moves = []
        for move in pseudo_moves:
            temp_board = self.copy()
            temp_board.move_piece(pos, move)
            if not temp_board.is_in_check(piece.color):
                legal_moves.append(move)
        return legal_moves

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c))
                if piece and piece.color == color and piece.symbol == 'k':
                    return (r, c)
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False 

        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c))
                if piece and piece.color != color:
                    if king_pos in piece.get_legal_moves((r, c), self):
                        return True
        return False

    def has_legal_moves(self, color):
        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c))
                if piece and piece.color == color:
                    moves = self.get_legal_moves((r, c))
                    if moves:
                        for move in moves:
                            temp_board = self.copy()
                            temp_board.move_piece((r, c), move)
                            if not temp_board.is_in_check(color):
                                return True
        return False

    def is_checkmate(self, color):
        return self.is_in_check(color) and not self.has_legal_moves(color)

    def is_stalemate(self, color):
        return not self.is_in_check(color) and not self.has_legal_moves(color)
    def copy(self):
        new_board = Board()
        new_board.state = deepcopy(self.state)
        new_board.last_move = self.last_move
        new_board.en_passant_target = self.en_passant_target
        return new_board
    def square_attacked(self, pos, by_color):
        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r,c))
                if piece and piece.color == by_color:
                    moves = self.get_legal_moves((r,c), ignore_check=True)
                    if pos in moves:
                        return True
        return False
