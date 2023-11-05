import random
import pygame
import numpy
import main
from item import Item
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
        self.enemy_hp = 6
        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(2, 6) / 2  # Randomized velocity of the generated enemy
        self.mana = random.randint(1, 3)  # the enemy will drop a random amount of mana
        self.money = random.randint(3, 5)  # the enemy will drop a random amount of money
        # Sets the initial position of the enemy
        if self.direction == 0: # it spawns to the left, goes to the right
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1: # it spawns to the right, goes to the left
            self.pos.x = 700
            self.pos.y = 235
        self.smallerfont = pygame.font.SysFont('notosansmono', 16)
        self.fmj_cooldown = pygame.USEREVENT + 3
        self.cooldown = False

    def move(self):
        if main.cursor.wait == 1: return
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

    def update(self):

        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, main.playergroup, False)
        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, main.fireballs, False)
        """If the player is currently in an attack mode, it means that the collision has occurred due to the player’s attack. 
        Thus, we kill off the enemy sprite using the kill() command."""
        if hits and main.player.attacking == True:
            if self.direction == 0 and main.player.direction == "LEFT": # knockback to the left
                self.pos.x -= 40
                self.rect.center = self.pos
                self.enemy_hp -= 1
                print("Enemy hit")
            elif self.direction == 1 and main.player.direction == "RIGHT": # knockback to the right
                self.pos.x += 40
                self.rect.center = self.pos
                self.enemy_hp -= 1
                print("Enemy hit")
        if f_hits and main.player.fmj == False:
            print("Enemy hit w/ a fireball")
            self.enemy_hp -= 3
            print(self.enemy_hp)
            main.fireball.kill()
        elif f_hits and self.cooldown == False:
            self.cooldown = True
            pygame.time.set_timer(self.fmj_cooldown, 500)
            print("Enemy hit w/ a fireball (FMJ)")
            print(self.enemy_hp)
            self.enemy_hp -= 3

        if self.enemy_hp == 0:
            rand_num = numpy.random.uniform(0, 100) #  random.uniform has a uniform spread
            item_no = 0
            if rand_num >= 0 and rand_num <= 5:  # 6% chance of a health drop
                item_no = 1
            elif rand_num > 5 and rand_num <= 99: # 10% chance of a money drop
                item_no = 2
            if item_no != 0:
                # Add Item to Items group
                item = Item(item_no) # create health/money item
                main.items.add(item) # add the item to the items group
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y
            if main.player.mana < 100: # limit the mana to 100
                main.player.mana += self.mana # add the dropped mana to the player

            main.mmanager.playsound(main.enemy_hit, 0.05)
            self.kill()
            main.handler.dead_enemy_count += 1 # increments the dead_enemy_count variable when the kill() command is being called.
            print("Enemy killed")

        # If collision has occurred and player not attacking, call "hit" function
        elif hits and main.player.attacking == False:
            main.player.player_hit()
        # shows enemy hp
        text_hp = self.smallerfont.render(str(self.enemy_hp), True, (255, 0, 0))
        displaysurface.blit(text_hp, (self.pos.x + 17, self.pos.y - 30))
    def render(self):
        # Displayed the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))
