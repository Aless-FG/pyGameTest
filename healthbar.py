import pygame

HEIGHT = 350
WIDTH = 730
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("png/heart5.png")

    def render(self):
        displaysurface.blit(self.image, (10, 10))