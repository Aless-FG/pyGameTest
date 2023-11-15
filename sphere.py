import os
import pygame
import main

HEIGHT = 350
WIDTH = 730
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))



class Sphere(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("png/sphere_anim/Sprite-0002.png").convert_alpha()
        self.image_interact = pygame.image.load("png/sphere_interact_sprite.png").convert_alpha()
        self.bgY = 230
        self.bgX = 600
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 230
        self.sphere_files = []
        self.hide = True
        self.current_bg_index = 0

        for root, dirs, files in os.walk("/home/ale/PycharmProjects/pyGameTest/png/sphere_anim"):
            for file in files:
                if file.endswith(".png"):
                    self.sphere_files.append(os.path.join(root, file))

        self.sphere_files.sort(key=lambda x: int(''.join(filter(str.isdigit, os.path.splitext(x)[0]))))
        self.frame_count = 0
        self.frame_rate = 10
        self.playing_forward = True

    def render(self):
        if self.hide == False:
            if main.player.rect.colliderect(self.rect): # draw highlighted sphere if in contact w/ player
                displaysurface.blit(self.image_interact, (self.bgX, self.bgY))
            else:
                displaysurface.blit(self.image, (self.bgX, self.bgY))

    def update(self):
        # Change background every self.frame_rate frames
        if self.frame_count % self.frame_rate == 0:
            if self.playing_forward:
                self.current_bg_index += 1
            else:
                self.current_bg_index -= 1

            if self.current_bg_index == len(self.sphere_files) - 1: # if the animation going forward has completed
                self.playing_forward = False
            elif self.current_bg_index == 0:
                self.playing_forward = True

            self.image = pygame.image.load(self.sphere_files[self.current_bg_index])
        self.frame_count += 1
