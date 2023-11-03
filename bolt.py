import pygame
import main

class Bolt(pygame.sprite.Sprite):
    """
     takes three parameters in its constructor. An X and Y value, for the initial spawn point, and a direction (d).
    """
    def __init__(self, x, y, d):
        super().__init__()
        self.image = pygame.image.load("png/bolt.png")
        self.rect = self.image.get_rect()
        self.rect.x = x + 15 # offset the position of the bolt
        self.rect.y = y + 20 # offset the position of the bolt
        self.direction = d

    def fire(self):

        if -10 < self.rect.x < 710:
            if self.direction == 0:
                self.image = pygame.image.load("png/bolt.png")
                main.displaysurface.blit(self.image, self.rect)
            else:
                self.image = pygame.image.load("png/bolt.png")
                main.displaysurface.blit(self.image, self.rect)

            if self.direction == 0:
                self.rect.move_ip(12, 0)
            else:
                self.rect.move_ip(-12, 0)
        else:
            self.kill()

        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, main.playergroup, False)
        if hits:
            main.player.player_hit()
            self.kill()