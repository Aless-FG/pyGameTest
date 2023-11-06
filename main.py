import pygame
from pygame.locals import *
import sys
from background import Background
from castle import Castle
from ground import Ground
from enemy import Enemy
from tkinter import Tk, Button
from healthbar import HealthBar
from fireball import Fireball
from pform import Platform
from stagedisplay import StageDisplay
from statusbar import StatusBar
from pbutton import PButton
from enemy2 import Enemy2
from musicmanager import MusicManager

# freq, size, channel, buffsize
pygame.mixer.pre_init(44100, 16, 1, 512)
pygame.init()  # Begin pygame

# Declaring variables to be used through the program
vec = pygame.math.Vector2  # used to record X and Y position of the player
HEIGHT = 350
WIDTH = 730
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
hit_cooldown = pygame.USEREVENT + 1  # need to create a new custom event
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))  # displays the game using width and height
pygame.display.set_caption("Game")  # changes window's title

run_ani_R = [pygame.image.load("png/Player_Sprite_R.png").convert_alpha(), pygame.image.load("png/Player_Sprite2_R.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite3_R.png").convert_alpha(), pygame.image.load("png/Player_Sprite4_R.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite5_R.png").convert_alpha(), pygame.image.load("png/Player_Sprite6_R.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite_R.png").convert_alpha()]

# Run animation for the LEFT
run_ani_L = [pygame.image.load("png/Player_Sprite_L.png").convert_alpha(), pygame.image.load("png/Player_Sprite2_L.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite3_L.png").convert_alpha(), pygame.image.load("png/Player_Sprite4_L.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite5_L.png").convert_alpha(), pygame.image.load("png/Player_Sprite6_L.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite_L.png").convert_alpha()]

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("png/Player_Sprite_R.png").convert_alpha(), pygame.image.load("png/Player_Attack_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack2_R.png").convert_alpha(), pygame.image.load("png/Player_Attack2_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack3_R.png").convert_alpha(), pygame.image.load("png/Player_Attack3_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack4_R.png").convert_alpha(), pygame.image.load("png/Player_Attack4_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack5_R.png").convert_alpha(), pygame.image.load("png/Player_Attack5_R.png").convert_alpha(),
                pygame.image.load("png/Player_Sprite_R.png").convert_alpha()]

# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("png/Player_Sprite_L.png").convert_alpha(), pygame.image.load("png/Player_Attack_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack2_L.png").convert_alpha(), pygame.image.load("png/Player_Attack2_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack3_L.png").convert_alpha(), pygame.image.load("png/Player_Attack3_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack4_L.png").convert_alpha(), pygame.image.load("png/Player_Attack4_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack5_L.png").convert_alpha(), pygame.image.load("png/Player_Attack5_L.png").convert_alpha(),
                pygame.image.load("png/Player_Sprite_L.png").convert_alpha()]

health_ani = [pygame.image.load("png/heart0.png").convert_alpha(), pygame.image.load("png/heart.png").convert_alpha(),
              pygame.image.load("png/heart2.png").convert_alpha(), pygame.image.load("png/heart3.png").convert_alpha(),
              pygame.image.load("png/heart4.png").convert_alpha(), pygame.image.load("png/heart5.png").convert_alpha()]

# Music and Sound
soundtrack = ["tracks/background_village.wav", "tracks/battle_music.wav", "tracks/gameover.wav"]
swordtrack = [pygame.mixer.Sound("tracks/sword1.wav"), pygame.mixer.Sound("tracks/sword2.wav"),
              pygame.mixer.Sound("tracks/sword3.wav"), pygame.mixer.Sound("tracks/sword4.wav")]
fireball_sound = pygame.mixer.Sound("tracks/fireball_sound.wav")
enemy_hit = pygame.mixer.Sound("tracks/enemy_hit.wav")

mmanager = MusicManager()
mmanager.playsoundtrack(soundtrack[0], -1, 0.05) # The second parameter states that it should repeat infinitely
class Player(pygame.sprite.Sprite):  # inherits from the pygame.sprite.Sprite class
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("png/Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))  # position of the player
        self.vel = vec(0, 0)  # velocity of the player
        self.acc = vec(0, 0)  # acceleration of the player
        self.direction = "RIGHT"  # used to store the current direction of the Player
        self.jumping = False
        self.running = False
        self.move_frame = 0  # track the current frame of the character being displayed
        self.attacking = False
        self.attack_frame = 0
        self.cooldown = False
        self.health = 5
        self.mana = 90
        self.money = 10
        self.xp = 0
        self.magic_cooldown = True # the player can use a fireball
        self.slash = 0 # needed for the sound effect
        self.fmj = False

    def move(self):

        self.acc = vec(0, 0.5)  # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
        # Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3:  # use abs() to return the magnitude since the velocity can be in the negative direction (the left direction)
            self.running = True
        else:
            self.running = False

        pressed_keys = pygame.key.get_pressed()  # Returns the current key presses

        # Accelerates the player in the direction of the key press
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC  # updates object's acceleration
        self.vel += self.acc  # updates object's velocity
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values
        """
        This causes character warping from one point of the screen to the other
        If you want to disable this feature, swap the 0 and WIDTH values of self.pos.x statements within the if statements. 
        This will create the opposite effect, not allowing the Player to move past the edge.
        """
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos  # Update rect with new pos

    def update(self):  # This function is in charge of changing the movement frame of the Player if he's moving.
        if cursor.wait == 1: return
        pygame.draw.rect(displaysurface, (255, 0, 0), self.rect, 5)
        if self.move_frame > 6:
            self.move_frame = 0
            return
        if self.jumping == False and self.running == True:
            """
            If the player’s velocity is greater than 0, then that means that he is moving in the right direction.
             Otherwise he is going in the left.
            """
            if self.vel.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            else:
                self.image = run_ani_L[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1
            # Returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = run_ani_L[self.move_frame]

    def attack(self):
        if cursor.wait == 1: return
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False

        if self.attack_frame == 0: # ensures that the sound is only played on the first attack frame
            mmanager.playsound(swordtrack[self.slash], 0.05)

            self.slash += 1
            if self.slash >= 4:
                self.slash = 0
            # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_ani_R[self.attack_frame]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.pos.x, self.pos.y)  # Adjust the top left corner to match the player's position
            self.rect.width = self.image.get_width()  # Set the width to match the image's width
            self.rect.height = self.image.get_height()  # Set the height to match the image's height
        elif self.direction == "LEFT":
            self.correction()
            self.image = attack_ani_L[self.attack_frame]
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
            pygame.time.set_timer(hit_cooldown, 1000)  # Resets cooldown in 1 second

            print("hit")
            self.health = self.health - 1
            health.image = health_ani[self.health]

            if self.health <= 0:
                mmanager.stop()
                mmanager.playsoundtrack(soundtrack[2], -1, 0.1)
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
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        pl_hits = pygame.sprite.spritecollide(self, platform_group, False)
        self.rect.x -= 1

        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12
        elif pl_hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

    def correction(self):
        # Function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.pos.x -= 20
        if self.attack_frame == 10:
            self.pos.x += 20

    def gravity_check(self):
        # takes three parameters, the sprite to be tested, and secondly the sprite group against which the sprite will be tested.
        # The third parameter takes a True or False value which determines whether to kill the sprite if a collision occurs
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        pl_hits = pygame.sprite.spritecollide(self, platform_group, False)
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
            elif pl_hits: # player is on a platform


                lowest = pl_hits[0]
                if self.pos.y < lowest.rect.bottom:  # checks if the player's y-coordinate (vertical position) is higher (less than) the bottom y-coordinate of the lowest ground object's bounding rectangle.
                    self.pos.y = lowest.rect.top - 1  # sets the player's y-coordinate to just above the top of the ground object, effectively preventing the player from falling through the ground.
                    self.vel.y = 0  # sets the player's vertical velocity to 0, effectively stopping any downward movement due to gravity.
                    self.jumping = False
                if player.attacking == True and fireballs:
                    p1.destroy_platform()


class EventHandler():
    def __init__(self):

        self.stage = 1
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 2 # generates enemies in world 1
        self.enemy_generation2 = pygame.USEREVENT + 3 # generates enemies in world 2
        self.world = 0
        self.stage_enemies = []  # enemies generation
        for x in range(1, 21):
            self.stage_enemies.append(int((x ** 2 / 2) + 1))  # number of enemies to be generated per level

    def next_stage(self):  # Code for when the next stage is clicked
        button.imgdisp = 1  # This ensures that the button is converted to Pause/Play mode when a world begins
        self.stage += 1
        self.enemy_count = 0
        self.dead_enemy_count = 0
        print("Stage: " + str(self.stage))
        # The higher the stage number, the lower the time gap between enemy spawns, meaning harder levels
        if self.world == 1:
            pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))  # sets the timer for enemy generation
        elif self.world == 2:
            print("SIUM WORLD2")
            pygame.time.set_timer(self.enemy_generation2, 1500 - (50 * self.stage))
    def update(self):
        if self.dead_enemy_count == self.stage_enemies[self.stage - 1]:  # if all the enemies have been killed
            self.dead_enemy_count = 0  # resets the counter
            stage_display.clear = True  # the text can now be displayed
            stage_display.stage_clear()  # shows stage clear when there are no more enemies

    def home(self):
        # Reset Battle code
        pygame.time.set_timer(self.enemy_generation, 0) # disables enemies generation (world 1)
        pygame.time.set_timer(self.enemy_generation2, 0)  # disables enemies generation (world 2)
        self.battle = False
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 0
        self.world = 0

        # Destroy any enemies or items lying around
        for group in enemies:  # , items
            for entity in group:
                entity.kill()

        # Bring back normal backgrounds
        castle.hide = False
        background.bgimage = pygame.image.load("png/Background.png")
        ground.image = pygame.image.load("png/Ground.png")
        button.render(button.imgdisp) # renders home or pause button
        cursor.hover()

    def stage_handler(self):  # starting menu
        # Code for the Tkinter stage selection window

        self.root = Tk()
        self.root.geometry('200x170')

        button1 = Button(self.root, text="Twilight Dungeon", width=18, height=2,
                         command=self.world1)
        button2 = Button(self.root, text="Skyward Dungeon", width=18, height=2,
                         command=self.world2)
        button3 = Button(self.root, text="Hell Dungeon", width=18, height=2,
                         command=self.world3)

        button1.place(x=40, y=15)
        button2.place(x=40, y=65)
        button3.place(x=40, y=115)

        self.root.mainloop()

    def world1(self):

        self.world = 1
        self.root.destroy()
        castle.hide = True
        self.battle = True
        p1.destroy = False
        p1.hide = False
        platform_group.add(p1)
        button.imgdisp = 1
        pygame.time.set_timer(self.enemy_generation, 2000)
        mmanager.playsoundtrack(soundtrack[1], -1, 0.05)

    def world2(self):
        self.root.destroy()
        background.bgimage = pygame.image.load("png/desert.jpg")
        ground.image = pygame.image.load("png/desert_ground.png")
        pygame.time.set_timer(self.enemy_generation2, 2500)
        self.world = 2
        button.imgdisp = 1
        p1.destroy = False
        p1.hide = False
        platform_group.add(p1)
        castle.hide = True
        self.battle = True
        mmanager.playsoundtrack(soundtrack[1], -1, 0.05)

    def world3(self):
        self.battle = True
        button.imgdisp = 1
        # Empty for now


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("png/cursor.png")
        self.rect = self.image.get_rect()
        self.wait = 0

    def pause(self):
        if self.wait == 1:  # resume game
            self.wait = 0  # pause game
        else:
            self.wait = 1

    def hover(self):  # responsible for the change in the cursor when hovering over the button
        if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
            """
            set the current cursor’s visibility to “off” (Line 3). We’ll then replace it with our own cursor
            """
            pygame.mouse.set_visible(False)
            cursor.rect.center = pygame.mouse.get_pos()  # update position
            displaysurface.blit(cursor.image, cursor.rect)
        else:
            pygame.mouse.set_visible(True)


background = Background()
ground = Ground()
player = Player()
castle = Castle()
handler = EventHandler()
stage_display = StageDisplay()
health = HealthBar()
status_bar = StatusBar()
cursor = Cursor()
button = PButton()
p1 = Platform()
# Sprite groups are used to manage and update multiple sprites simultaneously.
# the collision detection functions that detect collisions requires a Sprite group as a parameter
ground_group = pygame.sprite.Group()
ground_group.add(ground)
platform_group = pygame.sprite.Group()
platform_group.add(p1)

playergroup = pygame.sprite.Group()
playergroup.add(player)
enemies = pygame.sprite.Group()
enemies2 = pygame.sprite.Group()
items = pygame.sprite.Group()
fireballs = pygame.sprite.Group()
bolts = pygame.sprite.Group()
font = pygame.font.get_fonts()




while True:
    player.gravity_check()
    mouse = pygame.mouse.get_pos()  # stores a list of two values, the first being the x-coordinate, and the second being the y-coordinate
    player.update()

    if player.attacking == True:
        player.attack()
    player.move()
    """
    render functions
    Always render the background first, then the ground and then all the players and enemies on top of the ground.
    """
    background.render()
    ground.render()
    button.render(button.imgdisp)
    cursor.hover()
    castle.update()
    p1.render()
    pygame.draw.rect(displaysurface, (255, 0, 255), player.rect, 2)
    """
    render the player after the castle. 
    Otherwise if you move the Player over to castle, the castle will render itself over the Player, hiding it.
    """
    if player.health > 0:
        displaysurface.blit(player.image, player.rect)
    health.render()  # rect stores a pair coordinates
    if stage_display.display == True:
        stage_display.move_display()
    if stage_display.clear == True:
        stage_display.stage_clear()
    """
    the status bar must render first, and then the text will render on top of it. 
    Doing it the other way around would hide the text completely.
    """
    displaysurface.blit(status_bar.surf, (630, 5))
    status_bar.update_draw()
    handler.update()
    if player.fmj: # player bought the fmj power up
        displaysurface.blit(pygame.image.load("png/fmj.png"), (360, 10))
    for entity in enemies:  # spawns enemies of world 1
        entity.update()
        entity.move()
        entity.render()
        if event.type == entity.fmj_cooldown: # if we do not set a cooldown the enemy will die instantly w/ fmj
            entity.cooldown = False
            pygame.time.set_timer(enemy.fmj_cooldown, 0)
    for entity2 in enemies2:  # spawns enemies of world 2
        entity2.update()
        entity2.move()
        entity2.render()
    for itm in items:
        itm.render()
        itm.update()

    for fb in fireballs:
        fb.fire()
        pygame.draw.rect(displaysurface, (255, 0, 0), fb.rect, 2) # fireball hitbox


    for b in bolts:
        b.fire()

    for event in pygame.event.get():
        # Will run when the close window button is clicked
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

            # For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
                if button.imgdisp == 1: # if it shows the pause button
                    cursor.pause()
                elif button.imgdisp == 0: # if it shows the home button
                    handler.home()
        if event.type == handler.enemy_generation: # first world
            """
            will keep generating enemies every time the timer for enemy generation is triggered. 
            However, it will not generate more enemies than what our handler’s stage_enemies variable has defined as the max limit for that stage
            """
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                enemy = Enemy()  # create new enemy
                enemies.add(enemy)
                handler.enemy_count += 1
        if event.type == handler.enemy_generation2: # second world

            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                print("EVENTO WORLD 2")
                enemy2 = Enemy2()  # create new enemy
                enemies2.add(enemy2)
                handler.enemy_count += 1

        """
        It’s important to call the timer again with a time duration of 0.
         This automatically disables it. Otherwise it could keep calling itself every second wasting resources.
        """
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)

        # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN and cursor.wait == 0:
            if event.key == pygame.K_f and player.money >= 5 and player.fmj == False: # fmj fireball upgrade (press F)
                player.money -= 5
                player.fmj = True

            if event.key == pygame.K_e and 450 < player.rect.x < 550:
                  # the player must press E and must be standing near the entrance of the castle
                handler.stage_handler()  # shows dungeons
            if event.key == pygame.K_n:
                if handler.world == 1:
                    if handler.battle == True and len(enemies) == 0:  # the player must be in world 2 and there must be 0 enemies
                        handler.next_stage()  # advance to the next stage
                        stage_display = StageDisplay()
                        stage_display.display = True
                        # Render stage display
                elif handler.world == 2:
                    if handler.battle == True and len(enemies2) == 0:  # the player must be in world 2 and there must be 0 enemies
                        handler.next_stage()  # advance to the next stage
                        stage_display = StageDisplay()
                        stage_display.display = True
                        # Render stage display

            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_m and player.magic_cooldown == True: # use m key to fire (no cooldown is more fun :) )
                if player.mana >= 6: # it costs 6 mana to fire

                    player.mana -= 6
                    player.attacking = True
                    fireball = Fireball()
                    fireballs.add(fireball)
                    ground_group.add(fireball)
                    mmanager.playsound(fireball_sound, 0.3)
            if event.key == pygame.K_RETURN:
                if player.attacking == False:
                    player.attack()
                    player.attacking = True
                player.update()


    FPS_CLOCK.tick(FPS)  # limits fps to 60

    """
    # Changes in the game are not implemented until the pygame.display.update() function has been called. 
    This function is responsible for updating your game window with any changes that have been made within that specific iteration of the game loop.
    """
    pygame.display.update()
