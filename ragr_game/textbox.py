import pygame


class Textbox:

    def __init__(self, font_size, font_name, rect):
        self.font_size = font_size
        self.rect = pygame.Rect(rect)
        self.text = ""
        self.active = False
        self.font = pygame.font.Font(font_name, font_size)

    def event_handler(self, event):
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #  self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return self.text
            elif len(self.text) < 24:
                self.text += event.unicode

    def clear_text(self):
        self.text = ""

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def draw(self, surface):
        # color = (255, 255, 255) if self.active else (180, 180, 180)
        # pygame.draw.rect(surface, (30, 30, 30), self.rect, border_radius=4)
        # pygame.draw.rect(surface, color, self.rect, 2, border_radius=4)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
