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
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import matplotlib.mlab as mlab


def detect_anomalies(temp_data):
    room_names = ['class1', 'office', 'lab1']
    x,y = temp.data.shape
    #Iterate through columns
    for i in range(y):
        column = temp_data[:,i]
        #Find mean and standard deviation
        mean = np.nanmean(column)
        std = np.nanstd(column)
        #Find any values that are 1.5 STD's from the mean
        anomalies = column[abs(column-mean) > 1.5 * std]
        print("Anomalies detected in room " + room_names[i] + ": ")
        print(anomalies)


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

    #Slice the 3D numpy array
    temp = darray[0]
    occup = darray[1]
    co2 = darray[2]

    #Calculate and display statistics for temp and occup
    print("Temp Var = " + str(np.nanvar(temp)))
    print("Temp Median = " + str(np.nanmedian(temp)))

    print("Occupancy Variance= " + str(np.nanvar(occup)))
    print("Occupancy Median = " + str(np.nanmedian(occup)))

    #Display histograms
    for k in [temp, occup, co2]:
        #Make sure each bin is width 1 so the cumulative probability is ~= 1
        bins = np.arange(np.floor(k[~np.isnan(k)].min()),np.ceil(k[~np.isnan(k)].max()))
        p,x = np.histogram(k[~np.isnan(k)],bins, density = True)
        center = (x[:-1] + x[1:]) / 2
        plt.figure()
        plt.bar(center, p, align='center')


    #probability distribution function of time intervals     
    time = data['temperature'].index
    differences = np.diff(time.values).astype(np.int64) // 1000000000

    bins = np.arange(np.floor(differences.min()),np.ceil(differences.max()))
    p,x = np.histogram(differences,bins, density = True)
    center = (x[:-1] + x[1:]) / 2

    plt.figure()
    plt.bar(center, p, align='center')
    #plt.hist(differences)
    print("Mean of Intervals = " + str(differences.mean()))
    print("Variance of Intervals = " + str(differences.var()))


    detect_anomalies(temp)
    plt.show()


