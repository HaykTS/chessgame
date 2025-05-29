import os
import pygame
import json

class Theme:
    def __init__(self, name, board_image, piece_images):
        self.name = name
        self.board_image = board_image
        self.piece_images = piece_images

class ThemeLoader:
    @staticmethod
    def load(name):
        with open("assets/themes/theme_config.json") as f:
            config = json.load(f)

        board_path = os.path.join("assets", config["board"])
        board_image = pygame.image.load(board_path)

        pieces_path = config["pieces"]
        piece_images = {"w": {}, "b": {}}
        for color in ["w", "b"]:
            path = os.path.join("assets", pieces_path[color])
            for symbol in ["p", "r", "n", "b", "q", "k"]:
                filename = f"{'w' if color == 'w' else 'b'}_{symbol}.png"
                piece_images[color][symbol] = pygame.image.load(os.path.join(path, filename))

        return Theme(name, board_image, piece_images)
