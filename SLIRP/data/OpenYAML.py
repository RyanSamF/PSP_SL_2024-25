import rocketpy as rp
import numpy as np
import yaml
import math
import csv


FT_TO_M = 3.28084
IN_TO_M = 1 / 39.37
LBS_TO_KG = 0.4536



def readYaml (filename):
    ############################################################################
    # Function to read YAML files with rocket data and convert them into 
    # RocketPy rocket class with data from config file
    #INPUTS:
    # Filename - filepath of the YAML vehicle file within the directory
    #OUTPUTS:
    # vehicle - RocketPy rocket class with vehicle data from the loaded YAML file
    # m_heav - mass of the heaviest section in lbs
    #############################################################################
    
    #Opens YAML file and seperates dictionary of dictionaries into individual dicts and variables
    #The contents of each dict defined here can be viewed within the config files
    #POSSIBLY ADD DEFINITIONS HERE LATER 
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    files_data = data["githubfiles"]
    motor_data = data["motor"]
    rocket_data = data["rocket"]
    nose_data = data["nose_cone"]
    fins_data = data["fins"] 
    parachutes_data = data["parachutes"]
    thrusturl = files_data["thrusturl"] #filepath for the thrust vs time csv file
    boostermass = rocket_data["booster"] #Mass of booster section (NOT CURRENTLY USED)
    avionicsmass = rocket_data["midsec"] #Mass of avionics section (NOT CURRENTLY USED)
    nosemass = rocket_data["uppersec"] #Mass of upper section (NOT CURRENTLY USED)
    m_heav = rocket_data["h_section"] #mass of heaviest section for energy calculations
    dragurl = files_data["dragurl"] #filepath for the drag vs mach number csv file

    #Defines the motor using the motor_data dictionary
    engine = rp.GenericMotor(
        coordinate_system_orientation= "nozzle_to_combustion_chamber", #position of 0 = end of nozzle
        thrust_source = thrusturl, #thrust vs time csv file
        dry_mass = (motor_data["net_mass"] - motor_data["prop_mass"]) * LBS_TO_KG, #Rocket's dry mass (lbs -> kg)
        propellant_initial_mass = motor_data["prop_mass"] * LBS_TO_KG, #Propellant mass (lbs -> kg)
        #center_of_dry_mass_position = motor_data["center_of_dry_mass"] / 39.37, #in -> m
        #dry_inertia = (1.22 / 4.882, 1.22 / 4.882, 0.042 / 4.882),
        chamber_radius= motor_data["chamber_rad"] * IN_TO_M ,#Combustion Chamber radius (in -> meters)    
        chamber_height = motor_data["chamber_height"] * IN_TO_M, #Combustion Chamber height (in -> meters)
        chamber_position = motor_data["center_of_dry_mass"] * IN_TO_M, #Combustion chamber position (in -> meters)
        nozzle_radius = motor_data["nozzle_rad"] * IN_TO_M, #Nozzle radius (in -> meters)
        burn_time = None #Burn time (forced undefined, as it will be defined by thrust curve length)
    )
    rp.Rocket.m_heav = None #adds new variable to rocketpy rocket class JANK SOLUTION, MAY CAUSE ISSUES
    rp.Rocket.main_deploy = None #m_heav is mass of heaviest section, main_deploy is main parachute deploy height
    print(type(rp.Rocket))
    vehicle = rp.Rocket(
    radius = rocket_data["radius"] * IN_TO_M, #airframe radius (in -> meters)
    mass = (rocket_data["mass"] * LBS_TO_KG), #Rocket mass WITHOUT motor (lbs -> kg)
    inertia = np.array(rocket_data["inertia"]) * LBS_TO_KG / FT_TO_M**2, #inertia vector (lbs/ft^2 -> kg/m^2)
    #First two are longitudinal moment of inertia, last is rotational)
    power_off_drag = dragurl, #Coefficient of drag when power is off vs mach number
    power_on_drag = dragurl, #Coefficient of drag when power is on vs mach number
    coordinate_system_orientation = "nose_to_tail", #defines position 0 = end of nose
    center_of_mass_without_motor = rocket_data["COM"] * IN_TO_M #Center of mass WITHOUT motor (in -> meters)  
    )
    vehicle.add_motor(engine, rocket_data["length"] * IN_TO_M) #position of motor in rocket

    #adds nose cone to vehicle
    nose_cone = vehicle.add_nose(
        length = nose_data["length"] * IN_TO_M, #Length of nose cone (in -> meters)
        kind = "von karman", #Nose type, IF EVER NOT VON KARMAN CHANGE THIS
        position = 0 #defines nose cone at end of nose cone (nose to tail orientation)
    )
    
    #adds fins to vehicle
    fin_set = vehicle.add_trapezoidal_fins(
        n = fins_data["n"], #number of fins
        root_chord = fins_data["root_chord"] * IN_TO_M, #root chord length (in -> meters)
        tip_chord = fins_data["tip_chord"] * IN_TO_M, #tip chord length (in -> meters)
        position = (rocket_data["length"] - fins_data["root_chord"]) * IN_TO_M, #position (in -> meters)
        span = fins_data["span"] * IN_TO_M, #span (in -> meters)
        sweep_length = fins_data["sweep"] * IN_TO_M #Sweep length (in -> meters),
        #   airfoil = (airfoilLift, "degrees") #OPTIONAL ADD AIRFOIL TO FINS ((WIP))
    )
    #Adds main if present
    if parachutes_data["main_present"]:
        main = vehicle.add_parachute(
            name = "main",
            cd_s = parachutes_data["main_cd"] * (parachutes_data["main_diameter"] / 2 * IN_TO_M) ** 2 * math.pi, 
            #Defined as area (m^2) * coefficient of drag 
            trigger = parachutes_data["main_trigger"] / FT_TO_M, #altitude of main deployment ft -> meters
            lag = 0 #lag between deployment signal and deployment
        )

    #Adds drogue if present
    if parachutes_data["drogue_present"]:
        drogue = vehicle.add_parachute(
            name = "drogue",
            lag = 0,# lag between deployment signal and deployment
            cd_s = parachutes_data["drogue_cd"] * (parachutes_data["drogue_diameter"] / 2 * IN_TO_M) ** 2 * math.pi,
            #Defined as area (m^2) * coefficient of drag 
            trigger = "apogee" #Triggers drogue and apogee
        )
    vehicle.m_heav = m_heav
    vehicle.main_deploy = main.trigger
    return(vehicle)

