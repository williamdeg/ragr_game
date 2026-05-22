import pygame


class Button:

    def __init__(self, rect, name="button"):
        self.rect = pygame.Rect(rect)

    def pressed(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
            event.pos
        )
