#Intelligent Systems Project Assignment
#Authors: Daniel Nelson, Tyler Beaumont
#GUI.py

from tkinter import Button,Spinbox,Tk,Label,Checkbutton,IntVar,StringVar,Radiobutton,Frame,LEFT,RIGHT,TOP

class InitialSetupGUI:
    #Tkinter gui manager wrapper class
    def __init__(self,title,root,defaults):
        self.data = None
        self.root = root
        self.root.title(title)
        gsettings_frame = Frame(root)
        gsettings_frame.grid(pady=10)

        pso_settings_frame = Frame(root)
        pso_settings_frame.grid(pady=10)

        Label(gsettings_frame,text="Global Settings").grid(row=0,column=0)
        
        #Location & Vehicle settings
        self.num_locs_label = Label(gsettings_frame,text="# Locations").grid(row=1,column=0)
        self.num_locs = Spinbox(gsettings_frame,from_=2,to=50,width=10,textvariable=IntVar(value=defaults['num_locations']))
        self.num_locs.grid(row=2,column=0)

        self.num_vehc_label = Label(gsettings_frame,text="# Vehicles").grid(row=1,column=1)
        self.num_vehc = Spinbox(gsettings_frame,from_=1,to=10,width=10,textvariable=IntVar(value=defaults['num_vehicles']))
        self.num_vehc.grid(row=2,column=1)

        #Screen dimensions settings
        self.screen_width_label = Label(gsettings_frame,text="Screen Width").grid(row=3,column=0)
        self.screen_width = Spinbox(gsettings_frame,from_=300,to=2560,width=10,textvariable=IntVar(value=defaults['screen_width']))
        self.screen_width.grid(row=4,column=0)

        self.screen_height_label = Label(gsettings_frame,text="Screen Height").grid(row=3,column=1)
        self.screen_height = Spinbox(gsettings_frame,from_=300,to=1440,width=10,textvariable=IntVar(value=defaults['screen_height']))
        self.screen_height.grid(row=4,column=1)

        #PSO Paramater Settings
        Label(pso_settings_frame,text="PSO Settings").grid(row=0,column=0)
        self.pso_pop_label = Label(pso_settings_frame,text="Swarm Population").grid(row=1,column=0)
        self.pso_pop = Spinbox(pso_settings_frame,from_=1,to=500,width=10,textvariable=IntVar(value=defaults['pso_population']))
        self.pso_pop.grid(row=2,column=0)#.pack(side=TOP)#(side=LEFT)

        self.pso_iter_label = Label(pso_settings_frame,text="# Iterations").grid(row=1,column=1)
        self.pso_iter = Spinbox(pso_settings_frame,from_=1,to=2000,width=10,textvariable=IntVar(value=defaults['pso_iterations']))
        self.pso_iter.grid(row=2,column=1)#.pack(side=TOP)#(side=LEFT)
        
        #Use default Google Data
        self.useGoogleData = IntVar()
        self.useGoogleDataCheck = Checkbutton(root,variable=self.useGoogleData,
                                        text="Use Google OR-Tools test data.",
                                        onvalue=True,offvalue=False)
        if(defaults['use_google_test_data'] == 'True'):
            self.useGoogleDataCheck.select()
        self.useGoogleDataCheck.grid(row=3,column=0,pady=10)

        #Use step through of routes
        self.useStepping = IntVar()
        self.useSteppingCheck = Checkbutton(root,variable=self.useStepping,
                                        text="Step through routes.",
                                        onvalue=True,offvalue=False)
        if(defaults['use_route_stepping'] == 'True'):
            self.useSteppingCheck.select()
        self.useSteppingCheck.grid(row=4,column=0,pady=10)

        #package input file as list
        self.usePackageList = IntVar()
        self.usePackageListCheck = Checkbutton(root,variable=self.usePackageList,
                                        text="Use Package Input File.",
                                        onvalue=True,offvalue=False)
        if(defaults['use_package_list'] == 'True'):
            self.usePackageListCheck.select()
        self.usePackageListCheck.grid(row=5,column=0,pady=10)

        methods_frame = Frame(root)

        SearchMethods = [
            ("ACO","aco","normal"),
            ("PSO W/Local improvement","pso_s1","normal"),
            ("PSO No Local Improvement","pso_s2","normal"),
            ("Testing (10-50 Locations)", "test", "normal")]

        self.searchMethod = StringVar()
        self.searchMethod.set("aco")

        for text,val,state in SearchMethods:
            temp = Radiobutton(methods_frame,variable=self.searchMethod,
                                            text=text,value=val,state=state,anchor='w').pack(fill='both')

        methods_frame.grid(row=6,column=0,pady=10)#.pack()

        Button(root,text="Done",width=10,command=self.__getData__).grid(row=7,column=0)
    
    def getData(self):
        return self.data

    def __getData__(self):
        #fetch data from widgets, store, then destroy root
        self.data = {'num_locations': int(self.num_locs.get()),
                'num_vehicles' : int(self.num_vehc.get()),
                'useGoogleData': self.useGoogleData.get(),
                'method':self.searchMethod.get(),
                'pso_population':int(self.pso_pop.get()),
                'pso_iterations':int(self.pso_iter.get()),
                'screen_width':int(self.screen_width.get()),
                'screen_height':int(self.screen_height.get()),
                'use_stepping':self.useStepping.get(),
                'use_package_list':self.usePackageList.get()}
        #destroy the settings gui when starting
        self.root.destroy()
        