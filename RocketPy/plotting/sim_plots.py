from matplotlib import *
import numpy as np
import matplotlib.pyplot as plt

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