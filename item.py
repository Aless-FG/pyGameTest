import pygame
import main

class Item(pygame.sprite.Sprite):
    def __init__(self, itemtype): # the item can be a heart or a money drop
        super().__init__()
        if itemtype == 1:
            self.image = pygame.image.load("png/heartdrop.png")
        elif itemtype == 2:
            self.image = pygame.image.load("png/coin.png")
        self.rect = self.image.get_rect()
        self.type = itemtype
        self.posx = 0
        self.posy = 0

    def render(self):
        self.rect.x = self.posx
        self.rect.y = self.posy
        main.displaysurface.blit(self.image, self.rect)

    def update(self):
        hits = pygame.sprite.spritecollide(self, main.playergroup, False)
        # Code to be activated if item comes in contact with player
        if hits:
            if main.player.health < 5 and self.type == 1: # if the player has less than 5 hearts and the drop is a heart
                main.player.health += 1
                main.health.image = main.health_ani[main.player.health] # update healthbar
                self.kill() # destroy the sprite
            if self.type == 2:
                main.player.money += main.enemy.money
                self.kill()