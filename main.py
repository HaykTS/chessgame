import pygame
from gui.theme import ThemeLoader
from gui.renderer import Renderer
from core.game import Game
from gui.events import EventHandler

pygame.init()

WINDOW_SIZE = (512,512)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess")

theme = ThemeLoader.load("classic")
theme.board_image = pygame.transform.scale(theme.board_image, WINDOW_SIZE)

game = Game()
renderer = Renderer(screen, theme, game)
event_handler = EventHandler(game, renderer)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        event_handler.handle_event(event)

    renderer.render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
