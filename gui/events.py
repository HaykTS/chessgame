import pygame
from .promotion_window import PromotionWindow


class EventHandler:
    def __init__(self, game, renderer):
        self.game = game
        self.renderer = renderer
        self.selected_pos = None
        self.awaiting_promotion = None
        self.promotion_window = None


    def handle_event(self, event):
        if self.promotion_window:
            closed = self.promotion_window.handle_event(event)
            if closed:
                self.promotion_window = None
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            tile_size = self.renderer.tile_size
            row = mouse_y // tile_size
            col = mouse_x // tile_size
            pos = (row, col)

            piece = self.game.board.get_piece(pos)

            if self.selected_pos:
                moved = self.game.move(self.selected_pos, pos)
                if moved:
                    if self.game.promotion_required:
                        color = self.game.turn 
                        self.promotion_window = PromotionWindow(
                            self.renderer.screen,
                            self.renderer.theme.piece_images,
                            color,
                            self.on_promotion_selected
                        )
                        self.renderer.promotion_window = self.promotion_window

                self.selected_pos = None
                self.renderer.selected_pos = None
                self.renderer.highlighted_moves = []
            elif piece and piece.color == self.game.turn:
                self.selected_pos = pos
                self.renderer.selected_pos = pos
                legal_moves = self.game.board.get_legal_moves(pos)
                self.renderer.highlighted_moves = legal_moves
            else:
                self.selected_pos = None
                self.renderer.selected_pos = None
                self.renderer.highlighted_moves = []



            

    def on_promotion_selected(self, piece_code):
        self.game.promote(piece_code)
        self.promotion_window = None
        self.renderer.promotion_window = None

