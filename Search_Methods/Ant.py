#Intelligent Systems Project Assignment
#Authors: Daniel Nelson
#Ant.py
import random
from Mapping import ACO_Location as Location,ACO_Neighbour as Neighbour
#RouteMap import Location, Neighbour

class Ant():
    def __init__(self, aLocation : Location, aPherDelta, aAntCapacity):
        #Ants current location
        self.Location = aLocation
        #Pheremone delta increase
        self.PherDelta = aPherDelta
        #Vehicle capacity constraint
        self.AntCapacity = aAntCapacity
        #Current weight taken on route
        self.CurrentWeight = 0
        #Best Route Cost
        self.BestCost = 999999
        #Array of locations in best route
        self.BestRoute = []
        #Array of locations in current route
        self.CurrentRoute = []
        #Current route cost
        self.RouteCost = 0
        #Best Neighbor at current location
        self.BestNeighbor = None
        #Boolean indicating more locations to visit
        self.MoreLocations = True
        #Local visited location array
        self.LocalVisited = []

    def CalculateMove(self, aVisited, aMap):
        
        #Calculate individual scores
        self.Location.CalculateScores()
        #Calculate individual probabilities
        self.Location.CalculateProbabilities()
        #Get neighbors
        lLocalNeighbors = self.Location.GetNeighbors()

        lNeighbors = []
        lProbs = []
        
        #Loop over neighbors
        for lNeighbor in lLocalNeighbors:
            #Check if valid neighbor
            if((lNeighbor.GetPackageWeight() + self.CurrentWeight) <= self.AntCapacity) and (self.SameLoc(lNeighbor, aVisited) == False):
                #Append to list of valid neighbors and probabilities
                lNeighbors.append(lNeighbor)
                lProbs.append(lNeighbor.GetProbability())
                
        #Check if any valid neighbors
        if len(lNeighbors) > 0:

            self.BestNeighbor = random.choices(lNeighbors, weights=lProbs, k=1)
            #Change location
            self.BestNeighbor = self.BestNeighbor[0]
            #Change ant location
            self.Location = self.BestNeighbor.GetLocation()
            #Add weight of package to tally
            self.CurrentWeight += self.BestNeighbor.GetPackageWeight()
            #Append to visited list
            aVisited.append(self.BestNeighbor)
            #Append to current route
            self.CurrentRoute.append(self.BestNeighbor)
            #Add route cost
            self.RouteCost += self.BestNeighbor.GetDist()

        else:
            #Mark no more locations
            self.MoreLocations = False
            #Send back to warehouse
            if len(self.CurrentRoute) > 0:
                self.CurrentRoute.append(self.CurrentRoute[0])
            

    def UpdateLocal(self): 
        #Update local pheremone 
        if self.BestNeighbor != None:
            #Apply formula
            self.BestNeighbor.SetPheremone( ( (1 - self.BestNeighbor.GetDecay() ) * self.BestNeighbor.GetPherLvl() + self.PherDelta))


    def UpdateBest(self):
        #Update best ant route if current is better
        if self.RouteCost < self.BestCost:
            #Update best cost
            self.BestCost = self.RouteCost
            #Update best route of location objects
            self.BestRoute = self.CurrentRoute

    def FindRoute(self, aVisited, aMap):
        self.CurrentRoute.append(aVisited[0])
        while self.MoreLocations:
            #Calculate move on current iteration
            self.CalculateMove(aVisited, aMap)
            #Update local pheremone
            self.UpdateLocal()
        #Update best current route if better
        self.UpdateBest()

    def SameLoc(self, aNeighbor, aList):
        #Check if a neighbor is the same as visited list
        for location in aList:
            if aNeighbor.X == location.X and aNeighbor.Y == location.Y:
                return True
        return False

    def ResetAnt(self):
        #Reset ant stats to default
        self.CurrentRoute = []
        self.CurrentWeight = 0
        self.MoreLocations = True

        self.RouteCost = 0


    def GetDelta(self):
        return self.PherDelta

    def GetRoute(self):
        return self.CurrentRoute

    def GetBestRoute(self):
        return self.BestRoute

    def GetRouteCost(self):
        return self.RouteCost

        
