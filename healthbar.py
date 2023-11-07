import pygame

import main

HEIGHT = 350
WIDTH = 730
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))



class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("png/heart_sprite.png")
        self.image_empty = pygame.image.load("png/heart_sprite_empty.png")
        self.image_heart_extended = pygame.image.load("png/heart_sprite_extend.png")
        self.heart_refill_frame = 0
        self.hearts = []
        for i in range(main.player.health):
            self.hearts.append(self.image)
        self.extended_hearts = []

    def render(self):  # renders player's hp

        distance = 20
        for h in self.hearts:
            if main.player.dmg >= 1:
                self.hearts[main.player.max_health - main.player.dmg] = self.image_empty  # place a white heart if the player took dmg
            displaysurface.blit(h, (distance, 10))

            distance += 20
