import pygame
from pygame.locals import *
import sys
from background import Background
from castle import Castle
from ground import Ground
from enemy import Enemy
from tkinter import Tk, Button

from healthbar import HealthBar

pygame.init()  # Begin pygame

# Declaring variables to be used through the program
vec = pygame.math.Vector2 # used to record X and Y position of the player
HEIGHT = 350
WIDTH = 730
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
hit_cooldown = pygame.USEREVENT + 1 # need to create a new custom event
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT)) # displays the game using width and height
pygame.display.set_caption("Game") # changes window's title

run_ani_R = [pygame.image.load("png/Player_Sprite_R.png"), pygame.image.load("png/Player_Sprite2_R.png"),
             pygame.image.load("png/Player_Sprite3_R.png"), pygame.image.load("png/Player_Sprite4_R.png"),
             pygame.image.load("png/Player_Sprite5_R.png"), pygame.image.load("png/Player_Sprite6_R.png"),
             pygame.image.load("png/Player_Sprite_R.png")]

# Run animation for the LEFT
run_ani_L = [pygame.image.load("png/Player_Sprite_L.png"), pygame.image.load("png/Player_Sprite2_L.png"),
             pygame.image.load("png/Player_Sprite3_L.png"), pygame.image.load("png/Player_Sprite4_L.png"),
             pygame.image.load("png/Player_Sprite5_L.png"), pygame.image.load("png/Player_Sprite6_L.png"),
             pygame.image.load("png/Player_Sprite_L.png")]

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("png/Player_Sprite_R.png"), pygame.image.load("png/Player_Attack_R.png"),
                pygame.image.load("png/Player_Attack2_R.png"), pygame.image.load("png/Player_Attack2_R.png"),
                pygame.image.load("png/Player_Attack3_R.png"), pygame.image.load("png/Player_Attack3_R.png"),
                pygame.image.load("png/Player_Attack4_R.png"), pygame.image.load("png/Player_Attack4_R.png"),
                pygame.image.load("png/Player_Attack5_R.png"), pygame.image.load("png/Player_Attack5_R.png"),
                pygame.image.load("png/Player_Sprite_R.png")]

# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("png/Player_Sprite_L.png"), pygame.image.load("png/Player_Attack_L.png"),
                pygame.image.load("png/Player_Attack2_L.png"), pygame.image.load("png/Player_Attack2_L.png"),
                pygame.image.load("png/Player_Attack3_L.png"), pygame.image.load("png/Player_Attack3_L.png"),
                pygame.image.load("png/Player_Attack4_L.png"), pygame.image.load("png/Player_Attack4_L.png"),
                pygame.image.load("png/Player_Attack5_L.png"), pygame.image.load("png/Player_Attack5_L.png"),
                pygame.image.load("png/Player_Sprite_L.png")]

health_ani = [pygame.image.load("png/heart0.png"), pygame.image.load("png/heart.png"),
              pygame.image.load("png/heart2.png"), pygame.image.load("png/heart3.png"),
              pygame.image.load("png/heart4.png"), pygame.image.load("png/heart5.png")]




class Player(pygame.sprite.Sprite): # inherits from the pygame.sprite.Sprite class
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("png/Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240)) # position of the player
        self.vel = vec(0, 0) # velocity of the player
        self.acc = vec(0, 0) # acceleration of the player
        self.direction = "RIGHT" # used to store the current direction of the Player
        self.jumping = False
        self.running = False
        self.move_frame = 0 # track the current frame of the character being displayed
        self.attacking = False
        self.attack_frame = 0
        self.cooldown = False
        self.health = 5

    def move(self):

        self.acc = vec(0, 0.5) # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
        # Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3: #use abs() to return the magnitude since the velocity can be in the negative direction (the left direction)
            self.running = True
        else:
            self.running = False

        pressed_keys = pygame.key.get_pressed() # Returns the current key presses

        # Accelerates the player in the direction of the key press
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC # updates object's acceleration
        self.vel += self.acc # updates object's velocity
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

    def update(self): # This function is in charge of changing the movement frame of the Player if he's moving.
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
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False

            # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.correction()
            self.image = attack_ani_L[self.attack_frame]

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

        self.rect.x -= 1

        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
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
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        """
        check whether the player has any velocity in the downwards direction. 
        If he doesn’t, then all is good (because he isn’t falling and thus is on the ground). 
        If however he is falling we will proceed.
        """
        if self.vel.y > 0:
            if hits: # will run if the hits variable recorded a collision between the player and ground
                """
                selects the first ground object from the list of hits. 
                The assumption here is that the first ground object in the list is the one closest to the player's current position along the y-axis.
                """
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom: #checks if the player's y-coordinate (vertical position) is higher (less than) the bottom y-coordinate of the lowest ground object's bounding rectangle.
                    self.pos.y = lowest.rect.top + 1 # sets the player's y-coordinate to just above the top of the ground object, effectively preventing the player from falling through the ground.
                    self.vel.y = 0 # sets the player's vertical velocity to 0, effectively stopping any downward movement due to gravity.
                    self.jumping = False

class EventHandler():
    def __init__(self):

        self.stage = 1
        self.enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 2

        self.stage_enemies = [] # enemies generation
        for x in range(1, 21):
            self.stage_enemies.append(int((x ** 2 / 2) + 1)) # number of enemies to be generated per level

    def next_stage(self):  # Code for when the next stage is clicked
        self.stage += 1
        self.enemy_count = 0
        print("Stage: " + str(self.stage))
        # The higher the stage number, the lower the time gap between enemy spawns, meaning harder levels
        pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage)) # sets the timer for enemy generation

    def stage_handler(self): # starting menu
        # Code for the Tkinter stage selection window
        print("stage handler function")
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
        print("world1")
        self.root.destroy()
        castle.hide = True
        self.battle = True
        pygame.time.set_timer(self.enemy_generation, 2000)


    def world2(self):
        self.battle = True
        # Empty for now

    def world3(self):
        self.battle = True
        # Empty for now

class StageDisplay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.headingfont = pygame.font.SysFont('notosansmono', 30)
        self.text = self.headingfont.render("STAGE: " + str(handler.stage), True, (0,0,0))
        self.rect = self.text.get_rect()
        self.posx = -100 # -100” position on the x-axis. This keeps it safely out of the window
        self.posy = 100
        self.display = False

    def move_display(self): # is incharge of “moving” the display across the screen
        # Create the text to be displayed
        self.text = self.headingfont.render("STAGE: " + str(handler.stage), True, (0,0,0))
        if self.posx < 700:
            self.posx += 5
            displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.display = False
            self.kill()

background = Background()
ground = Ground()
player = Player()
castle = Castle()
handler = EventHandler()
stage_display = StageDisplay()
health = HealthBar()
# enemy = Enemy()
# Sprite groups are used to manage and update multiple sprites simultaneously.
# the collision detection functions that detect collisions requires a Sprite group as a parameter
ground_group = pygame.sprite.Group()
ground_group.add(ground)
playergroup = pygame.sprite.Group()
playergroup.add(player)
enemies = pygame.sprite.Group()

font = pygame.font.get_fonts()
while True:
    player.gravity_check()
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

    castle.update()

    """
    render the player after the castle. 
    Otherwise if you move the Player over to castle, the castle will render itself over the Player, hiding it.
    """
    if player.health > 0:
        displaysurface.blit(player.image, player.rect)
    health.render() # rect stores a pair coordinates
    if stage_display.display == True:
        stage_display.move_display()
    for entity in enemies: # spawns enemies
        entity.update()
        entity.move()
        entity.render()
    for event in pygame.event.get():
        # Will run when the close window button is clicked
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

            # For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == handler.enemy_generation:
            """
            will keep generating enemies every time the timer for enemy generation is triggered. 
            However, it will not generate more enemies than what our handler’s stage_enemies variable has defined as the max limit for that stage
            """
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                enemy = Enemy() # create new enemy
                enemies.add(enemy)
                handler.enemy_count += 1

        """
        It’s important to call the timer again with a time duration of 0.
         This automatically disables it. Otherwise it could keep calling itself every second wasting resources.
        """
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)
        # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and 450 < player.rect.x < 550:
                print("stage handler IF") # the player must press E and must be standing near the entrance of the castle
                handler.stage_handler() # shows dungeons
            if event.key == pygame.K_n:
                if handler.battle == True and len(enemies) == 0: # the player must be in dungeon and there must be 0 enemies
                    handler.next_stage() # advance to the next stage
                    stage_display = StageDisplay()
                    stage_display.display = True
                    # Render stage display



            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_RETURN:
                if player.attacking == False:
                    player.attack()
                    player.attacking = True
                player.update()

    FPS_CLOCK.tick(FPS) # limits fps to 60

    """
    # Changes in the game are not implemented until the pygame.display.update() function has been called. 
    This function is responsible for updating your game window with any changes that have been made within that specific iteration of the game loop.
    """
    pygame.display.update()