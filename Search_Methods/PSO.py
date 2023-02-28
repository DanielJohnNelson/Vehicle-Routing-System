#Intelligent Systems Project Assignment
#Authors: Tyler Beaumont
#PSO.py

from random import randint
from genericFunctions import CalcDistance2,CalcDistance3,CalcDistance4,SumRouteWeight,\
CalcDimensionalDistance,SumRouteDistance


def two_opt(p,route):
    #Local optimision of route, by swapping 
    pairs of locations to find more efficient permuations#
    def swap(r,i,j):
        #Returns new route by reversing sections of existing route#
        new_route = r[0:i-1]
        temp = r[i:k];temp.reverse()
        new_route.extend(temp)
        new_route.extend(r[k+1:])

        return new_route

    #route
    n = len(route)
    baseline = SumRouteDistance(route)

    for i in range(1,n-2):
        for k in range(i+2,n):
            new_route = swap(route,i,k)
            new_baseline = SumRouteDistance(new_route)
            if new_baseline < baseline:
                route = new_route
                baseline = new_baseline
                break

    return route

class Faux_Vehicle():
    #Temporary Vehicle Class to avoid overwriting vehicle data 
    and allow for more flexible processing
    def __init__(self,xref,yref,radius,max_capacity):
        self.xref = xref
        self.yref = yref
        self.radius = radius
        self.capacity = 0
        self.max_capacity = max_capacity
        self.route = []

class Particle():
    #Individual particle of swarm
    def __init__(self,vehicles,width,height,locations,capacity=15):
        self.fitness       = None
        self.pbest_fitness = None
        self.lbest_fitness = None
        self.nbest_fitness = None
        self.max_capacity  = capacity

        self.neighbours = []
        self.routes     = []
        self.capacity   = 0
        self.dimensions = []

        for v in vehicles: #3m dimensional representation, where m is number of vehicles
            self.dimensions.append(randint(1,width))#xref
            self.dimensions.append(randint(1,height))#yref
            self.dimensions.append(randint(int(width/3),int(width/2)))#radius
                    
        self.velocity = [0] * (3 * len(vehicles))

        self.pbest = self.dimensions.copy()#personal best, initially starting position
        self.lbest = None  #local best location
        self.nbest = None  #neighbourhood best location

        self.penalty = 0#multiplier for each missed location

    def updatePbest(self):
        #updates personal best to current position if it's fitness is better 
        if self.fitness < self.pb.fitness:
            self.pb = self.pos

    def calculateNbest(self):
        #determines personal best position of neighbours
        top_term = self.fitness - self.pbest_fitness # top term of division in equation
        nbest = []

        for d in range(len(self.dimensions)):
            #get neighobur with best value
            try:
                neighbour_fdr = [( (self.fitness - n.pbest_fitness)/(abs( self.dimensions[d] - n.pbest[d])) ,n) \
                                for n in self.neighbours]
            except ZeroDivisionError:
                #potenital BUG divide by zero bug when both same value. maybe set to 1, or set to one of their inital values
                neighbour_fdr =  [( (self.fitness - n.pbest_fitness)/ self.dimensions[d] ,n) \
                                for n in self.neighbours]
            best_fdr = min(neighbour_fdr,key=lambda x:x[0])
            nbest.append(best_fdr[1].pbest[d])
        
        self.nbest = nbest


    def calculate_fitness(self,routes,penalty):
        #Calculates fitness as sum of route distances
        + a penalty multiplier
        total_sum = 0
        for route in routes:
            total_sum += SumRouteDistance(route)

        return total_sum + (penalty * 10000)#adding penalty for missing locations

    def decode(self,dimensions,vehicle,world,local_improvement):
        #Decoding takes a particles dimension (which relate to each vehicle),to predictably build a set of route of each vehicle, that adhere to capacity constraints
        visited = []
        routes = []

        d = 0
        vehicles = []
        for v in vehicle:
            xref = dimensions[d]
            yref = dimensions[(d+1)]
            radius = dimensions[(d+2)]
            V = Faux_Vehicle(
                            xref, yref, radius, v.capacity )
            vehicles.append(V)
            d += 3
            #2.a construct routes
            route = []

            #list of tuples (distance from v ref points to location,actual location object)
            location_distances = [ (CalcDistance3(xref,yref,l),l) for l in world.locations if l not in visited]
            #List of locations within vehicles radius
            in_radius = [l for l in location_distances if l[0] <= radius]

            #sort to give closest locations priority
            in_radius.sort(key=lambda l:l[0])

            for l in in_radius:
                if l[1].package_sum + SumRouteWeight(route) <= v.capacity:
                    route.append(l[1])
                    visited.append(l[1])

            route.insert(0,world.depot[0]);route.append(world.depot[0])#add depots to route
            V.route = route
            routes.append(route)

        #2.b optimise partical routes
        #conditional route improvement
        if local_improvement: self.local_improvements(routes)
            
        #2.c insert remaining customers
        remaining = [l for l in world.locations if l not in visited]
        remaining.sort( key=lambda x: CalcDistance2( x,world.depot[0] ), reverse=True )

        for l in remaining:
            vehicles.sort(key=lambda x:CalcDistance3(x.xref,x.yref,l))
            for v in vehicles:#now ordered by closest to location
                if (l.package_sum + SumRouteWeight(v.route) <= v.max_capacity) and l not in visited:
                    if len(v.route) == 2:v.route.insert(-1,l)
                    else: v.route.insert(-2,l)
                    visited.append(l)
                    break


        #2.d re-optimise
        #add a pentalty for this particle
        #this essentially ensures that any particle that does not visit all locations, will never be the best
        remaining = [l for l in world.locations if l not in visited]
        penalty = len(remaining)

        #conditional route improvement
        if local_improvement: self.local_improvements(routes)

        return (routes,penalty)

    def local_improvements(self,routes):
        #apply two-opt algorithm to each route,
        to locally improve each
        for route in routes:
            route = two_opt(self,route)

    def __repr__(self):
        #Python representation function
        return "X:{0},Y:{1}".format(self.X,self.Y)


class Swarm():
    #Acts as a container for each particle to easily delegate processing and hold certain values required externally to the particle
    def __init__(self,population,vehicles,width,height,locations):
        self.vehicles = vehicles
        self.particles = [ Particle(vehicles,width, height,locations) for p in range(population) ]

    def evaluateNbest(self):
        #Delegates computation to each particle
        for p in self.particles:
            p.calculateNbest()

    def evaluateLbest(self,K=5):
        #determine local best location from other nearby particles
        for p in self.particles:
            #Get Neighbours
            neighbours = [n for n in self.particles if n != p]
            neighbours.sort(key=lambda x: CalcDimensionalDistance(p.pbest,x.pbest))#sort closest to furthest
            p.neighbours = neighbours[:K]#take only the K-closest

            neighbours.append(p)#append so we can easily set lbest for all

        lbest_particle = min(neighbours,key=lambda x: x.pbest_fitness)
        for n in neighbours:
            n.lbest = lbest_particle.pbest
            n.lbest_fitness = lbest_particle.pbest_fitness

    def evaluateGbest(self):
        #get the overall best position from all particles
        best_particle = min(self.particles, key=lambda x: x.pbest_fitness)

        self.gbest = best_particle.pbest
        self.gbest_fitness = best_particle.pbest_fitness

    def evaluatePbest(self,world,local_improvement):
        #Delegates computation to each particle
        for p in self.particles:
            pb_result = p.decode(p.pbest,self.vehicles,world,local_improvement)
            pb_route = pb_result[0]
            pb_penalty = pb_result[1]

            p.pbest_fitness = p.calculate_fitness(pb_route,pb_penalty)

            if p.fitness < p.pbest_fitness:
                p.pbest = p.dimensions
                p.pbest_fitness = p.fitness

    def evaluateRoute(self):
        #Calculates Routes Fitnesses. Delegates computation to each particle
        for p in self.particles:
            p.fitness = p.calculate_fitness(p.routes,p.penalty)

    def updateParticles(self,t,T,xmax,xmin):
        #Update each particles position and velocity
        cp = 0.5#pb position acceleration constant
        cg = 0.5#global best position acceleration constant
        cl = 1.5#local best position acceleration constant
        cn = 1.5#neighbourhood best position acceleration constant
        w1 = 0.9#First Intertia Weight
        wT = 0.4#Last Interia Weight
        u  = randint(0,1)#uniform random number
        wt = wT + (t-T)/(1-T) * (w1 - wT)#interial weight of t'th iteration

        for p in self.particles:
            for d in range(len(p.dimensions)):
                p.velocity[d] = wt*p.velocity[d]+ \
                                    cp*u*(p.pbest[d]    - p.dimensions[d] ) + \
                                    cg*u*(self.gbest[d] - p.dimensions[d] ) + \
                                    cl*u*(p.lbest[d]    - p.dimensions[d] ) + \
                                    cn*u*(p.nbest[d]    - p.dimensions[d] )

                p.dimensions[d] = p.dimensions[d] + p.velocity[d]
                #Boundary Constraining
                if p.dimensions[d] > xmax:
                    p.dimensions[d] = xmax
                    p.velocity[d] = 0
                #Boundary Constrainings
                if p.dimensions[d] < xmin:
                    p.dimensions[d] = xmin
                    p.velocity[d] = 0

    def decode(self,world,local_improvement):
        #Delegates processing to individual particles
        for p in self.particles:
            result = p.decode(p.dimensions,self.vehicles,world,local_improvement)
            p.routes = result[0]
            p.penalty = result[1]


class PSO:
    #Algorithm class, used to easily launch
    def __init__(self,Master,width,height,local_improvements):
        #needed for random particle position initialisation
        self.width  = width
        self.height = height
        self.Master = Master
        self.world  = Master.getField('world')

        self.vehicles = self.Master.getField('vehicles')

        self.local_improvement = local_improvements#boolean

    def AssignRoutes(self,routes):
        #Assign final route set to each vehicle#
        #print("Assigning Routes to Vehicles")
        for i in range(len(self.vehicles)):
            self.vehicles[i].route = routes[i]
            print(self.vehicles[i].id + ": Route Assigned.")

    def run(self,population=25,iterations = 250):
        #Main entry point, this function encapsulates all necessary orchestration
        #9. Stopping criteria
        K = 5 #num of neighbours; arbirary value
        T = self.Master.getField("pso_iterations")
        population = self.Master.getField("pso_population")
        
        print("--Particle Swarm Optimisation--\n--Local Improvements:%s--\nT(%s) P(%s)\n" % (self.local_improvement,T,population)) 
        for t in range(1,T):
            #1. Initialise
            vehicles = self.vehicles
            swarm = Swarm(population, vehicles,self.width,self.height,self.world.locations)       
            #2. Deocode
            swarm.decode(self.world,self.local_improvement)
            #3. Compute Performance measure for each particle
            swarm.evaluateRoute()
            #4. Update pbest
            swarm.evaluatePbest(self.world,self.local_improvement)
            #5. Update gbest
            swarm.evaluateGbest()
            #6. Update lbest
            swarm.evaluateLbest(K)
            #7. Generate nbest
            swarm.evaluateNbest()
            #8. Update Velocity
            swarm.updateParticles(t,T,self.width,1)

        #10. Decode final solution
        p = Particle(vehicles,self.width,self.height,self.world.locations)
        p.dimensions = swarm.gbest
        p.fitness    = swarm.gbest_fitness

        final_routes = p.decode(p.dimensions,vehicles,self.world,self.local_improvement) 

        self.AssignRoutes(final_routes[0])
        