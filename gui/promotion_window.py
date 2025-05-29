import pygame

class PromotionWindow:
    def __init__(self, screen, piece_images, color, callback):
        self.screen = screen
        self.piece_images = piece_images
        self.color = color
        self.callback = callback  

        self.options = ['q', 'r', 'b', 'n']
        self.tile_size = screen.get_width() // 8
        self.width = self.tile_size * len(self.options)
        self.height = self.tile_size
        self.padding = 10

        self.bg_color = (200, 255, 200) 

        screen_rect = self.screen.get_rect()
        self.x = (screen_rect.width - self.width - 2 * self.padding) // 2
        self.y = (screen_rect.height - self.height - 2 * self.padding) // 2

        self.rects = []
        for i in range(len(self.options)):
            rect = pygame.Rect(
                self.x + self.padding + i * self.tile_size,
                self.y + self.padding,
                self.tile_size,
                self.tile_size
            )
            self.rects.append(rect)

    def draw(self):
        
        bg_rect = pygame.Rect(
            self.x,
            self.y,
            self.width + 2 * self.padding,
            self.height + 2 * self.padding
        )
        pygame.draw.rect(self.screen, self.bg_color, bg_rect, border_radius=8)

       
        for i, piece_code in enumerate(self.options):
            image = self.piece_images[self.color][piece_code]
            scaled = pygame.transform.scale(image, (self.tile_size, self.tile_size))
            self.screen.blit(scaled, self.rects[i].topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    selected_piece = self.options[i]
                    self.callback(selected_piece)
                    return True 
        return False 
