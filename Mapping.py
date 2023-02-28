#Intelligent Systems Project Assignment
#Authors: Daniel Nelson, Tyler Beaumont
#Mapping.py

#This file heavily employs OOP principles of inheritance & polymorphism to reduce complexity for certain algorithms.In this way, PSO doesn't have to worry about overhead related to additional attributes used by ACO from math import sqrt

class Point():
    def __init__(self,_X,_Y):
        self.X = _X
        self.Y = _Y
        self.coords = (_X,_Y)
    def __repr__(self):
        return "X:{0},Y:{1}".format(self.X,self.Y)


class Core_Location(Point):
    #inherits point class
    def __init__(self,_X,_Y,_Packages,_T='l'):
        super().__init__(_X,_Y)
        self.Type = _T
        self.neighbours = []
        self.packages = _Packages
        self.package_sum = self.GetPackageWeight()

    def __repr__(self):
        results = "Location: %s\n  Neighbours:\n" % str(self.coords)
        if len(self.neighbours) > 0:
            for n in self.neighbours:
                results = results + "    %s : %s,\n" % (n.coords,n.dist)
        else:
            results = results + "no neighbours."
        return results

    def __str__(self):
        package_str = ""
        for package in self.packages:
            package_str += "{0}kg,".format(package.weight)

        return "{0} : packages:[{1}]".format(self.coords,package_str)

    def GetNeighbors(self):
        return self.neighbours

    def GetPackageWeight(self):
        if len(self.packages) < 1: return 0
        return sum(p.weight for p in self.packages)


class Core_Neighbour():
    #inherits point class, extends with distance
    def __init__(self,_L,_D,_S):
        self.actual_location = _L
        #Distance between initial location and neighbor
        self.Distance = _D
        #Savings calculation of adding neighbor to route instead of starting from depot
        self.Savings = _S

        self.X = _L.X
        self.Y = _L.Y
        self.coords = self.actual_location.coords

    def GetDist(self):
        return self.Distance

    def GetLocation(self):
        return self.actual_location

    def GetPackageWeight(self):
        if len(self.actual_location.packages) < 1: return 0
        return sum(p.weight for p in self.actual_location.packages)
        
    def __repr__(self):
        return "coords:({0},{1}), distance:{2}".format(self.actual_location.X, \
                                                        self.actual_location.Y, \
                                                        self.Distance)

    def __str__(self):
        package_str = ""
        for package in self.actual_location.packages:
            package_str += "{0}kg,".format(package.weight)

        return "{0} : packages:[{1}]".format(self.coords,package_str)

class ACO_Neighbour(Core_Neighbour):
    #inherits Core_neighbour class, extends ACO properties
    def __init__(self,_L,_D,_S):
        super().__init__(_L,_D,_S)
        #Pheremone level of path between location and neighbor
        self.PheremoneLvl = 1
        #Pheremone evaporation coefficient of path between location and neighbor
        self.Decay = 0.25#None  #Need to figure out
        #Score of attractiveness before probability
        self.Score = None
        #Probability of selection amongst other neighbors
        self.Probability = None


    def SetPheremone(self, aNum):
        self.PheremoneLvl = aNum

    def GetDecay(self):
        return self.Decay

    def GetPherLvl(self):
        return self.PheremoneLvl

    def CalculateScore(self):
        #Calculates individual score based off distance heuristic, pheremone level and savings
        self.Score = ((1 / self.Distance) * (self.PheremoneLvl))

    def CalculateProbability(self, aSum):
        #Calculates probability of selection
        if (self.Score==0 or self.Score==0.0) and (aSum==0 or aSum==0.0):return 0
        self.Probability = (self.Score / aSum)

    def GetScore(self):
        if self.Score is None: self.CalculateScore()
        return self.Score

    def GetProbability(self):
        return self.Probability

    def __repr__(self):
        return "XY:({0},{1}), D:{2}, PH:{3}, S:{4}, P:{5}".format(self.actual_location.X, \
                                                    self.actual_location.Y, self.Distance, \
                                                    self.PheremoneLvl, self.Score, self.Probability)

class ACO_Location(Core_Location):
    #Extends core location, extending with ACO properties
    def __init__(self,_X,_Y,_Packages,_T='l'):
        super().__init__(_X,_Y,_Packages,_T)
        self.Probabilities = []

    def GetProbabilities(self):
        return self.Probabilities

    def CalculateScores(self):
        #Calculates individual scores for each neighbor
        for lNeighbor in self.neighbours:
            lNeighbor.CalculateScore()

    def ScoreSum(self):
        #Calculates sum of scores over each neighbor
        lSum = 0
        for lNeighbor in self.neighbours:
            lSum = lSum + lNeighbor.GetScore()
        return lSum
    
    def CalculateProbabilities(self):
        #Calculates individual probabilities for each neighbor
        lCurrentProb = []
        for lNeighbor in self.neighbours:
            lNeighbor.CalculateProbability(self.ScoreSum())
            lCurrentProb.append(lNeighbor.GetProbability())

        self.Probabilities = lCurrentProb

class PSO_Location(Core_Location):
    def __init__(self,_X,_Y,_Packages,_T='l'):
        super().__init__(_X,_Y,_Packages,_T)

    def __repr__(self):
        return "PSO_L: X:{0},Y:{1}".format(self.X,self.Y)

class PSO_Neighbour(Core_Neighbour):
    def __init__(self,_L,_D,_S):
        super().__init__(_L,_D,_S)   


class Map():
    #Essentially a container class, simplifies access to locations & depots
    def __init__(self,search_method,_locations, _packages):
        #convert locations to relevant type
        if(search_method == 'aco'):
            self.location_type = ACO_Location
            self.neighbour_type = ACO_Neighbour
        elif(search_method == 'pso'):
            self.location_type = PSO_Location
            self.neighbour_type = PSO_Neighbour
        else: 
            self.location_type = Core_Location
            self.neighbour_type = Core_Neighbour
        #relevant location supertype,     #X,      #Y,    #Packages
        self.locations = [ self.location_type( l[0], l[1], [p for p in _packages if p.location is l] ) 
                            for l in _locations ]

        #locations with no packages are coloured light grey
        for l in self.locations:
            if len(l.packages) < 1: l.Type = 'np'#no packages

        #set first item in array as type depot
        self.locations[0].Type = 'd'  
        self.locations[0].packages = []

        #Single array of depot coordinates
        self.depot = []
        self.depot.append(self.locations[0])
        #Array of Location objects
        self.InitLocations(self.neighbour_type)

        self.depot[0] = self.locations.pop(0) #replace inital depot w/ depot with initialised neighbours

    def CalcDistance(self, aStartLoc, aEndLoc):
        return sqrt( (aEndLoc.X - aStartLoc.X)**2 + (aEndLoc.Y - aStartLoc.Y)**2 )

    def InitLocations(self,neighbour_type):
        #Loop over locations
        for l in self.locations:
            for n in self.locations:
                if n != l and n != self.depot[0]:
                    #Append new neighbor with distance and savings calculations
                    l.neighbours.append( 
                        neighbour_type(n,
                            self.CalcDistance(l,n), 
                            self.CalcSavings(l, n) 
                        ))

    def CalcSavings(self, aStartLoc, aEndLoc):
        #Apply savings formula
        return (self.CalcDistance(self.depot[0], aStartLoc) + self.CalcDistance(self.depot[0], aEndLoc) - self.CalcDistance(aStartLoc, aEndLoc))
        
    def __repr__(self):
        result = "["
        for l in self.locations:
            result = result + (l.coords + ',')
        return result + "]"