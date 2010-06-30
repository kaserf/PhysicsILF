#!/usr/bin/python
"""
This file is part of the 'Physics' Project
Physics is a 2D Physics Playground for Kids (supporting Box2D2)
Physics Copyright (C) 2008, Alex Levenson, Brian Jordan
Elements Copyright (C) 2008, The Elements Team, <elements@linuxuser.at>

Wiki:   http://wiki.laptop.org/wiki/Physics
IRC:    #olpc-physics on irc.freenode.org

Code:   http://dev.laptop.org/git?p=activities/physics
        git clone git://dev.laptop.org/activities/physics

License:  GPLv3 http://gplv3.fsf.org/
"""

import sys
import math
import pygame
from pygame.locals import *
from pygame.color import *
import olpcgames
import elements
from elements import Elements
import tools
from helpers import *
from ilf import Facade

class PhysicsGame:
    def __init__(self,screen):
        self.screen = screen
        # get everything set up
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24) # font object
        self.canvas = olpcgames.ACTIVITY.canvas
        self.joystickobject = None 
        self.debug = True
        # create the name --> instance map for components
        self.toolList = {}
        for c in tools.allTools:
             self.toolList[c.name] = c(self)
        self.currentTool = self.toolList[tools.allTools[0].name]
        
        # set up the world (instance of Elements)
        self.world = elements.Elements(self.screen.get_size())
        self.world.renderer.set_surface(self.screen)
        
        # set up static environment
        self.world.add.ground()    
        
        #set up learning framework
        self.ilf = Facade(self);
        
    def run(self):
        self.running = True    
        while self.running:
            for event in pygame.event.get():
                # notify the learning framework
                #!!!IMPORTANT!!!: this has to be before the tool handles the event
                self.ilf.handleEvents(event, self.currentTool)
                self.currentTool.handleEvents(event)
            # Clear Display
            self.screen.fill((255,255,255)) #255 for white
        
            # Update & Draw World
            self.world.update()
            self.world.draw()
            
            # draw output from tools
            self.currentTool.draw()
            
            #Print all the text on the screen
            text = self.font.render("Current Tool: "+self.currentTool.name, True, (255,255,255))
            textpos = text.get_rect(left=700,top=7)
            self.screen.blit(text,textpos)  
            
            # Flip Display
            pygame.display.flip()  
            
            # Try to stay at 30 FPS
            self.clock.tick(30) # originally 50    

    def setTool(self,tool):
        self.currentTool.cancel()
        self.currentTool = self.toolList[tool] 

    def triggerSupport(self, interaction):
        olpcgames.ACTIVITY.updateILFLabel("DummyAgent: " + interaction.name + " lead to a problem!")

    def stopSupport(self):
        olpcgames.ACTIVITY.updateILFLabel("New detection process started...")

def main():
    toolbarheight = 75
    tabheight = 45
    pygame.init()
    pygame.display.init()
    x,y  = pygame.display.list_modes()[0]
    screen = pygame.display.set_mode((x,y-toolbarheight-tabheight))
    # create an instance of the game
    game = PhysicsGame(screen) 
    # start the main loop
    game.run()

# make sure that main get's called
if __name__ == '__main__':
    main()

