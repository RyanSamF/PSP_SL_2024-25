from rocketpy import *
from matplotlib import *
import datetime
import numpy as np
import pandas
import yaml
import math
import matplotlib.pyplot as plt


angles = [5, 5, 7.5, 7.5, 10]
speeds = [0, 5, 10, 15, 20]
speeds_ms = [x * 0.44704 for x in speeds]

with open('wolf_config.yaml', 'r') as file:
    data = yaml.safe_load(file)

files_data = data["githubfiles"]
motor_data = data["motor"]
rocket_data = data["rocket"]
nose_data = data["nose_cone"]
fins_data = data["fins"]
parachutes_data = data["parachutes"]

thrusturl = files_data["thrusturl"]

df = pandas.read_csv(thrusturl, index_col=None)
time_thrust = np.array(df[df.columns[0]].tolist())
thrust = np.array(df[df.columns[1]].tolist())
thrust_array = np.stack([time_thrust, thrust], 1)

dragurl = files_data["dragurl"]
df = pandas.read_csv(dragurl, index_col=None)
time_drag = np.array(df[df.columns[0]].tolist())
drag = np.array(df[df.columns[1]].tolist())
drag_array = np.stack([time_drag, drag], 1)


#env.set_atmospheric_model(type ="wyoming_sounding", file = URL)
#env.set_atmospheric_model(type = "Windy", file="")
env_arr = []
for wind_speed in speeds_ms:
    env = Environment(latitude = 34.894616, longitude = -86.616947)
    #URL = "http://weather.uwyo.edu/cgi-bin/sound   ing?region=naconf&TYPE=TEXT%3ALIST&YEAR=2024&MONTH=04&FROM=1300&TO=1312&STNM=72230"
    env.set_date((2024, 4, 13, 6))
    env.set_atmospheric_model(
        type="custom_atmosphere",
        wind_u = [(0, wind_speed), (2000, wind_speed)],
        wind_v = [(0, 0), (2000, 0)]
                          )
    env_arr.append(env)
#env.info()
#env.plots.all()
airfoilLift = []
for i in np.linspace(-10,10, 200):
    airfoilLift.append((i, i * 10))

airfoilLift = np.array(airfoilLift) 

l1482 = GenericMotor(
    coordinate_system_orientation= "nozzle_to_combustion_chamber",
    thrust_source = thrust_array,
    dry_mass = (motor_data["net_mass"] - motor_data["prop_mass"]) * 0.4536, #lbs -> kg
    propellant_initial_mass = motor_data["prop_mass"] * 0.4536, #kg
    center_of_dry_mass_position = motor_data["center_of_dry_mass"] / 39.37, #in -> m
    #dry_inertia = (1.22 / 4.882, 1.22 / 4.882, 0.042 / 4.882),
    chamber_radius= motor_data["chamber_rad"] /39.37  ,#in to meters
    chamber_height = motor_data["chamber_height"] / 39.37, #in to meters
    chamber_position = motor_data["chamber_pos"] / 39.37, #in to meters
    nozzle_radius = motor_data["nozzle_rad"] / 39.37, #in to meters
    burn_time = None
)

wolf = Rocket(
    radius = rocket_data["radius"] / 39.37, #radius in -> meters
    mass = (rocket_data["mass"] / 2.2046), #mass lbs -> kg
    inertia = rocket_data["inertia"], #inertia lbs/ft^2 -> kg/m^2
    power_off_drag = drag_array,
    power_on_drag = drag_array,
    coordinate_system_orientation = "nose_to_tail",
    center_of_mass_without_motor = rocket_data["COM"] / 39.37 #in -> meters
)
wolf.add_motor( l1482, 92.5 / 39.37) #position of motor in rocket

nose_cone = wolf.add_nose(
    length = nose_data["length"] / 39.37,
    kind = "von karman",
    position = 0
)

fin_set = wolf.add_trapezoidal_fins(
    n = fins_data["n"], #number of fins
    root_chord = fins_data["root_chord"] / 39.37, #in -> meters
    tip_chord = fins_data["tip_chord"] / 39.37, #in -> meters
    position = fins_data["position"] / 39.37, #in -> meters
    span = fins_data["span"] / 39.37, #in -> meters
    sweep_length = 3.7 / 39.37,
    airfoil = (airfoilLift, "degrees")
)
main = wolf.add_parachute(
    name = "main",
    cd_s = parachutes_data["main_cd"] * (parachutes_data["main_diameter"] / 2 / 39.37) ** 2 * math.pi,
    trigger = parachutes_data["main_trigger"] / 3.281 #altitude of main deployment ft -> meters
)
drogue = wolf.add_parachute(
    name = "drogue",
    cd_s = parachutes_data["drogue_cd"] * (parachutes_data["drogue_diameter"] / 2 / 39.37) ** 2 * math.pi,
    trigger = "apogee"
)
for i in range(0,1):
    testFlight   = Flight(
        rocket = wolf, environment = env_arr[i], rail_length = 3.6576, inclination = 90 - angles[i]  , heading = 270)
    print((testFlight.apogee - env.elevation) * 3.28084)
    print((testFlight.apogee - env.elevation))
    alt = []
    accel = []
    vel = []
    time = testFlight.time
    for index in time:
        alt.append(testFlight.altitude(index) * 3.28084)
        accel.append(testFlight.az(index) * 3.28084 )
        vel.append(testFlight.vz(index) *  3.28084)
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('Acceleration (ft/s²), Velocity (ft/s)')
    lns1 = ax1.plot(time, accel, color=(1,0,0), label="Acceleration")
    lns2 = ax1.plot(time, vel, color=(0.9290, 0.6940, 0.1250), label="Velocity")
    
    ax2 = ax1.twinx()
    ax2.set_ylabel("Altitude (ft)")
    lns3 = ax2.plot(time, alt, color=(0, 0, 1),label="Altitude")
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)

    plt.suptitle("Flight Parameters against Time",
                fontweight = 'bold')
    plt.title(str(speeds[i])+" mph " + str(angles[i]) + " Degrees")
    plt.show()
    
    ke_ = 0.5 * vel[-1] ** 2 *  #Kinetic energy at landing in Newtons
    stability = testFlight.stability_margin(testFlight.out_of_rail_time)
    print(stability)

#wolf.draw()
#testFlight.plots.trajectory_3d()
#testFlight.plots.all()
#testFlight.plots.aerodynamic_forces()
#testFlight.prints.all()


    