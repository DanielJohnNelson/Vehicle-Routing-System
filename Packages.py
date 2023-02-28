#Intelligent Systems Project Assignment
#Authors: Daniel Nelson, Tyler Beaumont
#Packages.py

from random import choice,randint

def GeneratePackages(total_capacity,_locations):
    #Create a list of packages, with a max weight of no more than the combined carry capacity of all delivery agents
    Packages = []
    locations = _locations
    remaining_capacities = total_capacity
    while remaining_capacities > 0:
        rand_weight = randint(1,25)

        if (remaining_capacities - rand_weight) < 0:
            rand_weight = remaining_capacities
            break
        else:
            remaining_capacities = remaining_capacities - rand_weight
            
        Packages.append( 
            Package(
                choice(locations),rand_weight) 
            )

    return Packages

def TestPackages(Locations):
    #Google or tools example package data
    Packages = []
    data = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    for i in range(len(data)):
        Packages.append(Package(
            Locations[i],
            data[i] ) )

    return Packages

def packageListParser(filename,locations):
    #Opens and parses given file as input package list
    with open(filename,'r') as file:
        weights = [int(line) for line in file]


        packages = []
        for i,location in enumerate(locations): 
            packages.append(
                Package(location,weights[i])
            )

    return packages


class Package():
    #Package class, each pacakge is assigned a package, some locations may not be assigned any packages
    def __init__(self,_location,_weight):
        self.location = _location
        self.weight   = _weight

    def __repr__(self):
        return "for:{0},{1}kg.".format(self.location,self.weight)