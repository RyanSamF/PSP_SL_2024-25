import matplotlib.pyplot as plt
import numpy as np

def CD_estimate(time, vel, accel, density, area):
    est_CD = (2* (abs(accel + 9.86) ) * 12.06556)/ (density * area * (vel) ** 2)
    est_CD = np.clip(est_CD, -1, 1)
    plt.plot(time, est_CD)
    plt.show()
    
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth