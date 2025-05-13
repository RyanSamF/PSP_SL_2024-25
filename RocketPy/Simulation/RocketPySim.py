import rocketpy as rp
from matplotlib import *
import datetime
import numpy as np
import pandas
import yaml
import math
import matplotlib.pyplot as plt
import csv
from zoneinfo import ZoneInfo
from plots.plotting import param_graph, prof_graph

FT_TO_M = 3.28084
IN_TO_M = 1 / 39.37
LBS_TO_KG = 0.4536

def get_windy_env(env_time):
    ###################################################################################
    #Creates RocketPy environment variable using data from WINDY given a date and time
    #INPUTS:
    # env_time - time and date for environment defined using datetime
    #OUTPUTS:
    # env - environment variable with estimated atmospheric conditions
    ###################################################################################
    """POSSIBLY NOT WORKING"""

    env = rp.Environment(latitude = 40.505404, longitude = -87.019832,elevation=187)
    env.set_date(env_time)
    env.set_atmospheric_model(
        type="Windy",
        file="ICON"
    )
    #env.all_info()
    return(env)

def get_ST_env(wind_speed):
    ###################################################################################
    #Creates RocketPy environment variable using given windspeed with
    # standard atmosphere
    #INPUTS:
    # wind_speed - wind speed for launch (m/s)
    #OUTPUTS:
    # env - environment variable with given windspeed
    ###################################################################################

    #Defines environment with elevation, time and position ((MAKE THIS AN INPUT))
    env = rp.Environment(latitude = 40.505404, longitude = -87.019832, elevation=187)
        #URL = "http://weather.uwyo.edu/cgi-bin/sound   ing?region=naconf&TYPE=TEXT%3ALIST&YEAR=2024&MONTH=04&FROM=1300&TO=1312&STNM=72230"
    env.set_date((2024, 4, 13, 6))
    #Creates environment using standard atmosphere, and defining wind at 0 and 5000 meters as wind speed
    env.set_atmospheric_model(
        type="custom_atmosphere",
        wind_u = [(0, wind_speed), (5000, wind_speed)], #wind in one direction (m/s)
        wind_v = [(0, 0), (5000, 0)], #wind in perpendicular directon (m/s)
        pressure=None, #no change from standard atmosphere in pressure
        temperature=None) #no change from standard atmosphere in temperature
    return(env)

def multi_sim(angles, speeds, vehicle):
    ###################################################################################
    #Creates RocketPy environment variable using given windspeed with
    # standard atmosphere
    #INPUTS:
    # angles - launch angles simulated (deg)
    # speeds - wind speeds simulated (mph)
    # vehicle - RocketPy rocket class variable with desired constrution
    #OUTPUTS:
    # NONE?
    ###################################################################################

    speeds_ms = [x * 0.44704 for x in speeds]
    env_arr = []
    #time =  datetime.datetime(2025, 2, 23, 13, 30, 0, 0, tzinfo=ZoneInfo("America/Indianapolis"))
    for wind_speed in speeds_ms:
        env = get_ST_env(wind_speed)
        env_arr.append(env)

    #Data labels for final output csv file, all final data is appended to these lists
    final_vel = ["Final Velocity (ft/s)"]
    stability = ["Stability off rod (calibers)"]
    descent_time = ["Descent Time (seconds)"]
    ascent_time = ["Ascent Time (seconds)"]
    apogee = ["Apogee (ft)"]
    distance = ["Drift Distance (ft)"]
    max_mach = ["Max Mach Number"]
    max_vel = ["Max Velocity (ft/s)"]
    max_accel = ["Max Acceleration (ft/s)"]
    max_ke = ["Max Kinetic Energy (ft-lbf)"]
    under_drogue = ["Time Under Drogue (sec)"]
    under_main = ["Time Under Main (sec)"]
    vel_at_main = ["Velocity at Main Deployment (ft/s)"]
    run_params = [""]

    #simulates launch and records above data for each pair of wind speeds and angles 
    for i in range(0,len(angles)):
        testFlight   = rp.Flight(
            rocket = vehicle, environment = env_arr[i], rail_length = 3.6576, inclination = 90 - angles[i]  , heading = 270)
        time = testFlight.time
        vel_main_deploy = 0
        alt = testFlight.altitude(time) * FT_TO_M
        accel = testFlight.az(time) * FT_TO_M
        vel = testFlight.vz(time) * FT_TO_M
        mach_num = testFlight.mach_number(time)
        drift = -1 * testFlight.x(time) * FT_TO_M
        for vIndex in range(0,len(vel)):
            if vel_main_deploy == 0 and alt[vIndex] <= main.trigger * 3.281 + 10 and vel[vIndex] < -1:
                vel_main_deploy = vel[vIndex]
                print("Under Drogue" + str(vel_main_deploy))
                time_main_deploy = time[vIndex]
                #print("alt:" + str(alt[-1]))
        plot_name = param_graph(time, alt, vel, accel, speeds[i], angles[i], "RocketPy")
        prof_graph(drift, alt, plot_name + " RocketPy")

        final_vel.append(vel[-1])
        stability.append(testFlight.stability_margin(testFlight.out_of_rail_time))
        descent_time.append(time[-1] - testFlight.apogee_time)
        ascent_time.append(testFlight.apogee_time)
        apogee.append((testFlight.apogee - env.elevation) * FT_TO_M)
        distance.append(abs(drift[-1] + (FT_TO_M * testFlight.x(testFlight.apogee_time))))
        print(drift[-1])
        run_params.append(plot_name)
        max_mach.append(max(mach_num))
        max_vel.append(max(vel))
        max_accel.append(max(accel))
        max_ke.append(0.5 * vel[-1] ** 2 * m_heav / 32.17)
        vel_at_main.append(vel_main_deploy)
        under_drogue.append(time_main_deploy + testFlight.apogee_time)
        #print("after" + str(time_main_deploy))
        under_main.append(time[-1] - time_main_deploy)
        print(max(drift) + FT_TO_M * testFlight.x(testFlight.apogee_time))
        #print("Velocity at Main Deployment:" + str(vel_main_deploy))
        #print(testFlight.out_of_rail_velocity * FT_TO_M)
        #testFlight.plots.trajectory_3d()
    print(stability)
    print(vehicle.cp_position(0) / IN_TO_M)
    print(vehicle.center_of_mass(0) / IN_TO_M)    
    print(vel[-1])
    end_results = [run_params, 
        final_vel,
        descent_time,
        ascent_time,
        apogee, 
        distance, 
        max_vel, 
        max_accel, 
        max_mach, 
        max_ke, 
        under_drogue, 
        under_main,
        vel_at_main] #stability removed
    #print([i for i in end_results])
    #print(descent_time)
    #print(testFlight.parachute_events)
    


    # Specify the file name
    filename = "output.csv"

    # Open the file in write mode
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        # Write each row to the CSV file
        writer.writerows(end_results)

    print(f"Data written to {filename}")