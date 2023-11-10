import numpy
import pygame
import main
import random
from item import Item
from bolt import Bolt


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.enemy_hp = 2
        self.pos = main.vec(0, 0)
        self.vel = main.vec(0, 0)

        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(3, 9) / 3  # Randomized velocity of the generated enemy
        self.mana = random.randint(2, 3)  # Randomized mana amount obtained upon
        if self.direction == 0: self.image = pygame.image.load("png/enemy2_sprite_right.png")
        if self.direction == 1: self.image = pygame.image.load("png/enemy2_sprite_left.png")
        self.rect = self.image.get_rect()
        # Sets the initial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 250
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 250
        self.movement_frame = 0
        self.movement = True
        self.wait_frames = 0
        self.wait = False
        self.shooting = False

    def move(self):
        if main.cursor.wait == 1: return
        if self.movement:
            pygame.draw.rect(main.displaysurface, (255, 0, 0), self.rect, 2)  # hitbox
            # Causes the enemy to change directions upon reaching the end of screen
            if self.pos.x >= (main.WIDTH - 20):
                self.direction = 1

                self.image = pygame.image.load("png/enemy2_sprite_left.png")
            elif self.pos.x <= 0:
                self.direction = 0

                self.image = pygame.image.load("png/enemy2_sprite_right.png")
            # Updates position with new values

            if self.direction == 0:
                self.pos.x += self.vel.x
                self.movement_frame += 1

            elif self.direction == 1:
                self.pos.x -= self.vel.x
                self.movement_frame += 1

            rand_num = numpy.random.uniform(0, 70)
            """if int(rand_num) < 1:
                bolt = Bolt(self.pos.x, self.pos.y, self.direction)
                main.bolts.add(bolt)"""

            self.rect.topleft = self.pos  # Updates rect
        else:
            self.rect.topleft = self.pos  # Updates rect

    def update(self):
        if self.movement_frame == 180 and self.shooting == False:  # stops moving after 3 secs
            self.movement = False
            #rand_num = int(numpy.random.uniform(1, 3))
            bolt = Bolt(self.pos.x, self.pos.y, self.direction)
            main.bolts.add(bolt)
            self.shooting = True
            self.wait = True # enemy2 set in a waiting status
        if self.wait == True:
            self.wait_frames += 1
            self.movement_frame = 0
        if self.wait_frames == 60: # waits 1 sec before moving again
            self.shooting = False # enemy2 can shoot again
            self.wait = False # it's not waiting anymore
            self.wait_frames = 0 # resets wait frames
            self.movement = True # enemy2 can move again

        hits = pygame.sprite.spritecollide(self, main.playergroup, False)
        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, main.fireballs, False)

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
                item = Item(item_no)  # create health/money item
                main.items.add(item)  # add the item to the items group
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y
            if main.player.mana < 100:  # limit the mana to 100
                main.player.mana += self.mana  # add the dropped mana to the player
            main.mmanager.playsound(main.enemy_hit, 0.05)
            self.kill()
            main.handler.dead_enemy_count += 1  # increments the dead_enemy_count variable when the kill() command is being called.
            print("Enemy killed")

    def render(self):
        # Displays the enemy on screen
        main.displaysurface.blit(self.image, self.rect)
