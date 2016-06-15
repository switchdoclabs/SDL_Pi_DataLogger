#
# read and interpret AirQualitySensor
# SwitchDoc Labs April 2016
#

import time


def readAirQualitySensor(ads1115):

	# Select the gain
	gain = 6144  # +/- 6.144V

	# Select the sample rate
	sps = 250  # 250 samples per second


	sensor_value = ads1115.readRAW_ADCSingleEnded(0, gain, sps)

	return sensor_value


def interpretAirQualitySensor(sensor_value):
	

	value = ""
	returnValue = -1

  	if (sensor_value > 11200):
  
    		value = "Very High Pollution Detected"
    		returnValue= 0;
  
	if (sensor_value > 6400):
  
    		value = "High Pollution"
    	 	returnValue= 1;
  
	if (sensor_value > 4800):
  
    		value = "Medium Pollution"
    		returnValue= 2 

	if (sensor_value > 3200):
  
    		value = "Low Pollution"
    		returnValue= 3
  	else:
    		value = "Fresh Air"
    		returnValue= 4

	atuple = (value, returnValue)
	return  list(atuple)



