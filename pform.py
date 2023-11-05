import pygame
import random
import main
HEIGHT = 350
WIDTH = 730

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((200, 18))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (150,170))
        self.hide = False
        self.destroy = False

    def render(self):
        if self.hide == False and self.destroy == False:
            main.displaysurface.blit(self.surf, self.rect)
    def destroy_platform(self):
        self.destroy = True
        self.hide = True
        self.kill()
