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
from SLUIRP.data import *
from SLUIRP.plotting import *
from SLUIRP.simulation import *



vdf_data = get_standard_data("CSV_files/VDF_Flight.csv")

vdf_data[0] = vdf_data[0] #- #vdf_data[0][0]
i=0
thrust = []
airfoilLift = []
for i in np.linspace(-10,10, 200):
    airfoilLift.append((i, i * 10))

airfoilLift = np.array(airfoilLift) 


angles = [4, 5, 7.5, 7.5, 10]
speeds = [1, 5  , 10, 15, 20]
env = rp.Environment(latitude = 40.505404, longitude = -87.019832, elevation=187)
    #URL = "http://weather.uwyo.edu/cgi-bin/sound   ing?region=naconf&TYPE=TEXT%3ALIST&YEAR=2024&MONTH=04&FROM=1300&TO=1312&STNM=72230"
env.set_date((2024, 4, 13, 6))
env.set_atmospheric_model(
    type="custom_atmosphere",
    wind_u = [(0, 10*0.44704 ), (5000, 10*0.44704)],
    wind_v = [(0, 0), (5000, 0)],
    pressure=None,
    temperature=None)


#compare_sim_real(vdf_data, env, 3, "VDF Flight")
#graph_thrust()
multi_sim(angles, speeds)
#graph_OR()
#testFlight.plots.trajectory_3d()
#testFlight.plots.all()
#testFlight.plots.aerodynamic_forces()
#testFlight.prints.all()
#print(wolf.center_of_mass())


#param_graph(time, alt, vel, accel, 7.4 , 3, "OpenRocket")