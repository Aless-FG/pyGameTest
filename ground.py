import pygame

HEIGHT = 350
WIDTH = 730
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("png/Ground.png")
        self.rect = self.image.get_rect(center=(350, 350))

    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))