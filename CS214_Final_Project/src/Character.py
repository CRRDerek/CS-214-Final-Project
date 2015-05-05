'''
Created on Apr 14, 2015

@author: 1upde_000
'''
from src.DynamicObject import DynamicObject
from src.StaticObject import StaticObject
from test.test_pyexpat import PositionTest
from src.Experience import Experience


class Character(DynamicObject):
    '''
    classdocs
    '''

    water = 3000
    food = 6000
    loneliness = 0
    myExperience = Experience()    
    damage_cooldown = 0
    myType = "NPC"
    mySightRadius = 200

    def __init__(self, params):
        '''
        Constructor
        '''


    def step(self):
        self.damage_cooldown += 1
        self.water -= 1
        self.food -= 1
        self.loneliness += 1
        if self.water < 0:
            self.destroy = True
        
        if self.myDX > 0 and self.myCollisions[0] == 0 or self.myDX < 0 and self.myCollisions[1] == 0 or self.myDX == 0:
            self.myLastX = self.myX
            self.myX += self.myDX
        #else:
            #self.myX = self.myLastX
        if self.myDY > 0 and self.myCollisions[3] == 0 or self.myDY < 0 and self.myCollisions[2] == 0 or self.myDY == 0:
            self.myLastY = self.myY
            self.myY += self.myDY
        #else:
            #self.myY = self.myLastY
        self.rightCollision = 0
        self.leftCollision = 0
        self.topCollision = 0
        self.bottomCollision = 0
        self.myCollisions = [self.rightCollision, self.leftCollision, self.topCollision, self.bottomCollision]
        
    def collide(self, otherObject, collisionAngle):
        if otherObject is not self:
            if otherObject.myType == "water_resource":
                self.water += otherObject.get_water()
            elif otherObject.myType == "predator" and self.damage_cooldown > 30:
                self.water -= 300
                self.damage_cooldown = 0
                otherObject.set_visible()
                    
            if collisionAngle == "Right" and self.myDX > 0:
                self.rightCollision = 1
                if otherObject.type() is "pushable":
                    otherObject.myDX = 2
                #self.myDX = 0
                #self.myX = otherObject.getX() - self.myW
                
            if collisionAngle == "Left" and self.myDX < 0:
                self.leftCollision = 1
                if otherObject.type() is "pushable":
                    otherObject.myDX = -2
                #self.myDX = 0
                #self.myX = otherObject.getX() + otherObject.getW()
            if collisionAngle == "Top" and self.myDY < 0:
                self.topCollision = 1
                if otherObject.type() is "pushable":
                    otherObject.myDY = -2
                #self.myDY = 0
                #self.myY = otherObject.getY() + otherObject.getH()
            if collisionAngle == "Bottom" and self.myDY > 0:
                self.bottomCollision = 1
                if otherObject.type() is "pushable":
                    otherObject.myDY = 2
                #self.myDY = 0
                #self.myY = otherObject.getY() - self.myH
            self.myCollisions = [self.rightCollision, self.leftCollision, self.topCollision, self.bottomCollision]
        
    def perceive(self, staticObjects, dynamicObjects, x, y):
        '''
        Stub
        '''

    def changeLocation(self, location):
        self.myExperience.changeLocation(location)        
        
    
    