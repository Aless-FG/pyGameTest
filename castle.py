import pygame

HEIGHT = 350
WIDTH = 730
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))


class Castle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hide = False
        self.image = pygame.image.load("png/castle.png")

    def update(self):
        if self.hide == False:
            displaysurface.blit(self.image, (400, 80))