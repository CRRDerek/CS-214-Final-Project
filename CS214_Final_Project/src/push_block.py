'''
Created on Apr 29, 2015

@author: 1upde_000
'''
from src import DynamicObject
from src.Globals import WINDOW_HEIGHT, WINDOW_WIDTH

class push_block(DynamicObject.DynamicObject):
    '''
    models a block which can be moved by the player or by an NPC
    '''
    
    myType = "pushable"
    def __init__(self, x, y):
        '''
        Constructor
        '''
        self.myX = x
        self.myY = y
        self.myH = WINDOW_HEIGHT / 25 - 4
        self.myW = WINDOW_WIDTH / 25 - 4
        self.myDX = 0
        self.myDY = 0
        
    def collideb(self, otherObject, collisionAngle):
        super()
        if self.topCollision > 0:
            self.myDY = 2
        if self.bottomCollision > 0:
            self.myDY = -2
        if self.leftCollision > 0:
            self.myDX = 2
        if self.rightCollision > 0:
            self.myDX = -2
            
    def stepb(self):
        super()
        if self.myDX > 0:
            self.myDX -= 0.01
        if self.myDX < 0:
            self.myDX += 0.-1
        if self.myDY > 0:
            self.myDX -= 0.01
        if self.myDY < 0:
            self.myDY += 0.01
        
    def draw(self, gameDisplay, draw):
        draw.rect(gameDisplay, 100, [self.myX, self.myY, self.myW, self.myH])   