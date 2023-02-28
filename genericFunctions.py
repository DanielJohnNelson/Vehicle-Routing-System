#Intelligent Systems Project Assignment
#Authors: Daniel Nelson, Tyler Beaumont
#genericFunctions.py

from math import sqrt

def CalcDistance2(aStartLoc, aEndLoc):
    #takes two objects, with attributes x&y
    return sqrt( (aEndLoc.X - aStartLoc.X)**2 + (aEndLoc.Y - aStartLoc.Y)**2 )

def CalcDistance3(X,Y,aEndLoc):
    #takes two raw x&y values, and one object with x&y attributess
    return sqrt( (aEndLoc.X - X)**2 + (aEndLoc.Y - Y)**2 )

def CalcDistance4(X1,Y1,X2,Y2):
    #takes four raw x&y values
    return sqrt( (X2 - X1)**2 + (Y2 - Y1)**2 )

def CalcDimensionalDistance(D1,D2):
    #Euclidian distance for d Dimensions
    result = 0
    for d1,d2 in zip(D1,D2):
        result += (d2 - d1)**2
    return sqrt(result)

def SumRouteDistance(route):
    #sums the distance between all locations in route
    total_dist = 0
    if len(route) < 1 : return total_dist
    for i in range(len(route)-1):
        aStartLoc = route[i]
        aEndLoc = route[i+1]
        total_dist += sqrt( (aEndLoc.X - aStartLoc.X)**2 + (aEndLoc.Y - aStartLoc.Y)**2 )
    return total_dist

def SumRouteWeight(route):
    #sums the weight of all packages of locations in route
    if route == None or len(route) < 1: return 0
    return sum(l.GetPackageWeight() for l in route)

def defaultsParser(filename):
    #Opens given file and parses as gui defaults format
    defaults = {}
    with open(filename,'r') as file:
        lines = [line.split(':') for line in file]
        #print(lines)
        for line in lines:
            defaults.update({line[0]:line[1].rstrip() })
    return defaults

