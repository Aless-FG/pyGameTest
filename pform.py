import pygame
import random
import main
HEIGHT = 350
WIDTH = 730

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((100, 18))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (150,190))
        self.hide = False

    def render(self):
        if self.hide == False:
            main.displaysurface.blit(self.surf, self.rect)