#!/usr/bin/env python
# Datalogger.py
# Gather Data, put in SQL, Graph with MatPlot Lib 
# SwitchDoc Labs
# 05/31/2016
# Version 1.1 6/15/2016
#
# supports:
# INA3221 - 3 Channel Current / Voltage Measurement Device
# ADS1115 - 4 Channel 16bit ADC
# OURWEATHER - OurWeather Complete Weather Kit 

# configuration variables
# set to true if present, false if not

INA3221_Present = False
ADS1115_Present = False
OURWEATHER_Present = True

# imports

import MySQLdb as mdb

import os

import sys
import time
from datetime import datetime
import random 

if INA3221_Present:
	import SDL_Pi_INA3221
	import INA3221Functions

if ADS1115_Present:
	from MADS1x15 import ADS1x15 
	import ADS1115Functions

if OURWEATHER_Present:
	import OURWEATHERFunctions





from datetime import timedelta



from apscheduler.schedulers.background import BackgroundScheduler

# constant defines

#How often in seconds to sample Data
#SampleTime = 1.0
SampleTime = 60.0
#How long in seconds to sample Data
LengthSample = 600000
#When to generate graph (every how many minutes) 
GraphRefresh = 2.0
#GraphRefresh = 10.0
#How many samples to Grah
GraphSampleCount =2880 


#mysql Password
password = 'password'
#mysql Table Name





# Main Program

print ""
print "SDL_Pi_Datalogger"
print ""
print " Will work with the INA3221 SwitchDoc Labs Breakout Board"
print " Will work with the ADS1115 SwitchDoc Labs Breakout Board"
print " Will work with OurWeather - Complete Weather Kit" 
print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
print ""

if ADS1115_Present:
	# Initialise the ADC using the default mode (use default I2C address)
	ADS1115 = 0x01	# 16-bit ADC
	ads1115 = ADS1x15(ic=ADS1115)

filename = time.strftime("%Y-%m-%d%H:%M:%SRTCTest") + ".txt"
starttime = datetime.utcnow()



# setup apscheduler

def tick():
    print('Tick! The time is: %s' % datetime.now()) 


def killLogger():
    scheduler.shutdown()
    print "Scheduler Shutdown...."
    exit() 

def doAllGraphs():
    if INA3221_Present:
    	INA3221Functions.buildINA3221Graph(password, GraphSampleCount)

    if ADS1115_Present:
    	ADS1115Functions.buildADS1115Graph(password, GraphSampleCount)

    if OURWEATHER_Present:
    	OURWEATHERFunctions.buildOURWEATHERGraphTemperature(password, GraphSampleCount)
    	OURWEATHERFunctions.buildOURWEATHERGraphWind(password, GraphSampleCount)



if __name__ == '__main__':

    scheduler = BackgroundScheduler()


    if INA3221_Present:
	scheduler.add_job(INA3221Functions.readINA3221Data, 'interval', seconds=SampleTime, args=[password])

    if ADS1115_Present:
	scheduler.add_job(ADS1115Functions.readADS1115Data, 'interval', seconds=SampleTime, args=[password])

    if OURWEATHER_Present:
	scheduler.add_job(OURWEATHERFunctions.readOURWEATHERData, 'interval', seconds=SampleTime, args=[password])

    minuteCron = "*/"+str(int(GraphRefresh))
    scheduler.add_job(doAllGraphs, 'cron', minute=minuteCron )


    scheduler.add_job(killLogger, 'interval', seconds=LengthSample)
    scheduler.add_job(tick, 'interval', seconds=60)
    scheduler.start()
    scheduler.print_jobs()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))


    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()









