#!/usr/bin/env python
# Datalogger.py
# Gather Data, put in SQL, Graph with MatPlot Lib 
# SwitchDoc Labs
# 05/31/2016
# Version 3.0  March 25, 2018
#
# supports:
# CSVSensor
# INA3221 - 3 Channel Current / Voltage Measurement Device
# ADS1115 - 4 Channel 16bit ADC
# OURWEATHER - OurWeather Complete Weather Kit 
# Three Panel Test - 3 Solar Cells and 3 SunAirPlus boards 
# WXLink from SwitchDoc Labs


# configuration variables
# set to true if present, false if not

from __future__ import print_function
INA219_Present = False
INA3221_Present = True
ADS1115_Present = False
OURWEATHER_Present = False
ThreePanelTest_Present = False
WXLINK_Present = False

# imports

import pymysql as mdb

import os

import sys
import time
from datetime import datetime
import random 


if INA219_Present:
        
        import INA219Functions

if INA3221_Present:
        import SDL_Pi_INA3221
        import INA3221Functions

if ADS1115_Present:
        from MADS1x15 import ADS1x15 
        import ADS1115Functions

if OURWEATHER_Present:
        import OURWEATHERFunctions

if ThreePanelTest_Present:
        import ThreePanelTestFunctions

if WXLINK_Present:
        import WXLINKFunctions



from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler.events

# constant defines

#How often in seconds to sample Data
SampleTime = 0.05
#SampleTime = 60.0
#How long in seconds to sample Data
#LengthSample = 120
LengthSample = 120
#When to generate graph (every how many minutes) 
GraphRefresh = 1
#GraphRefresh = 10.0
#How many samples to Graph
GraphSampleCount = 2000 


#mysql user
username = "datalogger"
#mysql Password
password = 'password'
#mysql Table Name





# Main Program

print("")
print("SDL_Pi_Datalogger")
print("")
print(" Will work with the INA3221 SwitchDoc Labs Breakout Board")
print(" Will work with the ADS1115 SwitchDoc Labs Breakout Board")
print(" Will work with OurWeather - Complete Weather Kit" )
print(" Will work with SwitchDoc Labs WxLink Wireless LInk " )
print("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
print("")

if ADS1115_Present:
	# Initialise the ADC using the default mode (use default I2C address)
	ADS1115 = 0x01	# 16-bit ADC
	ads1115 = ADS1x15(ic=ADS1115)

filename = time.strftime("%Y-%m-%d%H:%M:%SRTCTest") + ".txt"
starttime = datetime.utcnow()



# setup apscheduler

def ap_my_listener(event):
        if event.exception:
              print(event.exception)
              print(event.traceback)



def tick():
    print('Tick! The time is: %s' % datetime.now()) 


def killLogger():
    scheduler.shutdown()
    print ("Scheduler Shutdown....")
    exit() 

def doAllGraphs():
    if INA219_Present:
    	INA219Functions.buildINA219Graph(username, password, GraphSampleCount)

    if INA3221_Present:
    	INA3221Functions.buildINA3221Graph(username, password, GraphSampleCount)

    if ADS1115_Present:
    	ADS1115Functions.buildADS1115Graph(username, password, GraphSampleCount,0)
    	ADS1115Functions.buildADS1115Graph(username, password, GraphSampleCount,1)
    	ADS1115Functions.buildADS1115Graph(username, password, GraphSampleCount,2)
    	ADS1115Functions.buildADS1115Graph(username, password, GraphSampleCount,3)

    if OURWEATHER_Present:
        OURWEATHERFunctions.buildOURWEATHERGraphTemperature(username, password, GraphSampleCount)
        OURWEATHERFunctions.buildOURWEATHERGraphWind(username, password, GraphSampleCount)
        OURWEATHERFunctions.buildOURWEATHERGraphSolarVoltage(username, password, GraphSampleCount)
        OURWEATHERFunctions.buildOURWEATHERGraphSolarCurrent(username, password, GraphSampleCount)

    if ThreePanelTest_Present:
    	ThreePanelTestFunctions.buildThreePanelTestGraphCurrent(username, password, GraphSampleCount)
    	ThreePanelTestFunctions.buildThreePanelTestGraphVoltage(username, password, GraphSampleCount)

    if WXLINK_Present:
    	WXLINKFunctions.buildWXLINKGraphSolar(username, password, GraphSampleCount)
    	WXLINKFunctions.buildWXLINKGraphSolarCurrent(username, password, GraphSampleCount)
    	WXLINKFunctions.buildWXLINKGraphSolarVoltage(username, password, GraphSampleCount)
    	WXLINKFunctions.buildWXLINKGraphSolarPower(username, password, GraphSampleCount)

if __name__ == '__main__':

    scheduler = BackgroundScheduler()

    scheduler.add_listener(ap_my_listener, apscheduler.events.EVENT_JOB_ERROR)

    # make sure functions work before scheduling - may remove when debugged

    if OURWEATHER_Present:
    	OURWEATHERFunctions.readOURWEATHERData(username, password)
    	OURWEATHERFunctions.buildOURWEATHERGraphTemperature(username, password, GraphSampleCount)
    	OURWEATHERFunctions.buildOURWEATHERGraphWind(username, password, GraphSampleCount)
    	OURWEATHERFunctions.buildOURWEATHERGraphSolarVoltage(username, password, GraphSampleCount)
    	OURWEATHERFunctions.buildOURWEATHERGraphSolarCurrent(username, password, GraphSampleCount)

    if WXLINK_Present:
    	WXLINKFunctions.readWXLINKData(username, password)
    	WXLINKFunctions.buildWXLINKGraphSolar(username, password, GraphSampleCount)
    	WXLINKFunctions.buildWXLINKGraphSolarCurrent(username, password, GraphSampleCount)
    	WXLINKFunctions.buildWXLINKGraphSolarVoltage(username, password, GraphSampleCount)
    	WXLINKFunctions.buildWXLINKGraphSolarPower(username, password, GraphSampleCount)

    if ThreePanelTest_Present:
    	ThreePanelTestFunctions.readThreePanelTestData(username, password)
    	ThreePanelTestFunctions.buildThreePanelTestGraphCurrent(username, password, GraphSampleCount)
    	ThreePanelTestFunctions.buildThreePanelTestGraphVoltage(username, password, GraphSampleCount)

    if ADS1115_Present:
        ADS1115Functions.readADS1115Data(username, password)	
        ADS1115Functions.buildADS1115Graph(username, password, GraphSampleCount,0)
        ADS1115Functions.buildADS1115Graph(username, password, GraphSampleCount,1)
        ADS1115Functions.buildADS1115Graph(username, password, GraphSampleCount,2)
        ADS1115Functions.buildADS1115Graph(username, password, GraphSampleCount,3)




    if INA219_Present:
        scheduler.add_job(INA219Functions.readINA219Data, 'interval', seconds=SampleTime, args=[username, password])

    if INA3221_Present:
        scheduler.add_job(INA3221Functions.readINA3221Data, 'interval', seconds=SampleTime, args=[username, password])

    if ADS1115_Present:
        scheduler.add_job(ADS1115Functions.readADS1115Data, 'interval', seconds=SampleTime, args=[username, password])

    if OURWEATHER_Present:
        scheduler.add_job(OURWEATHERFunctions.readOURWEATHERData, 'interval', seconds=SampleTime, args=[username, password])

    if ThreePanelTest_Present:
        scheduler.add_job(ThreePanelTestFunctions.readThreePanelTestData, 'interval', seconds=SampleTime, args=[username, password])

    if WXLINK_Present:
        scheduler.add_job(WXLINKFunctions.readWXLINKData, 'interval', seconds=SampleTime, args=[username, password])

    minuteCron = "*/"+str(int(GraphRefresh))
    scheduler.add_job(doAllGraphs, 'cron', second="0,15,30,45" )

    #scheduler.add_job(doAllGraphs, 'cron', minute=minuteCron )


    #scheduler.add_job(killLogger, 'interval', seconds=LengthSample)
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









