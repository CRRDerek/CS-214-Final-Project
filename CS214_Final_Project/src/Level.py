'''
Created on Mar 15, 2015

@author: Derek Dik
'''

import pygame

from src.Globals import WINDOW_HEIGHT
from src.StaticObject import StaticObject
from src.PushBlock import PushBlock
from src.PreyAnimal import PreyAnimal
from src.SimplePredator import SimplePredator
from src.PlantTrap import PlantTrap
from src.WaterResource import WaterResource
from src.FoodResource import FoodResource
from src.GameTimer import get_time
from src.EndTrigger import EndTrigger


class Level(object):
    '''
    Class to model a single room
    '''
    
    _static_objects = []
    _dynamic_objects = []
    _width = 0
    _height = 0
    TILE_SIZE = WINDOW_HEIGHT / 25
    _description = ""
    # Timer to start when the _player dies
    _death_rattle = -120
    
    def __init__(self, fileName, x, y):
        '''
        Constructor
        '''
        height = 0
        width = 0
        self._x = x
        self._y = y
        self._static_objects = []
        self._dynamic_objects = []
        
        # Open the room file
        file = open(fileName + "\\room.dat", "r")
        
        # Load in the background image
        self._background = pygame.image.load(fileName + "\\background.png")
        
        # Load in the foreground image
        self._foreground = pygame.image.load(fileName + "\\foreground.png")
        self._foreground = self._foreground.convert_alpha()
        
        # Initialize a new list to store room data
        tiles = []
        
        # For each line in the room file
        for line in file:
            # Add 1 to the height of the room
            height += 1
            width = 0
            words = line.split()
            tileRow = []
            for tile in words:
                width += 1
                tileRow.append(tile)
            tiles.append(tileRow)
        
        file.close()
        
        for row in range(0, height):
            for column in range(0, width):
                val = tiles[row][column]
                if val == "1" or val == "x":
                    newTile = StaticObject(self.TILE_SIZE * column, self.TILE_SIZE * row)
                    self._static_objects.append(newTile)
                elif val == "2":
                    newResource  = WaterResource(self.TILE_SIZE * column, self.TILE_SIZE * row) 
                    self._static_objects.append(newResource)
                elif val == "3":
                    newResource  = FoodResource(self.TILE_SIZE * column, self.TILE_SIZE * row) 
                    self._static_objects.append(newResource)
                elif val == "4":
                    new_push_block  = PushBlock(self.TILE_SIZE * column, self.TILE_SIZE * row) 
                    self._dynamic_objects.append(new_push_block)
                elif val is "5":
                    new_prey_animal = PreyAnimal(self.TILE_SIZE * column, self.TILE_SIZE * row)
                    self._dynamic_objects.append(new_prey_animal)
                elif val is "6":
                    new_predator = SimplePredator(self.TILE_SIZE * column, self.TILE_SIZE * row)
                    self._dynamic_objects.append(new_predator)
                elif val is "7":
                    new_plant = PlantTrap(self.TILE_SIZE * column, self.TILE_SIZE * row)
                    self._static_objects.append(new_plant)  
                elif val is "v":
                    victory_trigger = EndTrigger(self.TILE_SIZE * column, self.TILE_SIZE * row)
                    self._static_objects.append(victory_trigger)
        self._height = height * self.TILE_SIZE
        self._width = width * self.TILE_SIZE
                
        
    def draw(self, gameDisplay, draw):

        gameDisplay.blit(self._background, (0, 0))
        
        for staticObject in self._static_objects:
            staticObject.draw(gameDisplay, draw)
        for dynamicObject in self._dynamic_objects:
            dynamicObject.draw(gameDisplay, draw)
        
        gameDisplay.blit(self._foreground, (0, 0))
                    
    def step(self):   
            
        #Test collisions
        for dynamicObject in self._dynamic_objects:
            for staticObject in self._static_objects:
                dynamicObject.testCollision(staticObject)
            for otherObject in self._dynamic_objects:
                dynamicObject.testCollision(otherObject)      

        #Step
        for dynamicObject in self._dynamic_objects:
            dynamicObject.step()
            if dynamicObject._type == "NPC":
                dynamicObject.perceive(self._static_objects, self._dynamic_objects)
            if dynamicObject.destroy:
                self._dynamic_objects.remove(dynamicObject)
                if dynamicObject._type == "Player":
                    self._death_rattle = get_time()

    def is_game_over(self):
        ''' 
        Function to check each step if the game has ended
        Returns True if the _player is dead
        '''
        return get_time() - self._death_rattle == 60
    
    def is_game_won(self):
        ''' 
        Function to check each step if the _player has found the embryos
        Returns True if the _player has beaten the game
        '''
        return self._player.has_won()

    def checkForTransition(self):
        transitioningObjects = []
        for dynamicObject in self._dynamic_objects:
            transitioningObject = [dynamicObject]
            if dynamicObject.getX() > self._width:
                transitioningObject.append("Right")
                transitioningObjects.append(transitioningObject)
                self._dynamic_objects.remove(dynamicObject)                
            elif dynamicObject.getX() < 0:
                transitioningObject.append("Left")
                transitioningObjects.append(transitioningObject)
                self._dynamic_objects.remove(dynamicObject)
            elif dynamicObject.getY() < 0:
                transitioningObject.append("Up")
                self._dynamic_objects.remove(dynamicObject)
                transitioningObjects.append(transitioningObject)
            elif dynamicObject.getY() > self._height:
                transitioningObject.append("Down")
                transitioningObjects.append(transitioningObject)
                self._dynamic_objects.remove(dynamicObject)
            else:
                transitioningObject.append(0)
                transitioningObject.append("None")
        return transitioningObjects
    def checkForPlayerTransition(self):
        if self._player.getX() > self._width:
            return "Right"
        elif self._player.getX() < 0:
            return "Left"
        elif self._player.getY() < 0:
            return "Up"
        elif self._player.getY() > self._height:
            return "Down"
        else:
            return "None"
        
    def addDynamicObject(self, dynamicObject):
        '''
        Function to add a new dynamic object from a different level to this level
        '''
        # Inform the object of the change
        dynamicObject.changeLocation([self._x, self._y])
        
        # Add the object to my list of dynamic objects
        self._dynamic_objects.append(dynamicObject)
        #Adjust the position accordingly
        if dynamicObject.getX() > self._width:
            dynamicObject.setX(0)
        elif dynamicObject.getX() < 0:
            dynamicObject.setX(self._width - self.TILE_SIZE)
        elif dynamicObject.getY() < 0:
            dynamicObject.setY(self._height - self.TILE_SIZE)
        elif dynamicObject.getY() > self._height:
            dynamicObject.setY(0)
           
    def resetPlayer(self, player):
        ''' Adds the _player to the level after a transition '''
        self._player = player
        self.addDynamicObject(player)
        
    ''' Keyboard handling functions '''
    def keyboardUp(self):
        self._player.setDY(-4)
        
    def keyboardReleaseUp(self):
        self._player.setDY(0)

    def keyboardDown(self):
        self._player.setDY(4)
        
    def keyboardReleaseDown(self):
        self._player.setDY(0)

    def keyboardLeft(self):
        self._player.setDX(-4)
        
    def keyboardReleaseLeft(self):
        self._player.setDX(0)
        
    def keyboardRight(self):
        self._player.setDX(4)
        
    def keyboardReleaseRight(self):
        self._player.setDX(0)
        