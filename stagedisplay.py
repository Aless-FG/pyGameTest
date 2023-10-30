import pygame

import main

class StageDisplay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.headingfont = pygame.font.SysFont('notosansmono', 30)
        self.stageclearfont = pygame.font.SysFont('notosansmono', 30)
        self.posx = -100 # -100” position on the x-axis. This keeps it safely out of the window
        self.posy = 100
        self.display = False
        self.clear = False

    def move_display(self): # is incharge of “moving” the display across the screen
        # Create the text to be displayed
        self.text = self.headingfont.render("STAGE: " + str(main.handler.stage), True, (0,0,0))
        if self.posx < 700:
            self.posx += 5
            main.displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.display = False
            self.posx = -100 # gtfo text
            self.posy = 100

    def stage_clear(self):
        self.text = self.stageclearfont.render("STAGE CLEAR!", True, (0,0,0))
        main.button.imgdisp = 0 # shows the home button
        if self.posx < 720:
            self.posx += 5
            main.displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.clear = False
            self.posx = -100
            self.posy = 100