import pygame
import main

class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = main.player.direction # get player position
        if self.direction == "RIGHT":
            self.image = pygame.image.load("png/fireball.png")
        else:
            self.image = pygame.image.load("png/fireball.png")
        """
        setting the center of the new rectangle to the same position as the player.pos
        the center of the fireball's rectangle is positioned at the same location as the player's position.
        """
        self.rect = self.image.get_rect(center=main.player.pos)
        self.rect.y = main.player.pos.y - 40
        if main.player.direction == "RIGHT":
            self.rect.x = main.player.pos.x
        else:
            self.rect.x = main.player.pos.x - 60


    def fire(self):
        main.player.magic_cooldown = 0 # the player cannot fire another firebatt till the previous one exits screen
        # Runs while the fireball is still within the screen w/ extra margin
        """
        As long as the fireball is within the range of -10 and 710, keep drawing and moving the fireball forward
        """
        if -10 < self.rect.x < 710:
            if self.direction == "RIGHT":
                self.image = pygame.image.load("png/fireball.png")
                main.displaysurface.blit(self.image, self.rect)
            else:
                self.image = pygame.image.load("png/fireball.png")
                main.displaysurface.blit(self.image, self.rect)

            if self.direction == "RIGHT":
                self.rect.move_ip(7, 0) # moves the fireball's rectangle 12 pixels to the right along the x-axis
            else:
                self.rect.move_ip(-7, 0)
        else:
            self.kill()
            main.player.magic_cooldown = 1
            main.player.attacking = False