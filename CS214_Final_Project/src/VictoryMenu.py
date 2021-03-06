'''
Created on May 9, 2015

@author: Derek Dik
'''

import pygame

from src.GuiButton import GuiButton

class VictoryMenu(object):
    '''
    Object to model a menu when the player completes the game
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._background = pygame.image.load("images\\UI\\Endcard.png")
        self._quit_button = GuiButton(450, 600, 200, 100, pygame.image.load("images\\UI\\QuitButton.png"))       
    
    def draw(self, gameDisplay, mouseX, mouseY):
        # Draw the background
        gameDisplay.blit(self._background, (0, 0))
        # Draw the quit button
        self._quit_button.draw(gameDisplay)
    
    def get_button(self, mouseX, mouseY):
        '''
        Function to check if the player has selected an option yet
        Returns 0 if no option has been selected
        Returns 1 if the user has clicked "quit"
        ''' 
        if self._quit_button.test(mouseX, mouseY):
            return 1
            print("quit button pressed")
        else:
            return 0
        