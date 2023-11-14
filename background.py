import os

import pygame
from os import walk

HEIGHT = 350
WIDTH = 730
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))



class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("png/background_sprite.png")
        # self.bgY and self.bgX store the X and Y position of the background
        self.bgY = 0
        self.bgX = 0
        self.background_files = []
        self.current_bg_index = 0
        self.bgY = 0
        for root, dirs, files in os.walk("/home/ale/PycharmProjects/pyGameTest/png/bg_anim"):
            for file in files:
                if file.endswith(".png"):
                    self.background_files.append(os.path.join(root, file))

        self.background_files.sort(key=lambda x: int(''.join(filter(str.isdigit, os.path.splitext(x)[0]))))
        self.frame_count = 0
        self.frame_rate = 5
        self.playing_forward = True

    def render(self):
        # will draw the background image with ( 0 , 0 ) as the origin point
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY)) # stores the pygame window object

    def update(self):
        # Change background every self.frame_rate frames
        if self.frame_count % self.frame_rate == 0:
            if self.playing_forward:
                self.current_bg_index += 1
            else:
                self.current_bg_index -= 1

            if self.current_bg_index == len(self.background_files) - 1: # if the animation going forward has completed
                self.playing_forward = False
            elif self.current_bg_index == 0:
                self.playing_forward = True

            self.bgimage = pygame.image.load(self.background_files[self.current_bg_index])
        self.frame_count += 1
