#Intelligent Systems Project Assignment
#Authors: Daniel Nelson, Tyler Beaumont
#MasterAgent.py
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from Mapping import Map
from Artist import Artist
import pygame
import pygame.gfxdraw
from Search_Methods.PSO import PSO
from Search_Methods.ACO import ACO
from math import ceil

class MasterRouter():
    #Central Controller. responsible for collecting & storing data, executing algorithms, and performing route visualistion /delegation.
    def __init__(self,search_method,width,height):
        self.id = "Master"
        self.width = width
        self.height = height
        self.KB = {#Knowledge base. vehicle information
            'vehicles':[],
            'packages':[],
            'world'   :None,
            'package_sum':0,
            'capacity_sum':0,
            'search_method':search_method.lower(),
            'num_locations':0
        }

    def setVehicles(self,vehicles):
        #Assigns vehicles & their cumulative capacity to KB
        print(self.id +": Recieving List of Available Vehicles...")
        capacity_sum = 0
        for v in vehicles:
            capacity_sum += v.getCapacity(self.id)

        self.KB['vehicles'] = vehicles
        self.KB['capacity_sum'] = capacity_sum

        print("{0}: Sum of all Capacities is:{1}\n".format(self.id,capacity_sum))

    def setPackages(self,packages):
        #Assigns packages & their cumulative weight to KB
        print(self.id +": Recieving List of Packages...")
        temp_package_sum = \
            sum(p.weight for p in packages)

        print(self.id + ": Sum of Package Weights:"+ str(temp_package_sum) + "\n")
        self.KB['packages'] = packages
        self.KB['package_sum'] = temp_package_sum

    def setWorld(self,locations):
        #Assigns world representation to KB & num locations
        self.KB['world'] = \
            Map(self.getField('search_method'), locations, self.getField('packages') )
        self.setField('num_locations',len(locations)-1)

    def getField(self,field):
        #Generic Getter for KB
        if field in self.KB:
            return self.KB[field]
        else: return None

    def setField(self,field,value):
        #Generic Setter for KB
        if field in self.KB:
            self.KB[field] = value
            return True
        else:
            self.KB.update({field:value})
            return False

    def Execute(self):
        #Execute algorithm from defined list
        method = self.getField('search_method')

        if method == 'aco':
            alg = ACO(self.getField('world'),self.getField('vehicles'))
        elif method == 'pso_s1':
            alg = PSO(self,self.width, self.height,True)
        elif method == 'pso_s2':
            alg = PSO(self,self.width, self.height,False)
   
        return alg.run()

    def Visualise(self,stepthrough=False):
        #Route visualisation
        pygame.init()
        #Initialise Artist, responsible for route drawing
        artist = Artist(self.getField('vehicles'),
                        self.getField('world'),
                        self.width, self.height)

        #Drawing Loop
        clock = pygame.time.Clock()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                #Draw
                artist.Draw(stepthrough)

            clock.tick(30)#Limit FPS
        pygame.quit()
    
    def RouteSum(self):
        #Sums all routes
        return sum(v.sumRoute() for v in self.getField('vehicles'))

    def Stats(self):
        #outputs route statistics, sum, average, weights, ect...
        print("Num Vehicles:{0}\nNum Locations:{1}"\
            .format(len(self.getField('vehicles')),
                    len(self.getField('world').locations) ))

        pathsum = 0
        for v in self.getField('vehicles'):
            if v.route == None: break
            print(v)

            pathsum += v.sumRoute()
        pathavg = pathsum / len(self.getField('vehicles'))
        print("Path Avg:{0}\nPath Sum:{1}".format(pathavg,self.RouteSum()))


    def EqulaliseVehicles(self):
        #"Takes the input list of packages, and resets vehicle capacties accordingly
        allocation = ceil(self.KB['package_sum'] / len(self.KB['vehicles']) )

        for v in self.KB['vehicles']:
            v.capacity = allocation

        print(allocation)