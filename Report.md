# Sensor Mini Project

Authors: Sean Nemtzow and Austin Negron

Date: 2020-09-09
-----

## Summary
This project focuses on the integration and analysis of internet-based sensors. It serves as an introduction to Python, web-based data transfer, and simple data analysis.  
To simulate the sensors, a server and its clients are locally-hosted. The server maintains the client connections and the clients output the received timestamped messages about the occupancy, temperature, and CO2 level of rooms in a building.


## Task 0
The client outputs json-formatted messages like the following:  
`{"class1": {"time": "2020-09-09T16:24:40.498528", "temperature": [26.991743538688336], "occupancy": [19], "co2": [28.24985548185597]}}` 

The server issues the following greeting string to the client when intially connected:
`ECE Senior Capstone IoT simulator`

## Task 1

<<<<<<< HEAD
Add Python code to Websockets client that saves the JSON data to a text file as it comes in (message by message)

		for i in range(max_packets):
            data = await websocket.recv()
            log.write(data)
            log.write("\n")
            log.flush()
            if i % 5 == 0:
                pass
                # print(f"{i} total messages received")
            print(data)
        log.close()


To save the data to a file:
	
	python -m sp_iotsim.client -l "log.txt"

To analyze the data:

	python analyze.py "log.txt"


#Task 2
=======
## Task 2
>>>>>>> 9fb2d41522fae101efa3adf50729bfe8067cb529

A key part of the sensor anaylyzer is finding the basic statistics to then be able to provide a baseline for analomy detection. 

The following statistics are for classroom 1:


![](temp.png)
Temp Var = 58.65
Temp Median = 26.99

![](occupancy.png)
Occupancy Variance = 17.37
Occupancy Median = 19.00

![](class1.png)

![](time.png)
Time Interval Mean = 0.58
Time Interval Variance = 0.94

These probability distribution functions are calculated by plotting a histogram of the data and normalizing so that the data sums to 100%. We were able to accomplish this by calling the Numpy functions and learning how to not take the nan values into account.



## Task 3

a We determined an "anomoly" to be any data point that is 1.5 standard deviation or more from the mean. 

Using this guideline, we found that 1.99% of the data was consiered to be an anomaly. 


After filtering the data, we realized the new median was 26.99, relatively the same as our previous median. However, the new variance was 2.38, quite the difference from our original variance of 58.65.

b No, a persistent change in temperaure doesn't always indicate a failed sensor because the room could be heating or cooling. However, we do expect the data to follow a similar distribution.

c Possible bounds of temperature for each room type include:

	Lab 1: Mininmum value is 17.67 and maximum value is 24.40.

	Classroom 1: Mininmum value is 15.61 and maximum value is 38.59.

	Office: Mininmum value is 9.28 and maximum value is 37.0.



#Task 4 - Conclusions

a This is reflective of the real world because it is very common for smart systems to be aggregating metrics to a centralized server for further analysis. The packet format seems reasomnable, however the downside is that the monitoring is offline, when usually anomaly detection will take place in real time. Ultimately, this is very beneficial to us as humans because it helps us make sense of the world around us and these technology tools help us understand ourselves than if we didn't have these tools accesible to us. 

b The simulation is deficient because, as stated in part a, it is using offline data instead of real-time data. Because our similation was only for a short period of time, as opposed to constantly tracking the different temperatures throughout the day, the similar doesn't capture the cylces of the day. For example, occupancy will change upon class schedules. Temperature will be colder during the night and warmer during the day. Having access to this real-time data would comfortably give us the most accurate mean and variance. 

c We were surprised with how quickly we were able to understand these websockets. We are grateful that a good amount of it was pre-coded for us, which allows us to make sense of what was going on and then built on top of that. Generally, python is more forgiving as a quick scripting language becuase it isn't essential to define variables and compile. As opposed to C++ which is much more involved in relation to those aspects. 

d The sensors should reach out to the servers when there is data for efficiency purposes. Otherwise, the servers would constantly be reaching out to the sensors, regardless of is there was data at a given time or not, thus causing more inefficiencies in the system. 
-----
