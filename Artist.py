#Intelligent Systems Project Assignment
#Authors: Daniel Nelson, Tyler Beaumont
#Artist.py
import pygame
import pygame.gfxdraw
from Statics import *
#from Mapping import *

class Artist():
    def __init__(self,vehicles,world,width,height):
        self.num_vehicles = len(vehicles)
        self.vehicles = vehicles
        self.world = world
        self.width = width
        self.height= height

        #Layer is pygame display
        self.layer = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Intelligent Systems - Assignment 1 (Daniel Nelson & Tyler Beaumont)")

        #largest x,y values to determine the minimum size of the map
        self.XMAX =max(world.locations,key=lambda i : i.X).X + (R*2)#R is added to ensure entire nodes are visible
        self.YMAX =max(world.locations,key=lambda i : i.Y).Y + (R*2)

        #Scale values to fit data to screen
        self.XSCL = width/self.XMAX
        self.YSCL = height/self.YMAX   

    def Path(self,A,B,colour,thickness=2):
        #given two nodes, draws a line connecting them
        a = ( int(A.X*self.XSCL) , int(A.Y*self.YSCL) )Scale X,Y values for screen
        b = ( int(B.X*self.XSCL) , int(B.Y*self.YSCL) )

        pygame.draw.line(self.layer,colour,a,b,thickness)

    def doNodes(self,d):
        #d is a node object#
        for node in d:
            X = int(node.X*self.XSCL)
            Y = int(node.Y*self.YSCL)
            pygame.gfxdraw.filled_circle(self.layer,X,Y,R,COLOURS[node.Type])
            #COLOURS[node.value] : looks up colour based on value of node
    
    def drawRoute(self,route,stepthrough,colour=(0,0,0),thickness=2):
        #Route should be a list of objects with X,Y attributes#

        for i in range(len(route)-1) :
            self.Path(route[i],route[i+1],colour,thickness)
            if stepthrough:#if flag set, draw step by step
                self.doNodes(self.world.depot)#draw depot only
                self.doNodes(self.world.locations)#draw remaining locations
                pygame.display.update()
                pygame.time.delay(500)#sleep(0.5)

    def Draw(self,stepthrough):
        #Encapsulates all drawing behaviours
        self.layer.fill(GREY)

        #this is to enable is to draw route from thickest to smallest, to avoid overlapping
        thickness = int( (self.num_vehicles * 1) + 3 )

        for vehicle in self.vehicles:
            if vehicle.route is not None:
                self.drawRoute(vehicle.route,stepthrough,vehicle.colour,thickness)
                thickness -= 1

        self.doNodes(self.world.depot)#draw depot only
        self.doNodes(self.world.locations)#draw remaining locations

        pygame.display.update()