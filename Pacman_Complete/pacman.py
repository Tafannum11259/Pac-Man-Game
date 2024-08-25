import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node )
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.direction = STOP
#DFS Algorithm:
    def update(self, dt):  # This function updates the object's behavior over time.
        self.sprites.update(dt) # Update the visuals of the object (like animations) as time passes
        # Update the object's position based on its direction, speed, and time increment (dt)
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()  #Determine the next valid direction for movement.
        if self.overshotTarget():  # Check if the object has gone too far past its destination.
            self.node = self.target  # If it went too far, make its current location the new destination.
            if self.node.neighbors[PORTAL] is not None: # Check if there is a portal neighbor in the current node.
                # If there's a portal, move the object to the neighbor node through the portal.
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction) # Calculate a new target node based on the direction.
            if self.target is not self.node:  # If the new target is different from the current node, update the direction.
                self.direction = direction
                # If the new target is the same as the current node, choose a different direction.
            else:
                self.target = self.getNewTarget(self.direction)
            if self.target is self.node: # If the target node is still the same as the current node, stop moving.
                self.direction = STOP
            self.setPosition()  # Update the object's position.
        # If the object hasn't overshot its target, check if the new direction is opposite to the current direction.
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection() # If it does, reverse its current direction.

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP  
 #BFS Algorithm:
    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
