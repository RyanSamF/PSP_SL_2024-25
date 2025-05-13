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
    ax1.legend(lns, labs, loc=1)
    ax1_ylims = ax1.axes.get_ylim()          
    ax1_yratio = ax1_ylims[0] / ax1_ylims[1]  

    ax2_ylims = ax2.axes.get_ylim()           
    ax2_yratio = ax2_ylims[0] / ax2_ylims[1] 

    if ax1_yratio < ax2_yratio: 
        ax2.set_ylim(bottom = ax2_ylims[1]*ax1_yratio)
    else:
        ax1.set_ylim(bottom = ax1_ylims[1]*ax2_yratio)
    plt.suptitle(program1 + " Vs. " + program2 + " Parameters vs. Time",
                fontweight = 'bold')
    plot_name = str(ws)+" mph " + str(angle) + " Degrees"
    plt.xlim((0, max(time1[-1],time2[-1])))
    plt.title(plot_name)
    plt.show()
    plt.savefig('Plots/' + "compare" + program1 + program2 + " Parameters.png", format='png')

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

def compare_sim_real(vdf_data, env, aoa, flight_name):
    testFlight   = rp.Flight(
                rocket = wolf, environment = env, rail_length = 3.6576, inclination = 90 - aoa  , heading = 270)
    time = testFlight.time
    alt = testFlight.altitude(time) * feet2meters
    accel = testFlight.az(time) * feet2meters
    vel = testFlight.vz(time) * feet2meters

    vdf_data [1] *= feet2meters
    vdf_data[2] *= feet2meters
    vdf_data[3] *= feet2meters


    compare_graph([time, alt, vel, accel], vdf_data, 10, 3, "RocketPy", flight_name)


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