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

feet2meters = 3.28084
in2meters = 1 / 39.37
lbs2kg = 0.4536

with open('ConfigFiles/VDF_config.yaml', 'r') as file:
    data = yaml.safe_load(file)

files_data = data["githubfiles"]
motor_data = data["motor"]
rocket_data = data["rocket"]
nose_data = data["nose_cone"]
fins_data = data["fins"]
parachutes_data = data["parachutes"]

thrusturl = files_data["thrusturl"]
boostermass = rocket_data["booster"]
avionicsmass = rocket_data["midsec"]
nosemass = rocket_data["uppersec"]
#df = pandas.read_csv(thrusturl, index_col=None)
#time_thrust = np.array(df[df.columns[0]].tolist())
#thrust = np.array(df[df.columns[1]].tolist())
#thrust_array = np.stack([time_thrust, thrust], 1)
#thrust_array = "CSV_files/Wolf_thrust.csv"
m_heav = rocket_data["h_section"]
dragurl = files_data["dragurl"]
#df = pandas.read_csv(dragurl, index_col=None)
#time_drag = np.array(df[df.columns[0]].tolist())
#drag = np.array(df[df.columns[1]].tolist())
#drag_array = np.stack([time_drag, drag], 1)

## REAL




#env.info()
#env.plots.all()
airfoilLift = []
for i in np.linspace(-10,10, 200):
    airfoilLift.append((i, i * 10))

airfoilLift = np.array(airfoilLift) 

L930 = rp.GenericMotor(
    coordinate_system_orientation= "nozzle_to_combustion_chamber",
    thrust_source = thrusturl,
    dry_mass = (motor_data["net_mass"] - motor_data["prop_mass"]) * lbs2kg, #lbs -> kg
    propellant_initial_mass = motor_data["prop_mass"] * lbs2kg, #lbs -> kg
    #center_of_dry_mass_position = motor_data["center_of_dry_mass"] / 39.37, #in -> m
    #dry_inertia = (1.22 / 4.882, 1.22 / 4.882, 0.042 / 4.882),
    chamber_radius= motor_data["chamber_rad"] * in2meters ,#in to meters    
    chamber_height = motor_data["chamber_height"] * in2meters, #in to meters
    chamber_position = motor_data["center_of_dry_mass"] * in2meters, #in to meters
    nozzle_radius = motor_data["nozzle_rad"] * in2meters, #in to meters
    burn_time = None
)

wolf = rp.Rocket(
    radius = rocket_data["radius"] * in2meters, #radius in -> meters
    mass = (rocket_data["mass"] * lbs2kg), #mass lbs -> kg
    inertia = np.array(rocket_data["inertia"]) * lbs2kg / feet2meters**2, #inertia lbs/ft^2 -> kg/m^2
    power_off_drag = dragurl,
    power_on_drag = dragurl,
    coordinate_system_orientation = "nose_to_tail",
    center_of_mass_without_motor = rocket_data["COM"] * in2meters #in -> meters
)
wolf.add_motor( L930, rocket_data["length"] * in2meters) #position of motor in rocket

nose_cone = wolf.add_nose(
    length = nose_data["length"] * in2meters,
    kind = "von karman",
    position = 0
)

fin_set = wolf.add_trapezoidal_fins(
    n = fins_data["n"], #number of fins
    root_chord = fins_data["root_chord"] * in2meters, #in -> meters
    tip_chord = fins_data["tip_chord"] * in2meters, #in -> meters
    position = (rocket_data["length"] - fins_data["root_chord"]) * in2meters, #in -> meters
    span = fins_data["span"] * in2meters, #in -> meters
    sweep_length = fins_data["sweep"] * in2meters,
    #   airfoil = (airfoilLift, "degrees")
)
if parachutes_data["main_present"]:
    main = wolf.add_parachute(
        name = "main",
        cd_s = parachutes_data["main_cd"] * (parachutes_data["main_diameter"] / 2 * in2meters) ** 2 * math.pi,
        trigger = parachutes_data["main_trigger"] / 3.281, #altitude of main deployment ft -> meters
        #lag = 0.5
    )
if parachutes_data["drogue_present"]:
    drogue = wolf.add_parachute(
        name = "drogue",
        lag = 0,
        cd_s = parachutes_data["drogue_cd"] * (parachutes_data["drogue_diameter"] / 2 * in2meters) ** 2 * math.pi,
        trigger = "apogee"
    )
#wolf.draw()

def prof_graph(drift, alt, plt_title):
    fig, ax1 = plt.subplots()
    ax1.set_ylabel("Altitude (ft)")
    ax1.set_xlabel('Drift Distance (ft)')
    lns3 = ax1.plot(drift, alt, color=(0, 0, 1))
    plt.suptitle("Flight Profile",
        fontweight = 'bold')
    plt.title(plt_title)
    plt.grid()
    plt.savefig('Plots/' + plt_title + " Profile.png", format='png')
    
def compare_graph(params1, params2, ws, angle, program1, program2):
    time1 = params1[0]
    alt1 = params1[1]
    vel1 = params1[2]
    accel1 = params1[3]
    time2 = params2[0]
    alt2 = params2[1]
    vel2 = params2[2]
    accel2 = params2[3]

    fig, ax1 = plt.subplots()
    plt.grid()
    ax1.set_ylabel("Altitude (ft)")
    ax1.set_xlabel('time (s)')
    lns3 = ax1.plot(time1, alt1, color=(0, 0, 1),label="Altitude (" + program1 + ")", alpha = 0.8)
    lns6 = ax1.plot(time2, alt2, color=(1, 0, 0),label="Altitude (" + program2 + ")", alpha = 0.8)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Acceleration (ft/s²), Velocity (ft/s)')
    lns1 = ax2.plot(time1, accel1, color=(0, 0.6, 1), label="Acceleration (" + program1 + ")",alpha = 0.8)
    lns2 = ax2.plot(time1, vel1, color=(0.5,0.8,0.95), label="Velocity (" + program1 + ")",alpha = 0.8)
    lns4 = ax2.plot(time2, accel2, color=(0.85, 0.4, 0.2), label="Acceleration (" + program2 + ")",alpha = 0.8)
    lns5 = ax2.plot(time2, vel2, color=(1,0.6,0), label="Velocity (" + program2 + ")",alpha = 0.8)
    lns = lns1+lns2+lns3+lns4+lns5+lns6
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=4)
    ax1_ylims = ax1.axes.get_ylim()          
    ax1_yratio = ax1_ylims[0] / ax1_ylims[1]  

    ax2_ylims = ax2.axes.get_ylim()           
    ax2_yratio = ax2_ylims[0] / ax2_ylims[1] 

    if ax1_yratio < ax2_yratio: 
        ax2.set_ylim(bottom = ax2_ylims[1]*ax1_yratio)
    else:
        ax1.set_ylim(bottom = ax1_ylims[1]*ax2_yratio)
    plt.suptitle(program1 + " and " + program2 + " Flight Parameters vs. Time",
                fontweight = 'bold')
    plot_name = str(ws)+" mph " + str(angle) + " Degrees"
    plt.xlim((0, time[-1]))
    plt.title(plot_name)
    
    plt.savefig('Plots/' + plot_name +  program1 + program2 + " Parameters.png", format='png')

def param_graph(time, alt, vel, accel, ws, angle, program):
    fig, ax1 = plt.subplots()
    plt.grid()
    ax1.set_ylabel("Altitude (ft)")
    ax1.set_xlabel('time (s)')
    lns3 = ax1.plot(time, alt, color=(0, 0, 1),label="Altitude")
    ax2 = ax1.twinx()
    ax2.set_ylabel('Acceleration (ft/s²), Velocity (ft/s)')
    lns1 = ax2.plot(time, accel, color=(0.9290, 0.6940, 0.1250), label="Acceleration")
    lns2 = ax2.plot(time, vel, color=(1,0,0), label="Velocity")
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
    ax1_ylims = ax1.axes.get_ylim()          
    ax1_yratio = ax1_ylims[0] / ax1_ylims[1]  

    ax2_ylims = ax2.axes.get_ylim()           
    ax2_yratio = ax2_ylims[0] / ax2_ylims[1] 

    if ax1_yratio < ax2_yratio: 
        ax2.set_ylim(bottom = ax2_ylims[1]*ax1_yratio)
    else:
        ax1.set_ylim(bottom = ax1_ylims[1]*ax2_yratio)
    plt.suptitle(program + " Flight Parameters vs. Time",
                fontweight = 'bold')
    plot_name = str(ws)+" mph " + str(angle) + " Degrees"
    plt.xlim((0, time[-1]))
    plt.title(plot_name)
    
    plt.savefig('Plots/' + plot_name +  program + " Parameters.png", format='png')
    return(plot_name)

def get_windy_env(env_time):
    env = rp.Environment(latitude = 40.505404, longitude = -87.019832,elevation=187)
        #URL = "http://weather.uwyo.edu/cgi-bin/sound   ing?region=naconf&TYPE=TEXT%3ALIST&YEAR=2024&MONTH=04&FROM=1300&TO=1312&STNM=72230"
    env.set_date(env_time)
    env.set_atmospheric_model(
        type="Windy",
        file="ICON"
    )
    #env.all_info()
    return(env)

def get_ST_env(wind_speed):
    env = rp.Environment(latitude = 40.505404, longitude = -87.019832, elevation=187)
        #URL = "http://weather.uwyo.edu/cgi-bin/sound   ing?region=naconf&TYPE=TEXT%3ALIST&YEAR=2024&MONTH=04&FROM=1300&TO=1312&STNM=72230"
    env.set_date((2024, 4, 13, 6))
    env.set_atmospheric_model(
        type="custom_atmosphere",
        wind_u = [(0, wind_speed), (5000, wind_speed)],
        wind_v = [(0, 0), (5000, 0)],
        pressure=None,
        temperature=None)
    return(env)
        

def multi_sim(angles, speeds):
    speeds_ms = [x * 0.44704 for x in speeds]
    env_arr = []
    time =  datetime.datetime(2025, 2, 23, 13, 30, 0, 0, tzinfo=ZoneInfo("America/Indianapolis"))
    for wind_speed in speeds_ms:
        env = get_ST_env(wind_speed)
        #env = get_windy_env(time)
        env_arr.append(env)
    final_vel = ["Final Velocity (ft/s)"]
    stability = ["Stability off rod (calibers)"]
    descent_time = ["Descent Time (seconds)"]
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
    for i in range(0,len(angles)):
        testFlight   = rp.Flight(
            rocket = wolf, environment = env_arr[i], rail_length = 3.6576, inclination = 90 - angles[i]  , heading = 270)
        alt = []
        accel = []
        vel = []
        mach_num = []
        drift = []
        time = testFlight.time
        vel_main_deploy = 0
        for index in time:
            alt.append(testFlight.altitude(index) * feet2meters)
            accel.append(testFlight.az(index) * feet2meters )
            vel.append(testFlight.vz(index) * feet2meters)
            mach_num.append(testFlight.mach_number(index))
            drift.append(-1 * testFlight.x(index) * feet2meters)
            if index == testFlight.apogee_time:
                apo_index = len(drift)
            if vel_main_deploy == 0 and alt[-1] <= main.trigger * 3.281 + 10 and vel[-1] < -1:
                vel_main_deploy = vel[-1]
                print("Under Drogue" + str(vel_main_deploy))
                time_main_deploy = index
                #print("alt:" + str(alt[-1]))
        plot_name = param_graph(time, alt, vel, accel, speeds[i], angles[i], "RocketPy")
        prof_graph(drift, alt, plot_name + " RocketPy")

        final_vel.append(vel[-1])
        stability.append(testFlight.stability_margin(testFlight.out_of_rail_time))
        descent_time.append(time[-1] - testFlight.apogee_time)
        apogee.append((testFlight.apogee - env.elevation) * feet2meters)
        distance.append(abs(drift[-1]-drift[apo_index]))
        run_params.append(plot_name)
        max_mach.append(max(mach_num))
        max_vel.append(max(vel))
        max_accel.append(max(accel))
        max_ke.append(0.5 * vel[-1] ** 2 * m_heav / 32.17)
        vel_at_main.append(vel_main_deploy)
        under_drogue.append(time_main_deploy - testFlight.apogee_time)
        #print("after" + str(time_main_deploy))
        under_main.append(time[-1] - time_main_deploy)
        #print("Velocity at Main Deployment:" + str(vel_main_deploy))
        #print(testFlight.out_of_rail_velocity * feet2meters)
        testFlight.plots.trajectory_3d()
    print(stability)
    print(wolf.cp_position(0) / in2meters)
    print(wolf.center_of_mass(0) / in2meters)    
    print(vel[-1])
    end_results = [run_params, 
        final_vel,
        descent_time,
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



def graph_OR():
    y = [['0','5'],['5','5'],['10','7.5'], ['15','7.5'], ['20','10']]
    for x in y:
        df = pandas.read_csv('CSV_files/' + x[0] + x[1].replace('.', '')+'.csv', index_col=None)
        time = np.array(df[df.columns[0]].tolist())
        alt = np.array(df[df.columns[1]].tolist())
        vel = np.array(df[df.columns[2]].tolist())
        accel = np.array(df[df.columns[3]].tolist())
        param_graph(time, alt, vel, accel, x[0], x[1], "OpenRocket")

def graph_thrust():
    df = pandas.read_csv(thrusturl, index_col=None)
    time = np.array(df[df.columns[0]].tolist())
    thrust = np.array(df[df.columns[1]].tolist())
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel('Thrust (lbf)')
    lns3 = ax1.plot(time, thrust * 0.2248, color=(0, 0, 1))
    plt.suptitle("Thrust Curve",
        fontweight = 'bold')
    plt.grid()
    plt.savefig('Plots/thrust.png', format='png')


#NOT WORKING YET    
def mc_sim(angle, wind_speed):
    env = rp.Environment(latitude = 20.6, longitude = -80.6)
    #URL = "http://weather.uwyo.edu/cgi-bin/sound   ing?region=naconf&TYPE=TEXT%3ALIST&YEAR=2024&MONTH=04&FROM=1300&TO=1312&STNM=72230"
    env.set_date((2024, 4, 13, 6))
    env.set_atmospheric_model(
        type="custom_atmosphere",
        wind_u = [(0, wind_speed), (5000, wind_speed)],
        wind_v = [(0, 0), (5000, 0)],
        pressure=None,
        temperature=None)
    s_wolf = rp.stochastic.StochasticRocket(wolf)
    s_env = rp.stochastic.StochasticEnvironment(environment = env, ensemble_member=list(range(env.num_ensemble_members)))
    testFlight   = rp.Flight(
            rocket = wolf, environment = env, rail_length = 3.6576, inclination = 90 - angle  , heading = 270)
    s_flight = rp.stochastic.StochasticFlight(testFlight)
    sim = rp.simulation.MonteCarlo("mc",s_env, s_wolf, s_flight)
    sim.simulate(100, False)
    sim.all_info()

#FUNCTION get_standard_data
#Takes CSV file with Time, Altitude, Velocity, and Acceleration data
#And formats it into an array for plotting.
def get_standard_data(csv_file):
    df1 = pandas.read_csv(csv_file, index_col=None)
    time = np.array(df1[df1.columns[0]].tolist())
    alt = np.array(df1[df1.columns[1]].tolist())
    vel = np.array(df1[df1.columns[2]].tolist())
    accel = np.array(df1[df1.columns[3]].tolist())
    return([time, alt, vel, accel])

print(rp.__file__)
filename = "output.csv"
# opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()
angles = [3, 5, 7.5, 7.5, 10]
speeds = [10, 5, 10, 15, 20]
multi_sim(angles, speeds)
#testFlight.plots.trajectory_3d()
#testFlight.plots.all()
#testFlight.plots.aerodynamic_forces()
#testFlight.prints.all()



#param_graph(time, alt, vel, accel, 7.4 , 3, "OpenRocket")