import pygame
import pygame_menu
from pygame.locals import *
import sys

from pygame_menu import themes

from background import Background
from castle import Castle
from ground import Ground
from enemy import Enemy
from tkinter import Tk, Button
from healthbar import HealthBar
from fireball import Fireball
from iceball import Iceball
from pform import Platform
from player import Player
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

menu = pygame_menu.Menu('Welcome to...', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_GREEN)
about_menu = pygame_menu.Menu('About', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_GREEN)
name_input = menu.add.text_input("Name: ", default='USR', maxchar=3)
print(name_input.get_value())
menu.add.button('Play', menu.disable)
menu.add.button('About', about_menu.enable())
about_menu.add.label('test')
about_menu.add.label('test2')
about_menu.add.button('Return to main menu', pygame_menu.events.BACK)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(displaysurface)

run_ani_R = [pygame.image.load("png/Player_Sprite_R.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite2_R.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite3_R.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite4_R.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite5_R.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite6_R.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite_R.png").convert_alpha()]

# Run animation for the LEFT
run_ani_L = [pygame.image.load("png/Player_Sprite_L.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite2_L.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite3_L.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite4_L.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite5_L.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite6_L.png").convert_alpha(),
             pygame.image.load("png/Player_Sprite_L.png").convert_alpha()]

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("png/Player_Sprite_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack2_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack2_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack3_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack3_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack4_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack4_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack5_R.png").convert_alpha(),
                pygame.image.load("png/Player_Attack5_R.png").convert_alpha(),
                pygame.image.load("png/Player_Sprite_R.png").convert_alpha()]

# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("png/Player_Sprite_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack2_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack2_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack3_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack3_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack4_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack4_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack5_L.png").convert_alpha(),
                pygame.image.load("png/Player_Attack5_L.png").convert_alpha(),
                pygame.image.load("png/Player_Sprite_L.png").convert_alpha()]

# Music and Sound
soundtrack = ["tracks/background_village.wav", "tracks/battle_music.wav", "tracks/gameover.wav"]
swordtrack = [pygame.mixer.Sound("tracks/sword1.wav"), pygame.mixer.Sound("tracks/sword2.wav"),
              pygame.mixer.Sound("tracks/sword3.wav"), pygame.mixer.Sound("tracks/sword4.wav")]
fireball_sound = pygame.mixer.Sound("tracks/fireball_sound.wav")
enemy_hit = pygame.mixer.Sound("tracks/enemy_hit.wav")

mmanager = MusicManager()
mmanager.playsoundtrack(soundtrack[0], -1, 0.05)  # The second parameter states that it should repeat infinitely


class EventHandler():
    def __init__(self):

        self.stage = 1
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 2  # generates enemies in world 1
        self.enemy_generation2 = pygame.USEREVENT + 3  # generates enemies in world 2
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
            pygame.time.set_timer(self.enemy_generation,
                                  1500 - (50 * self.stage))  # sets the timer for enemy generation
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
        pygame.time.set_timer(self.enemy_generation, 0)  # disables enemies generation (world 1)
        pygame.time.set_timer(self.enemy_generation2, 0)  # disables enemies generation (world 2)
        self.battle = False
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 1
        self.world = 0

        # Destroy any enemies or items lying around
        for group in enemies:  # , items
            for entity in group:
                entity.kill()

        # Bring back normal backgrounds
        castle.hide = False
        background.bgimage = pygame.image.load("png/bg_anim/background_sprite2.png")
        ground.image = pygame.image.load("png/ground_sprite.png")
        button.render(button.imgdisp)  # renders home or pause button
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
iceballs = pygame.sprite.Group()
bolts = pygame.sprite.Group()
font = pygame.font.get_fonts()


print(background.background_files)
while True:
    player.gravity_check()
    mouse = pygame.mouse.get_pos()  # stores a list of two values, the first being the x-coordinate, and the second being the y-coordinate
    player.update()
    background.update()
    p1.update()
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
    health.render()
    if stage_display.display == True:
        stage_display.move_display()
    if stage_display.clear == True:
        stage_display.stage_clear()
    """
    the status bar must render first, and then the text will render on top of it. 
    Doing it the other way around would hide the text completely.
    """
    displaysurface.blit(status_bar.surf, (610, 5))
    status_bar.update_draw()
    handler.update()
    if player.fmj:  # player bought the fmj power up
        displaysurface.blit(pygame.image.load("png/fmj_sprite.png"), (20, 45))
    if player.double_jump_display:
        displaysurface.blit(pygame.image.load("png/idk_sprite.png"), (55, 45))
    for entity in enemies:  # spawns enemies of world 1
        entity.update()
        entity.move()
        entity.render()
        if event.type == entity.fmj_cooldown:  # if we do not set a cooldown the enemy will die instantly w/ fmj
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
        pygame.draw.rect(displaysurface, (255, 0, 0), fb.rect, 2)  # fireball hitbox

    for ib in iceballs:
        ib.fire()
        pygame.draw.rect(displaysurface, (255, 0, 0), ib.rect, 2)  # iceball hitbox

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
                if button.imgdisp == 1:  # if it shows the pause button
                    cursor.pause()
                elif button.imgdisp == 0:  # if it shows the home button
                    handler.home()
        if event.type == handler.enemy_generation:  # first world
            """
            will keep generating enemies every time the timer for enemy generation is triggered. 
            However, it will not generate more enemies than what our handler’s stage_enemies variable has defined as the max limit for that stage
            """
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                enemy = Enemy()  # create new enemy
                enemies.add(enemy)
                handler.enemy_count += 1
        if event.type == handler.enemy_generation2:  # second world

            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:

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
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_f and player.money >= 5 and player.fmj == False:  # fmj upgrade (press F)
                player.money -= 5
                player.fmj = True

            if event.key == pygame.K_g and player.money >= 10 and player.double_jump_display == False:  # fmj upgrade (press F)
                player.money -= 10
                player.double_jump_display = True
                player.double_jump = True

            elif event.key == pygame.K_g and player.money >= 10 and player.double_jump_display == True:  # jumps upgrade upgrade (press F)
                player.money -= 10
                player.double_jump_display = False
                player.double_jump = False

            if event.key == pygame.K_e and 450 < player.rect.x < 550:
                # the player must press E and must be standing near the entrance of the castle
                handler.stage_handler()  # shows dungeons
            if event.key == pygame.K_n:
                if handler.world == 1:
                    if handler.battle == True and len(
                            enemies) == 0:  # the player must be in world 2 and there must be 0 enemies
                        handler.next_stage()  # advance to the next stage
                        stage_display = StageDisplay()
                        stage_display.display = True
                        # Render stage display
                elif handler.world == 2:
                    if handler.battle == True and len(
                            enemies2) == 0:  # the player must be in world 2 and there must be 0 enemies
                        handler.next_stage()  # advance to the next stage
                        stage_display = StageDisplay()
                        stage_display.display = True
                        # Render stage display

            if event.key == pygame.K_SPACE and player.double_jump == False:
                player.jump()
            if event.key == pygame.K_SPACE and player.double_jump == True and player.mana >= 5:
                player.double_jump_powerup()

            elif event.key == pygame.K_m and player.magic_cooldown == True:  # use m key to fire (fireball)
                if player.mana >= 6:  # it costs 6 mana to fire

                    player.mana -= 6
                    player.attacking = True
                    fireball = Fireball()
                    fireballs.add(fireball)
                    ground_group.add(fireball)
                    mmanager.playsound(fireball_sound, 0.3)

            if event.key == pygame.K_k and player.magic_cooldown == True:  # use k key to fire (iceball)
                if player.mana >= 3:  # it costs 6 mana to fire

                    player.mana -= 3
                    player.attacking = True
                    iceball = Iceball()
                    iceballs.add(iceball)
                    ground_group.add(iceball)

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
