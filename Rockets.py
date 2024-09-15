from rocketpy import *
from matplotlib import *
import datetime
import numpy as np
import pandas


thrusturl = 'https://raw.githubusercontent.com/RyanSamF/PSP_SL_2024-25/main/exodusthrustcurve.csv'
df = pandas.read_csv(thrusturl, index_col=None)
print(df[df.columns[0]].tolist())
print(df[df.columns[1]].tolist())
"""
env = Environment(latitude = 34.894616, longitude = -86.616947)
#URL = "http://weather.uwyo.edu/cgi-bin/sound   ing?region=naconf&TYPE=TEXT%3ALIST&YEAR=2024&MONTH=04&FROM=1300&TO=1312&STNM=72230"
env.set_date(
    (2024, 4, 13, 6))
#env.set_atmospheric_model(type ="wyoming_sounding", file = URL)
#env.set_atmospheric_model(type = "Windy", file="")
env.set_atmospheric_model(type="standard_atmosphere")
env.info()
#env.plots.all()
airfoilLift = []
for i in np.linspace(-10,10, 200):
    airfoilLift.append((i, i * 10))

airfoilLift = np.array(airfoilLift)

l1482 = GenericMotor(
    coordinate_system_orientation= "nozzle_to_combustion_chamber",
    thrust_source = "https://raw.githubusercontent.com/RyanSamF/PSP_SL_2024-25/main/testCurve.csv",
    dry_mass = 4.2 - 1.878, #kg
    propellant_initial_mass = 1.878, #kg
    center_of_dry_mass_position = 9.764 / 39.37, #in -> m
    #dry_inertia = (1.22 / 4.882, 1.22 / 4.882, 0.042 / 4.882),
    chamber_radius= 35.05 / 1000, #mm to meters
    chamber_height = 15.75 / 39.37, #in to meters
    chamber_position = (19.625 / 39.37) / 2,
    nozzle_radius = 0.625 / 39.37,
    burn_time = None
)

exodus = Rocket(
    radius = 2.575 / 39.37, #radius in -> meters
    mass = (34.4903 / 2.2046), #mass lbs -> kg
    inertia = (186.28 / 4.882 , 186.28 / 4.882, 1.56 / 4.882), #inertia lbs/ft^2 -> kg/m^2
    power_off_drag = "..\\RasCurve.csv", 
    power_on_drag = "..\\RasCurve.csv",
    coordinate_system_orientation = "nose_to_tail",
    center_of_mass_without_motor = 45.967 / 39.37
)
exodus.add_motor( l1482, 92.5 / 39.37)

nose_cone = exodus.add_nose(
    length = 11 / 39.37,
    kind = "von karman",
    position = 0
)

fin_set = exodus.add_trapezoidal_fins(
    n = 3,
    root_chord = 9.9 / 39.37, 
    tip_chord = 3.8 / 39.37,
    position = 82.6 / 39.37,
    span = 6.7 / 39.37,
    sweep_length = 3.7 / 39.37,
    airfoil = (airfoilLift, "degrees")
)
#main = exodus.add_parachute(
    #name = "main",
    #cd_s = 11.674,
    #trigger = 213.36
#)
drogue = exodus.add_parachute(
    name = "drogue",
    cd_s = 0.291,
    trigger = "apogee"
)
testFlight = Flight(
    rocket = exodus, environment = env, rail_length = 3.6576, inclination = 85  , heading = 130 + 180
)

#exodus.draw()
#testFlight.plots.trajectory_3d()
testFlight.plots.all()
#testFlight.plots.aerodynamic_forces()
testFlight.prints.all()
print((testFlight.apogee - env.elevation) * 3.28084)
print((testFlight.apogee - env.elevation))
"""