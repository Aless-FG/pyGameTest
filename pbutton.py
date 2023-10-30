import pygame
import main

vec = pygame.math.Vector2
class PButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.vec = vec(620, 300) # button's position
        self.imgdisp = 0 #  will keep track of the button mode, and will have a value of either 0 or 1.

    def render(self, num): # num is used to determine which image to display
        if num == 0:
            self.image = pygame.image.load("png/home_small.png")
        elif num == 1:
            if main.cursor.wait == 0: #cursor.wait is used to determine which image is to be displayed
                self.image = pygame.image.load("png/pause_small.png")
            else:
                self.image = pygame.image.load("png/play_small.png")

        main.displaysurface.blit(self.image, self.vec)