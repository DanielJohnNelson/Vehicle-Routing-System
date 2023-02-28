#Intelligent Systems Project Assignment
#Authors: Daniel Nelson, Tyler Beaumont
#MasterAgent.py

import TestData
from MasterRouter import MasterRouter
from GUI import InitialSetupGUI
import Packages as _Packages
from Packages import packageListParser
from tkinter import Tk
import time
from memory_profiler import memory_usage
from Statics import StartupMessage
from genericFunctions import defaultsParser

def main():
    #GUI Manager for inital setup of values

    print(StartupMessage)

    root = Tk()
    #Initialize GUI
    gui_defaults = defaultsParser("GUI_Defaults.txt")
    InitalSetupView = InitialSetupGUI("title",root,gui_defaults)
    root.mainloop()

    Inital_vals = InitalSetupView.getData()
    #example output ^
    #{'num_locations': 16, 'num_vehicles': 1, 'useGoogleData': 1}


    if (Inital_vals['method'].lower() == "test") :
        #Loop for both methods
        for x in range(3):
            if x == 0:
                lMethod = 'aco'
            elif x == 1:
                lMethod = 'pso_s1'
            else:
                lMethod = 'pso_s2'
            #Initialize variables
            Master = MasterRouter(lMethod,
                              Inital_vals['screen_width'],
                              Inital_vals['screen_height'])
            #Declare arrays for each set of location sizes
            lAcoMem = [0] * 5
            lAcoTime = [0] * 5
            lAcoRoute= [0] * 5
            lIndex = 0
            lLocationSize = 10
            #Loop over 50 iterations (10 per location size iteration)
            for i in range(1,50):
                #Create world and agents
                Locations = TestData.RandomLocations(lLocationSize)
                Vehicles = TestData.RandomVehicles( Inital_vals['num_vehicles'] )
                Master.setVehicles(Vehicles)
                if Inital_vals['use_package_list']:
                    Packages = packageListParser('package_input_list.txt')
                    Master.setPackages(Packages)
                    Master.EqulaliseVehicles()
                else:
                    Packages = _Packages.GeneratePackages(Master.getField('capacity_sum'),Locations )
                    Master.setPackages(Packages)
                
                Master.setWorld(Locations)
                Master.setField("pso_population",Inital_vals['pso_population'])
                Master.setField("pso_iterations",Inital_vals['pso_iterations'])
                #Start timer
                lStart = time.time()
                #Execute algorithm checking memory usage
                lMemUse = memory_usage(Master.Execute)
                #Stop time
                lTime = (time.time() - lStart)

                #Add to sum
                lAcoRoute[lIndex] += Master.RouteSum()
                lAcoTime[lIndex] += lTime
                lAcoMem[lIndex] += max(lMemUse)

                #Check if locationsize should increase
                if i % 10 == 0:
                    lLocationSize += 10
                    lIndex += 1
            
            #Calculate averages
            for index, x in enumerate(lAcoMem):
                lAcoRoute[index] /= 10
                lAcoMem[index] /= 10
                lAcoTime[index] /= 10


            lFile = open("Balanced_as_all_things_should_be.txt", "a")
            
            lFile.write("Method: " + lMethod.upper() + "\n")

            #Write to file
            for index, j in enumerate(lAcoTime):
                lFile.write("Locations ({0}) : Average Time ({1}), Max Memory ({2}), Average Route Length ({3})\n".format( (index + 1) * 10 , lAcoTime[index], lAcoMem[index], lAcoRoute[index] ))


            lFile.close()
    else:
        #Create Master Router, initialised with search method
        Master = MasterRouter(Inital_vals['method'],
                              Inital_vals['screen_width'],
                              Inital_vals['screen_height'])
        Master.setField("pso_population",Inital_vals['pso_population'])
        Master.setField("pso_iterations",Inital_vals['pso_iterations'])
        if(Inital_vals['useGoogleData']) : 
            #Initialise with default google-or-tools data

            Locations = TestData.TestLocations()
            #Testing vehicles
            Vehicles = TestData.TestVehicles()
            #Assign vehicles to master router.
            #master will update internal 'capacity_sum'
            Master.setVehicles(Vehicles)
            #Generate Package List
            Packages = _Packages.TestPackages(Locations)

            #Assign package list to master
            Master.setPackages(Packages)

            #Assign Masters World View
            Master.setWorld(Locations)
        else:
            #Initialise with randomised values
            Locations = TestData.RandomLocations(Inital_vals['num_locations'])
            #Create vehicles
            Vehicles = TestData.RandomVehicles( Inital_vals['num_vehicles'] )
            #Assign vehicles to master router.
            #master will update internal 'capacity_sum'
            Master.setVehicles(Vehicles)
            #Generate Package List
            if Inital_vals['use_package_list']:
                Packages = packageListParser('package_input_list.txt',Locations)
                #Assign package list to master
                Master.setPackages(Packages)
                Master.EqulaliseVehicles()
            else:
                Packages = _Packages.GeneratePackages(Master.getField('capacity_sum'),Locations )
                #Assign package list to master
                Master.setPackages(Packages)


            #Assign Masters World View
            Master.setWorld(Locations)

        #Performs selected optimisation algoritm.
        Master.Execute()

        #Show routes & Route statistics on completion
        Master.Stats()

        #start visualisation
        Master.Visualise(stepthrough=Inital_vals['use_stepping'])#can take width & height



if __name__ == '__main__':
    main()