import pygame
from pygame.locals import K_LEFT, K_RIGHT

import main


class Player(pygame.sprite.Sprite):  # inherits from the pygame.sprite.Sprite class
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("png/Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = main.vec((340, 240))  # position of the player
        self.vel = main.vec(0, 0)  # velocity of the player
        self.acc = main.vec(0, 0)  # acceleration of the player
        self.direction = "RIGHT"  # used to store the current direction of the Player
        self.jumping = False
        self.running = False
        self.move_frame = 0  # track the current frame of the character being displayed
        self.attacking = False
        self.attack_frame = 0
        self.cooldown = False
        self.max_health = 8
        self.health = self.max_health
        self.extended_hp = 0
        self.dmg = 0  # damage taken by the player
        self.mana = 90
        self.money = 90
        self.xp = 0
        self.magic_cooldown = True  # the player can use a fireball/iceball
        self.slash = 0  # needed for the sound effect
        self.fmj = False  # fmj power up
        self.double_jump_display = False
        self.double_jump = False
        self.smallerfont = pygame.font.SysFont('notosansmono', 16)


    def move(self):

        self.acc = main.vec(0, 0.5)  # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
        # Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3:  # use abs() to return the magnitude since the velocity can be in the negative direction (the left direction)
            self.running = True
        else:
            self.running = False

        pressed_keys = pygame.key.get_pressed()  # Returns the current key presses

        # Accelerates the player in the direction of the key press
        if pressed_keys[pygame.K_a]:
            self.acc.x = -main.ACC
        if pressed_keys[pygame.K_d]:
            self.acc.x = main.ACC
        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * main.FRIC  # updates object's acceleration
        self.vel += self.acc  # updates object's velocity
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values
        """
        This causes character warping from one point of the screen to the other
        If you want to disable this feature, swap the 0 and WIDTH values of self.pos.x statements within the if statements. 
        This will create the opposite effect, not allowing the Player to move past the edge.
        """
        if self.pos.x > main.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = main.WIDTH

        self.rect.midbottom = self.pos  # Update rect with new pos

    def update(self):  # This function is in charge of changing the movement frame of the Player if he's moving.
        if main.cursor.wait == 1: return
        pygame.draw.rect(main.displaysurface, (255, 0, 0), self.rect, 5)


        if self.move_frame > 6:
            self.move_frame = 0
            return
        if self.jumping == False and self.running == True:
            """
            If the player’s velocity is greater than 0, then that means that he is moving in the right direction.
             Otherwise he is going in the left.
            """
            if self.vel.x > 0:
                self.image = main.run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            else:
                self.image = main.run_ani_L[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1
            # Returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = main.run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = main.run_ani_L[self.move_frame]

    def attack(self):
        if main.cursor.wait == 1: return
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False

        if self.attack_frame == 0:  # ensures that the sound is only played on the first attack frame
            main.mmanager.playsound(main.swordtrack[self.slash], 0.05)

            self.slash += 1
            if self.slash >= 4:
                self.slash = 0
            # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = main.attack_ani_R[self.attack_frame]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.pos.x, self.pos.y)  # Adjust the top left corner to match the player's position
            self.rect.width = self.image.get_width()  # Set the width to match the image's width
            self.rect.height = self.image.get_height()  # Set the height to match the image's height
        elif self.direction == "LEFT":
            self.correction()
            self.image = main.attack_ani_L[self.attack_frame]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.pos.x, self.pos.y)  # Adjust the top left corner to match the player's position
            self.rect.width = self.image.get_width()  # Set the width to match the image's width
            self.rect.height = self.image.get_height()  # Set the height to match the image's height
            # Update the current attack frame
        self.attack_frame += 1

    def player_hit(self):
        if self.cooldown == False:
            self.cooldown = True  # Enable the cooldown
            """
            set_timer() function which will take two parameters, a UserEvent and a time interval.
             The UserEvent will be sent out as an event signal
            """
            pygame.time.set_timer(main.hit_cooldown, 1000)  # Resets cooldown in 1 second

            print("hit")
            self.health -= 1
            self.dmg += 1
            # health.image = health_ani[self.health]

            if self.health <= 0:
                main.mmanager.stop()
                main.mmanager.playsoundtrack(main.soundtrack[2], -1, 0.1)
                self.kill()
                """
                 display_update() function is an optional feature, used for when you want to update the screen immediately 
                 instead of waiting for the game loop
                """
                pygame.display.update()
            pygame.display.update()

    def jump(self):
        self.rect.x += 1

        # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, main.ground_group, False)
        pl_hits = pygame.sprite.spritecollide(self, main.platform_group, False)
        self.rect.x -= 1

        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12
        elif pl_hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

    def double_jump_powerup(self):
        self.rect.x += 1
        self.rect.x -= 1
        self.mana -= 5 #
        self.vel.y = -7



    def correction(self):
        # Function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.pos.x -= 20
        if self.attack_frame == 10:
            self.pos.x += 20
    def mana_restore(self):
        pl_hits = pygame.sprite.spritecollide(self, main.platform_group, False)
        if pl_hits and self.mana <= 99 and self.money >= 0:
            self.mana += 1
            self.money -= 0.5

    def gravity_check(self):
        # takes three parameters, the sprite to be tested, and secondly the sprite group against which the sprite will be tested.
        # The third parameter takes a True or False value which determines whether to kill the sprite if a collision occurs
        hits = pygame.sprite.spritecollide(self, main.ground_group, False)
        pl_hits = pygame.sprite.spritecollide(self, main.platform_group, False)
        """
        check whether the player has any velocity in the downwards direction. 
        If he doesn’t, then all is good (because he isn’t falling and thus is on the ground). 
        If however he is falling we will proceed.
        """
        if self.vel.y > 0:
            if hits:  # will run if the hits variable recorded a collision between the player and ground

                """
                selects the first ground object from the list of hits. 
                The assumption here is that the first ground object in the list is the one closest to the player's current position along the y-axis.
                """
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:  # checks if the player's y-coordinate (vertical position) is higher (less than) the bottom y-coordinate of the lowest ground object's bounding rectangle.
                    self.pos.y = lowest.rect.top + 1  # sets the player's y-coordinate to just above the top of the ground object, effectively preventing the player from falling through the ground.
                    self.vel.y = 0  # sets the player's vertical velocity to 0, effectively stopping any downward movement due to gravity.
                    self.jumping = False
                    #self.double_jump = True
            elif pl_hits:  # player is on a platform
                self.mana_restore()
                lowest = pl_hits[0]
                if self.pos.y < lowest.rect.bottom:  # checks if the player's y-coordinate (vertical position) is higher (less than) the bottom y-coordinate of the lowest ground object's bounding rectangle.
                    self.pos.y = lowest.rect.top + 1  # sets the player's y-coordinate to just above the top of the ground object, effectively preventing the player from falling through the ground.
                    self.vel.y = 0  # sets the player's vertical velocity to 0, effectively stopping any downward movement due to gravity.
                    self.jumping = False
                    #self.double_jump = True
                if main.player.attacking == True or main.player.running and main.fireballs or main.iceballs:
                    main.p1.destroy_platform()

