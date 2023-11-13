import pygame
import main

HEIGHT = 350
WIDTH = 730
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
class StatusBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.smallerfont = pygame.font.SysFont('notosansmono', 16)
        self.surf = pygame.Surface((220, 80)) #  This surface is essentially a blank rectangle, 90 is the width
        self.rect = self.surf.get_rect() # The rectangle represents the position and size of the status bar


    def update_draw(self):
        # Create the text to be displayed
        text_name = self.smallerfont.render("PLAYER: " + str(main.name_input.get_value()), True, (255, 0, 0))
        text1 = self.smallerfont.render("STAGE: " + str(main.handler.stage), True, (255, 0, 0))
        text2 = self.smallerfont.render("EXP: " + str(main.player.xp), True, (255,0,0))
        text3 = self.smallerfont.render("MANA: " + str(main.player.mana), True, (255,0,0))
        text4 = self.smallerfont.render("FPS: " + str(int(main.FPS_CLOCK.get_fps())), True, (255,0,0))
        text5 = self.smallerfont.render("MNY: " + str(int(main.player.money)), True, (255, 0, 0))

        # Draw the text to the status bar
        displaysurface.blit(text_name, (610, 0))
        displaysurface.blit(text1, (610, 13))
        displaysurface.blit(text2, (610, 27))
        displaysurface.blit(text3, (610, 40))
        displaysurface.blit(text4, (610, 53))
        displaysurface.blit(text5, (610, 66))