import pygame

import main

class Item(pygame.sprite.Sprite):
    def __init__(self, itemtype): # the item can be a heart or a money drop
        super().__init__()
        if itemtype == 1:
            self.image = pygame.image.load("png/heart_sprite.png")
        elif itemtype == 2:
            self.image = pygame.image.load("png/coin_sprite.png")
        self.rect = self.image.get_rect()
        self.type = itemtype
        self.posx = 0
        self.posy = 0
        self.vely = 0.02

    def render(self):
        self.rect.x = self.posx
        self.rect.y = self.posy
        main.displaysurface.blit(self.image, self.rect)

    def update(self):
        hits = pygame.sprite.spritecollide(self, main.playergroup, False)
        # Code to be activated if item comes in contact with player
        if hits:
            if main.player.health < main.player.max_health and self.type == 1: # if the player has less than 5 hearts and the drop is a heart
                main.player.health += 1
                if main.player.dmg >= 1:
                    main.player.dmg -= 1
                    main.health.hearts[main.player.health - 1] = main.health.image # refill heart
                self.kill() # destroy the sprite
            elif main.player.health == main.player.max_health and self.type == 1:
                main.player.health += 1
                main.player.max_health += 1
                main.health.hearts.append(main.health.image_heart_extended)
                self.kill()  # destroy the sprite
            if self.type == 2:
                main.player.money += main.enemy.money
                self.kill()

