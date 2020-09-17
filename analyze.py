#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
import math
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

#Function to determine data points larger than 1.5 std's from data mean
def detect_anomalies(temp_data, temp_var):
    print("Detecting anomalies and removing from temperature data\n")
    length  = np.count_nonzero(~np.isnan(temp_data))
    mean = np.nanmean(temp_data)
    std = math.sqrt(temp_var)
    #Find any values that are 1.5 STD's from the mean and discard them
    print("Max allowable value: %.2f\n" %((1.5 * std) + mean))
    print("Min allowable value: %.2f\n" %(mean-(1.5 * std)))
    temp_reduced = temp_data[~(abs(temp_data-mean) > (1.5 * std))]
    new_length = np.count_nonzero(~np.isnan(temp_reduced))
    percent = ((length - new_length)/ length) * 100
    print("%.2f%% of data was bad" %(percent))

    new_median = np.nanmedian(temp_reduced)
    new_var = np.nanvar(temp_reduced)

    print("New median is %.2f and new variance is %.2f" %(new_median, new_var))


def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)
    darray=np.array(list(data.values()))
    print(data)

    #Slice the 3D numpy array
    temp = darray[0][:,1]
    occup = darray[1][:,1]
    co2 = darray[2][:,1]

    #Calculate and display statistics for temp and occup
    temp_var = np.nanvar(temp)
    print("The following statistics are for room lab1:\n")
    print("Temp Var = " + str(temp_var))
    print("Temp Median = " + str(np.nanmedian(temp)) + "\n")

    print("Occupancy Variance = " + str(np.nanvar(occup)))
    print("Occupancy Median = " + str(np.nanmedian(occup)) + "\n")

    #Display histograms
    for k in [[temp, "Temperature"], [occup, "Occupancy"], [co2, "CO2"]]:
        #Make sure each bin is width 1 so the cumulative probability is ~= 1
        sensor = k[0][~np.isnan(k[0])]
        bins = np.arange(np.floor(sensor.min()),np.ceil(sensor.max()))
        p,x = np.histogram(sensor,bins, density = True)
        center = (x[:-1] + x[1:]) / 2
        plt.figure()
        plt.bar(center, p, align='center')
        plt.ylabel('Probability')
        plt.xlabel('Sensor Value')
        plt.title(k[1] + " Sensor PDF of Class1")


    #probability distribution function of time intervals     
    time = data['temperature'].index
    differences = np.diff(time.values).astype(np.int64) // 1000000000

    bins = np.arange(np.floor(differences.min()),np.ceil(differences.max()))
    p,x = np.histogram(differences,bins, density = True)
    center = (x[:-1] + x[1:]) / 2

    plt.figure()
    plt.bar(center, p, align='center')
    plt.ylabel('Probability')
    plt.xlabel('Time between messages (Seconds)')
    plt.title('Time Interval')
    print("Time Interval Mean = " + str(differences.mean()))
    print("Time Interval Variance = " + str(differences.var()) + "\n")

    detect_anomalies(temp, temp_var)
    plt.show()


