import numpy
import pygame
import main
import random


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.enemy_hp = 2
        self.pos = main.vec(0, 0)
        self.vel = main.vec(0, 0)

        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(2, 6) / 3  # Randomized velocity of the generated enemy
        self.mana = random.randint(2, 3)  # Randomized mana amount obtained upon
        if self.direction == 0: self.image = pygame.image.load("png/enemy2.png")
        if self.direction == 1: self.image = pygame.image.load("png/enemy2.png")
        self.rect = self.image.get_rect()
        self.wait = 0
        self.wait_status = False
        self.turning = 0  # tracks the state of the enemy
        # Sets the initial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 250
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 250

    def move(self):
        if main.cursor.wait == 1: return

        # Causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (main.WIDTH - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0

        # Updates position with new values
        """
        every 50 frames, the enemy will stop. And then stay still for another 50 frames (in which he will attack). 
        Then he will proceed to move forward for another 50 frames.
        """
        if self.wait > 100:
            self.wait_status = True
        elif int(self.wait) <= 0:
            self.wait_status = False

        """if wait_status is true, then the Enemy will not move, instead it will go into the if block where the decrement self.wait. 
        This will continue until self.wait is at 0 or less.
        
        if self.wait_status == True:
            self.wait -= 1"""
        if self.direction == 0:
            self.pos.x += self.vel.x
            self.wait += self.vel.x  # For every pixel the enemy moves, the value of self.wait is increment by 1
        elif self.direction == 1:
            self.pos.x -= self.vel.x
            self.wait += self.vel.x

        """if self.direction_check():
            self.turn()
            self.wait = 90  # the Enemy waits for 90 frames before turning
            self.turning = 1"""

        self.rect.topleft = self.pos  # Updates rect

    def update(self):
        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, main.playergroup, False)
        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, main.fireballs, False)
        """If the player is currently in an attack mode, it means that the collision has occurred due to the player’s attack. 
        Thus, we kill off the enemy sprite using the kill() command."""
        if hits and main.player.attacking == True:
            if self.direction == 0 and main.player.direction == "LEFT":  # knockback to the left
                self.pos.x -= 40
                self.rect.center = self.pos
                self.enemy_hp -= 1
                print("Enemy hit")
            elif self.direction == 1 and main.player.direction == "RIGHT":  # knockback to the right
                self.pos.x += 40
                self.rect.center = self.pos
                self.enemy_hp -= 1
                print("Enemy hit")
        if f_hits:
            self.enemy_hp = 0

        if self.enemy_hp == 0:
            rand_num = numpy.random.uniform(0, 100)  # random.uniform has uniform spread
            item_no = 0
            if rand_num >= 0 and rand_num <= 5:  # 6% chance of a health drop
                item_no = 1
            elif rand_num > 5 and rand_num <= 15:  # 10% chance of a money drop
                item_no = 2
            if item_no != 0:
                # Add Item to Items group
                item = main.Item(item_no)  # create health/money item
                main.items.add(item)  # add the item to the items group
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y
            if main.player.mana < 100:  # limit the mana to 100
                main.player.mana += self.mana  # add the dropped mana to the player
            self.kill()
            main.handler.dead_enemy_count += 1  # increments the dead_enemy_count variable when the kill() command is being called.
            print("Enemy killed")

    def direction_check(self):  # If 1 is returned, then that means we need to change the direction of the enemy
        # if the player is behind the enemy and the enemy is going to the right
        if main.player.pos.x - self.pos.x < 0 and self.direction == 0:
            print(1)
            return 1
        # if the player is behind the enemy and the enemy is going to the left
        elif main.player.pos.x - self.pos.x > 0 and self.direction == 1:
            print(2)
            return 1
        else:
            return 0

    """
    that for a game running at 60 FPS, setting self.wait to 90 makes the enemy pause for 1.5 seconds,
     before turning around. ( 90 divided by 60). 
    """
    def turn(self):
        if self.wait > 0:
            self.wait -= 1
            return
        elif int(self.wait) <= 0:
            self.turning = 0

        if self.direction:
            self.direction = 0
            self.image = pygame.image.load("png/airplane_left.png")
        else:
            self.direction = 1
            self.image = pygame.image.load("png/airplane_right.png")

    def render(self):
        # Displays the enemy on screen
        main.displaysurface.blit(self.image, self.rect)
