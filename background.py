import pygame

HEIGHT = 350
WIDTH = 730
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("png/Background.png")
        # self.bgY and self.bgX store the X and Y position of the background
        self.bgY = 0
        self.bgX = 0

    def render(self):
        # will draw the background image with ( 0 , 0 ) as the origin point
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY)) # stores the pygame window object