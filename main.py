import pygame
from pygame.locals import *
import sys
from background import Background
from ground import Ground
from enemy import Enemy
pygame.init()  # Begin pygame

# Declaring variables to be used through the program
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 730
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

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




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("png/Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "RIGHT"
        self.jumping = False
        self.running = False
        self.move_frame = 0
        self.attacking = False
        self.attack_frame = 0

    def move(self):
        # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
        self.acc = vec(0, 0.5)
        # Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False
        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        # Accelerates the player in the direction of the key press
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values
        # This causes character warping from one point of the screen to the other
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos  # Update rect with new pos

    def update(self):
        if self.move_frame > 6:
            self.move_frame = 0
            return
        if self.jumping == False and self.running == True:
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
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False


background = Background()
ground = Ground()
player = Player()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

while True:
    player.gravity_check()
    player.update()
    player.move()
    if player.attacking == True:
        player.attack()
    displaysurface.blit(player.image, player.rect)
    for event in pygame.event.get():
        # Will run when the close window button is clicked
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

            # For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_RETURN:
                if player.attacking == False:
                    player.attack()
                    player.attacking = True
    background.render()
    ground.render()
    displaysurface.blit(player.image, player.rect)
    pygame.display.update()
    FPS_CLOCK.tick(FPS)