import pygame

import main

HEIGHT = 350
WIDTH = 730
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("png/ground_sprite.png")
        self.image2 = pygame.image.load("png/ground_test.png")
        """
        Using the get_rect() method on the image object will return a rectangle object of the same dimensions as the image
        The center argument specifies where the center of the rectangle should be placed. In this case, it's set to (350, 350),
        which means that the center of the Rect is positioned at coordinates (350, 350) on the game screen.
        """
        self.rect = self.image.get_rect(center=(350, 350))

    def render(self):
        if main.handler.stage == 1:
            displaysurface.blit(self.image, (self.rect.x, self.rect.y))
        elif main.handler.stage == 2:
            displaysurface.blit(self.image2, (self.rect.x, self.rect.y))