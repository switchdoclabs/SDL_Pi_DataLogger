#!/usr/bin/env python
# Datalogger.py
# Gather Data, put in SQL, Graph with MatPlot Lib 
# SwitchDoc Labs
# 05/31/2016
#
#

# imports

import MySQLdb as mdb

import os

import sys
import time
from datetime import datetime
import random 
import SDL_Pi_INA3221

import gc
from datetime import timedelta

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from matplotlib import pyplot
from matplotlib import dates
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pylab

from apscheduler.schedulers.background import BackgroundScheduler

# constant defines

#How often in seconds to sample Data
SampleTime = 0.5
#How long in seconds to sample Data
LengthSample = 60000
#How often to generate graph in seconds
GraphRefresh = 10
#How many samples to Graph
GraphSampleCount = 300


#mysql Password
password = 'password'
#mysql Table Name
tableName = 'WeatherLink'





# Main Program

print ""
print "Datalogger"
print ""
print "Sample uses 0x40 and SunAirPlus board INA3221"
print " Will work with the INA3221 SwitchDoc Labs Breakout Board"
print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
print ""

ina3221 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)
filename = time.strftime("%Y-%m-%d%H:%M:%SRTCTest") + ".txt"
starttime = datetime.utcnow()

# the three channels of the INA3221 named for SunAirPlus Solar Power Controller channels (www.switchdoc.com)
LIPO_BATTERY_CHANNEL = 1
SOLAR_CELL_CHANNEL   = 2
OUTPUT_CHANNEL       = 3

# open database
con = mdb.connect('localhost', 'root', password, 'DataLogger' )

# you must create a Cursor object. It will let
# you execute all the queries you need
cur = con.cursor()

# setup apscheduler

def tick():
    print('Tick! The time is: %s' % datetime.now()) 

def readData():
    	print('readData - The time is: %s' % datetime.now())


  	print "------------------------------"
  	shuntvoltage1 = 0
  	busvoltage1   = 0
  	current_mA1   = 0
  	loadvoltage1  = 0


  	busvoltage1 = ina3221.getBusVoltage_V(LIPO_BATTERY_CHANNEL)
  	shuntvoltage1 = ina3221.getShuntVoltage_mV(LIPO_BATTERY_CHANNEL)
  	# minus is to get the "sense" right.   - means the battery is charging, + that it is discharging
  	current_mA1 = ina3221.getCurrent_mA(LIPO_BATTERY_CHANNEL)  

  	loadvoltage1 = busvoltage1 + (shuntvoltage1 / 1000)

        # set Label
	# myLabel = "LIPO_Battery"
        myLabel = ""  

  	print "(Channel 1) %s Bus Voltage 1: %3.2f V " % (myLabel, busvoltage1)
  	print "(Channel 1) %s Shunt Voltage 1: %3.2f mV " % (myLabel, shuntvoltage1)
  	print "(Channel 1) %s Load Voltage 1:  %3.2f V" % (myLabel, loadvoltage1)
  	print "(Channel 1) %s Current 1:  %3.2f mA" % (myLabel, current_mA1)
  	print

  	shuntvoltage2 = 0
  	busvoltage2 = 0
  	current_mA2 = 0
  	loadvoltage2 = 0

  	busvoltage2 = ina3221.getBusVoltage_V(SOLAR_CELL_CHANNEL)
  	shuntvoltage2 = ina3221.getShuntVoltage_mV(SOLAR_CELL_CHANNEL)
        # "-" removed for this demo program
  	current_mA2 = ina3221.getCurrent_mA(SOLAR_CELL_CHANNEL)
  	loadvoltage2 = busvoltage2 + (shuntvoltage2 / 1000)
  
        # set Label
	# myLabel = "Solar Cell"
        myLabel = ""  

  	print "(Channel 2) %s Bus Voltage 2:  %3.2f V " % (myLabel, busvoltage2)
  	print "(Channel 2) %s Shunt Voltage 2: %3.2f mV " % (myLabel, shuntvoltage2)
  	print "(Channel 2) %s Load Voltage 2:  %3.2f V" % (myLabel, loadvoltage2)
  	print "(Channel 2) %s Current 2:  %3.2f mA" % (myLabel, current_mA2)
  	print 

  	shuntvoltage3 = 0
  	busvoltage3 = 0
  	current_mA3 = 0
  	loadvoltage3 = 0

  	busvoltage3 = ina3221.getBusVoltage_V(OUTPUT_CHANNEL)
  	shuntvoltage3 = ina3221.getShuntVoltage_mV(OUTPUT_CHANNEL)
  	current_mA3 = ina3221.getCurrent_mA(OUTPUT_CHANNEL)
  	loadvoltage3 = busvoltage3 + (shuntvoltage3 / 1000)
        
	# set Label
	# myLabel = "Output"
        myLabel = ""  
  
  	print "(Channel 3) %s Bus Voltage 3:  %3.2f V " % (myLabel, busvoltage3)
  	print "(Channel 3) %s Shunt Voltage 3: %3.2f mV " % (myLabel, shuntvoltage3)
  	print "(Channel 3) %s Load Voltage 3:  %3.2f V" % (myLabel, loadvoltage3)
  	print "(Channel 3) %s Current 3:  %3.2f mA" % (myLabel, current_mA3)
  	print
	#
	# Now put the data in MySQL
	# 
        # Put record in MySQL

        print "writing SQLdata ";


        # write record
        deviceid = 0
        query = 'INSERT INTO '+tableName+('(timestamp, deviceid, channel1_load_voltage, channel1_current, channel2_load_voltage, channel2_current, channel3_load_voltage, channel3_current) VALUES(UTC_TIMESTAMP(),  %i,  %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' %( deviceid,  busvoltage1, current_mA1, busvoltage2, current_mA2, busvoltage3, current_mA3))
        print("query=%s" % query)

        cur.execute(query)	
	con.commit()

# graph building routine

def buildGraph():
    		print('buildGraph - The time is: %s' % datetime.now())

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		cursor = con1.cursor()

		query = '(SELECT timestamp, deviceid, channel1_load_voltage, channel1_current, channel2_load_voltage, channel2_current, channel3_load_voltage, channel3_current, id FROM '+tableName+' ORDER BY id DESC LIMIT '+ str(GraphSampleCount) + ') ORDER BY id ASC' 

		print "query=", query
		try:
			cursor.execute(query)
			result = cursor.fetchall()
		except:
			e=sys.exc_info()[0]
			print "Error: %s" % e


		print result[0]
		t = []   # time
		u = []   # channel 1 - Current 
		averageCurrent = 0.0
 		currentCount = 0
		for record in result:
			t.append(record[0])
			u.append(record[7])
			averageCurrent = averageCurrent+record[7]
			currentCount=currentCount+1

		averageCurrent = averageCurrent/currentCount
		
		print ("count of t=",len(t))

		fds = dates.date2num(t) # converted
		# matplotlib date format object
		hfmt = dates.DateFormatter('%H:%M:%S')
		#hfmt = dates.DateFormatter('%m/%d-%H')

		fig = pyplot.figure()
		fig.set_facecolor('white')
		ax = fig.add_subplot(111,axisbg = 'white')
		ax.vlines(fds, -200.0, 1000.0,colors='w')



		#ax.xaxis.set_major_locator(dates.MinuteLocator(interval=1))
		ax.xaxis.set_major_formatter(hfmt)
		ax.set_ylim(bottom = -200.0)
		pyplot.xticks(rotation='45')
		pyplot.subplots_adjust(bottom=.3)
		pylab.plot(t, u, color='r',label="Arduino Current",linestyle="-",marker=".")
		pylab.xlabel("Seconds")
		pylab.ylabel("Current mA")
		pylab.legend(loc='lower center')

		pylab.axis([min(t), max(t), 0, max(u)+20])
		pylab.figtext(.5, .05, ("Average Current %6.2fmA\n%s") %(averageCurrent, datetime.now()),fontsize=18,ha='center')

		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/DataLoggerGraph.png", facecolor=fig.get_facecolor())	



		cursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------Graph finished now"


def killLogger():
    scheduler.shutdown()
    exit() 



if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(readData, 'interval', seconds=SampleTime)
    scheduler.add_job(buildGraph, 'interval', seconds=GraphRefresh)
    scheduler.add_job(killLogger, 'interval', seconds=LengthSample)
    scheduler.add_job(tick, 'interval', seconds=60)
    scheduler.start()
    scheduler.print_jobs()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))


    buildGraph()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()









