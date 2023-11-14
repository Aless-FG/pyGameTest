import os

import pygame
import random
import main
HEIGHT = 350
WIDTH = 730

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((200, 18))
        self.image = pygame.image.load("png/platform_anim/Sprite-0001.png")
        self.rect = self.surf.get_rect(center = (150,170))
        self.hide = False
        self.destroy = False
        self.background_files = []
        self.current_bg_index = 0

        for root, dirs, files in os.walk("/home/ale/PycharmProjects/pyGameTest/png/platform_anim"):
            for file in files:
                if file.endswith(".png"):
                    self.background_files.append(os.path.join(root, file))

        self.background_files.sort(key=lambda x: int(''.join(filter(str.isdigit, os.path.splitext(x)[0]))))
        self.frame_count = 0
        self.frame_rate = 8
        self.playing_forward = True

    def render(self):
        if self.hide == False and self.destroy == False:
            main.displaysurface.blit(self.image, self.rect)

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

            self.image = pygame.image.load(self.background_files[self.current_bg_index])
        self.frame_count += 1

    def destroy_platform(self):
        self.destroy = True
        self.hide = True
        self.kill()
