import pygame
import main


class Iceball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = main.player.direction  # get player position
        self.pos = main.vec(main.player.pos.x, main.player.pos.y - 40)
        self.vel = main.vec(0, 2)

        if self.direction == "RIGHT":
            self.image = pygame.image.load("png/iceball_sprite_right.png").convert_alpha()
        else:
            self.image = pygame.image.load("png/iceball_sprite_left.png").convert_alpha()
        """
        setting the center of the new rectangle to the same position as the player.pos
        the center of the fireball's rectangle is positioned at the same location as the player's position.
        """
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.y = main.player.pos.y - 40



    def fire(self):
        main.player.magic_cooldown  = False

        # Runs while the fireball is still within the screen w/ extra margin
        """
        As long as the fireball is within the range of -10 and 710, keep drawing and moving the fireball forward
        """
        if -10 < self.rect.x < 710:

            if self.direction == "RIGHT":
                self.image = pygame.image.load("png/iceball_sprite_right.png").convert_alpha()
                main.displaysurface.blit(self.image, self.rect)
            else:
                self.image = pygame.image.load("png/iceball_sprite_left.png").convert_alpha()
                main.displaysurface.blit(self.image, self.rect)

            if self.direction == "RIGHT":
                self.pos.x += 2
                self.gravity_check()
            else:

                self.pos.x -= 2

                self.gravity_check()

            self.rect.center = self.pos

        else:
            self.kill()
            main.player.magic_cooldown = True
            main.player.attacking = False

    def gravity_check(self):

        # Detect collisions with the ground objects
        hits = pygame.sprite.spritecollide(main.iceball, main.ground_group, False)
        pl_hits = pygame.sprite.spritecollide(main.iceball, main.platform_group, False)

        if self.vel.y > 0:
            if len(hits) == 2:
                lowest = hits[0]
                if self.pos.y < lowest.rect.top:
                    self.pos.y = lowest.rect.top - 10   # Align the fireball with the top of the ground object
                    self.vel.y = 0  # Stop the fireball from moving vertically
            elif pl_hits:
                lowest = pl_hits[0]
                self.pos.y = lowest.rect.top - 10   # Align the fireball with the top of the ground object
                self.vel.y = 0  # Stop the fireball from moving vertically
            self.vel.y += 0.7

        # Update the position based on the new velocity
        self.pos += self.vel
        self.rect.center = self.pos
