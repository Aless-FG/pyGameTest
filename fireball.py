import pygame
import main


class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = main.player.direction  # get player position
        self.pos = main.vec(main.player.pos.x, main.player.pos.y - 20)
        self.vel = main.vec(0, 2)

        if self.direction == "RIGHT":
            self.image = pygame.image.load("png/fireball.png")
        else:
            self.image = pygame.image.load("png/fireball.png")
        """
        setting the center of the new rectangle to the same position as the player.pos
        the center of the fireball's rectangle is positioned at the same location as the player's position.
        """
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.y = main.player.pos.y - 40


    def fire(self):

        main.player.magic_cooldown = 1  # the player cannot fire another firebatt till the previous one exits screen
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
                self.pos.x += 5
                self.gravity_check()
            else:

                self.pos.x -= 5
                print("siu2")
                self.gravity_check()

            self.rect.center = self.pos

        else:
            self.kill()
            main.player.magic_cooldown = 1
            main.player.attacking = False

    def gravity_check(self):

        # Detect collisions with the ground objects
        hits = pygame.sprite.spritecollide(main.fireball, main.ground_group, False)
        pl_hits = pygame.sprite.spritecollide(main.fireball, main.platform_group, False)

        if self.vel.y > 0:
            if len(hits) == 2:
                lowest = hits[0]
                if self.pos.y < lowest.rect.top:
                    print(lowest.rect.top)
                    self.pos.y = lowest.rect.top - 20  # Align the fireball with the top of the ground object
                    self.vel.y = 0  # Stop the fireball from moving vertically
            elif pl_hits:
                lowest = pl_hits[0]
                self.pos.y = lowest.rect.top   # Align the fireball with the top of the ground object
                self.vel.y = 0  # Stop the fireball from moving vertically
            self.vel.y += 0.7

        # Update the position based on the new velocity
        self.pos += self.vel
        self.rect.center = self.pos
