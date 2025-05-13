import pandas
import numpy as np
import csv

def get_standard_data(csv_file):
    df1 = pandas.read_csv(csv_file, index_col=None)
    time = np.array(df1[df1.columns[0]].tolist())
    alt = np.array(df1[df1.columns[1]].tolist())
    vel = np.array(df1[df1.columns[2]].tolist())
    accel = np.array(df1[df1.columns[3]].tolist())
    return([time, alt, vel, accel])