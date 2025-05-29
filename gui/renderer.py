import pygame
from pygame.examples.grid import TILE_SIZE
#HIGHLIGHT = (200, 255, 255)
#MOVE_COLOR = (144, 238, 144)
#UNAV_MOVE_COLOR = (255, 0, 0)

class Renderer:
    def __init__(self, screen, theme, game):
        self.screen = screen
        self.theme = theme
        self.game = game
        self.tile_size = screen.get_width() // 8
        self.highlighted_moves = []
        self.selected_pos = None

    def render(self):
        self.render_board()
        self.render_highlights()
        self.render_pieces()
        if hasattr(self, 'promotion_window') and self.promotion_window:
            self.promotion_window.draw()

    def render_highlights(self):
        s_move = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)

        if self.selected_pos:
            r,c = self.selected_pos
            pygame.draw.rect(s_move, (100, 100, 255, 100), (0, 0, self.tile_size, self.tile_size))
            self.screen.blit(s_move, (c * self.tile_size, r * self.tile_size))
        for r,c in self.highlighted_moves:
            s_move.fill((0, 255, 0, 80))
            self.screen.blit(s_move, (c * self.tile_size, r * self.tile_size))
        king_pos = self.game.board.find_king(self.game.turn)
        if self.game.board.is_in_check(self.game.turn):
            if king_pos:
                r, c = king_pos
                s_move.fill((255, 0, 0, 80))
                self.screen.blit(s_move, (c * self.tile_size, r * self.tile_size))
    def render_board(self):
        self.screen.blit(self.theme.board_image, (0, 0))

    def render_pieces(self):
        board = self.game.board
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece:
                    color = "w" if piece.color == "w" else "b"
                    symbol = piece.symbol.lower()
                    image = self.theme.piece_images[color][symbol]
                    scaled = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                    x = col * self.tile_size
                    y = row * self.tile_size
                    self.screen.blit(scaled, (x, y))
    def render_promotion_menu(self, color):
        size = self.tile_size
        pieces = ['q', 'r', 'b', 'n']
        for i, p in enumerate(pieces):
            image = self.theme.piece_images[color][p]
            scaled = pygame.transform.scale(image, (size, size))
            x = i * size
            y = 0  
            self.screen.blit(scaled, (x, y))
