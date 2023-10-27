import random
import pygame

import main

HEIGHT = 350
WIDTH = 730
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
vec = pygame.math.Vector2
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("png/Enemy.png")
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)

        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(2, 6) / 2  # Randomized velocity of the generated enemy

        # Sets the initial position of the enemy
        if self.direction == 0: # it spawns to the left
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1: # it spawns to the right
            self.pos.x = 700
            self.pos.y = 235

    def move(self):
        # Causes the enemy to change directions upon reaching the end of screen
        """
        The reason why we are comparing to WIDTH - 20 instead of WIDTH is to keep a little margin between the enemy and the screen.
         If we were to use WIDTH, the enemy would be midway out of the screen before changing directions.
        (This is because pos.x returns the x-coordinate of the middle of the enemy)

        """
        if self.pos.x >= (WIDTH - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0

        # Updates position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos  #  If not for this, the “rect” of the enemy would be left behind at the initial spawn point and collisions would not occur accurately

    def update(self):  # Checks for collision with the Player

        hits = pygame.sprite.spritecollide(self, main.playergroup, False)

        """If the player is currently in an attack mode, it means that the collision has occurred due to the player’s attack. 
        Thus, we kill off the enemy sprite using the kill() command."""
        if hits and main.player.attacking == True:
            self.kill()
            print("Enemy killed")

        # If collision has occurred and player not attacking, call "hit" function
        elif hits and main.player.attacking == False:
            main.player.player_hit()
    def render(self):
        # Displayed the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))
