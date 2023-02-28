#Intelligent Systems Project Assignment
#Authors: Daniel Nelson, Tyler Beaumont
#DeliveryAgent.py

from math import sqrt

class DeliveryAgent():
    #Delivery Agent / Vehicle class
    def __init__(self,_id,_capacity=100,_col=(0,0,0) ):
        self.id = "v_%s" % _id
        #Capacity of agent
        self.capacity = _capacity
        #Route to be determined
        self.route = None#[]
        self.colour = _col

        #Variables for PSO
        self.xref = None
        self.yref = None
        self.r    = None

        self.distances = None

    def getCapacity(self,requester):
        #return self capcity
        print("{0} Requested capacity from {1}: Responded with:{2}".format(requester,self.id,self.capacity))
        return self.capacity

    def printRoute(self):
        if self.route == None or len(self.route) < 1:return None
        result = ""

        for location in self.route:
            result += str(location)

        return result

    def sumRoute(self):
        if type(self.route) == tuple:
            self.route = self.route[1]
        if self.route == None or len(self.route) < 1:return 0
        else:
            dsum = 0
            #Calculate sum over route length
            for i in range(len(self.route)):
                if i == len(self.route)-1:return dsum
                aStartLoc = self.route[i]
                aEndLoc = self.route[i+1]
                dsum += sqrt( (aEndLoc.X - aStartLoc.X)**2 + (aEndLoc.Y - aStartLoc.Y)**2 )
        
    def sumPackages(self):
        total = 0
        if len(self.route) < 1 or self.route == None:
            return total
        #Calculate sum over all packages
        for l in self.route:
            total += l.GetPackageWeight()

        return total
            #return sum(l.Distance for l in self.route)

    def __repr__(self):
            #Python magic function, defines how obj is represented in when print is called
        return "X:{1}, Y:{2}, C:{3}\n".format(self.x,self.y,self.capacity)

    def __str__(self):
        return "{0}:\ncapacity:{1}\nroute length:{2}\npackage sum:{3}\nroute:{4}\n".format(self.id,self.capacity,self.sumRoute(),self.sumPackages(),self.printRoute())