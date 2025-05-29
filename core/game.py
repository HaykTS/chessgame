from core.pieces import Queen, Rook, Bishop, Knight
from .board import Board
class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'w' 
        self.game_over = False
        self.promotion_required = False
        self.promotion_position = None
        self.winner = None
    def next_turn(self):
        self.turn = 'w' if self.turn == 'b' else 'b'
    def move(self, start, end):
        piece = self.board.get_piece(start)
        if not piece or piece.color != self.turn:
            return False  

        legal_moves = self.board.get_legal_moves(start)
        if end not in legal_moves:
            return False 
        temp_board = self.board.copy()
        temp_board.move_piece(start, end)
        if temp_board.is_in_check(self.turn):
            return False 

        self.board.move_piece(start, end)
        if piece.symbol.lower() == "p" and ((piece.color == "w" and end[0] == 0) or (piece.color == "b" and end[0] == 7)):
            self.promotion_required = True
            self.promotion_position = end
            return True

        opponent = 'b' if self.turn == 'w' else 'w'
        if self.board.is_checkmate(opponent):
            self.game_over = True
            self.winner = self.turn
            print("Checkmate")
        elif self.board.is_stalemate(opponent):
            self.game_over = True
            self.winner = None 

        self.turn = opponent
        return True
    def promote(self, piece_type): 
        r, c = self.promotion_position
        color = self.board.get_piece((r, c)).color

        if piece_type == "q":
            self.board.state[r][c] = Queen(color)
        elif piece_type == "r":
            self.board.state[r][c] = Rook(color)
        elif piece_type == "b":
            self.board.state[r][c] = Bishop(color)
        elif piece_type == "n":
            self.board.state[r][c] = Knight(color)

        self.promotion_required = False
        self.promotion_position = None
        self.next_turn()
