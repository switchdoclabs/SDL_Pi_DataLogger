
######################################
#
# readWXLINKData and buildWXLINKGraph
#
#
######################################

import gc
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from matplotlib import pyplot
from matplotlib import dates
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pylab

import sys

import smbus 
import time

from pytz import timezone

from struct import *


i2cbus = smbus.SMBus(1)

WXLINKaddress = 0x08


import httplib2 as http
import json


try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from datetime import datetime
import MySQLdb as mdb


WXLINKtableName = 'WXLINKTable'

# set up your WxLink I2C address IP Address here
uri = 'http://192.168.1.140/FullDataString'
path = '/'

# fetch the JSON data from the OurWeather device
def fetchJSONData(uri, path):
	target = urlparse(uri+path)
	method = 'GET'
	body = ''

	h = http.Http()
	
	# If you need authentication some example:
	#if auth:
	#    h.add_credentials(auth.user, auth.password)

	response, content = h.request(
        	target.geturl(),
        	method,
        	body,
        	headers)

	# assume that content is a json reply
	# parse content with the json module
	data = json.loads(content)

	return data

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}


import crcpython2
# read WXLink and return list to set variables
crcCalc = crcpython2.CRCCCITT(version='XModem')

def readWXLINKData(password):
    	print('readWXLINKData - The time is: %s' % datetime.now(timezone('US/Pacific')))

   	try:
		data1 = "" 
   		data2 =  ""
   		print "-----------"
   		print "block 1"
   		data1 = i2cbus.read_i2c_block_data(WXLINKaddress, 0);
		data1 = bytearray(data1)
   		#data1 = i2cbus.read_i2c_block_data(WXLINKaddress, 0);
   		print ' '.join(hex(x) for x in data1) 
   		print "block 2"
   		data2 = i2cbus.read_i2c_block_data(WXLINKaddress, 1);
		data2 = bytearray(data2)
   		#data2 = i2cbus.read_i2c_block_data(WXLINKaddress, 1);
   		print ' '.join(hex(x) for x in data2) 
   		print "-----------"



                if ((len(data1) == 0) or (len(data2) == 0)):
			print "zero length WXLink Read"
			return   # bad read


                # check crc for errors - don't update data if crc is bad

                #get crc from data
                receivedCRC = unpack('H', str(data2[29:31]))[0]
                #swap bytes for recievedCRC
                receivedCRC = (((receivedCRC)>>8) | ((receivedCRC&0xFF)<<8))&0xFFFF
                print "ReversedreceivedCRC= %x" % receivedCRC

                calculatedCRC = crcCalc.calculate(data1+data2[0:27])

                print "calculatedCRC = %x " % calculatedCRC

                # check for start bytes, if not present, then invalidate CRC

                if (data1[0] != 0xAB) or (data1[1] != 0x66):
                       calculatedCRC = receivedCRC + 1


		if (receivedCRC == calculatedCRC):
                        print "Good CRC Recived"

			#data1
	
			print len(data1)
			header0 = data1[0]
			header1 = data1[1]
			protocol = data1[2]
			timeSinceReboot = unpack('i',str(data1[3:7]))[0]
			windDirection = unpack('H', str(data1[7:9]))[0]
			averageWindSpeed = unpack('f', str(data1[9:13]))[0]
			windClicks = unpack('l', str(data1[13:17]))[0]
			totalRainClicks = unpack('l', str(data1[17:21]))[0]
			maximumWindGust = unpack('f', str(data1[21:25]))[0]
			outsideTemperature = unpack('f', str(data1[25:29]))[0]
			elements = [data1[29], data1[30], data1[31], data2[0]]
			outHByte = bytearray(elements)
			outsideHumidity = unpack('f', str(outHByte))[0]
	
			# data2
		
			batteryVoltage = unpack('f', str(data2[1:5]))[0]
			batteryCurrent = unpack('f', str(data2[5:9]))[0]
			loadCurrent = unpack('f', str(data2[9:13]))[0]
			solarPanelVoltage = unpack('f', str(data2[13:17]))[0]
			solarPanelCurrent = unpack('f', str(data2[17:21]))[0]
	
			auxA = unpack('f', str(data2[21:25]))[0]
			messageID = unpack('l', str(data2[25:29]))[0]
			checksumLow = data2[29]
			checksumHigh = data2[30]


			print "header = %x %x" % (header0, header1)
			print "protocol = %d" % (protocol )
			print "timeSinceReboot = %d" % timeSinceReboot
			print "windDirection = %d" % windDirection
			print "averageWindSpeed = %6.2f" % averageWindSpeed
			print "windClicks = %d" % windClicks
			print "totalRainClicks = %d" % totalRainClicks
			print "maximumWindGust = %6.2f" % maximumWindGust
			print "outsideTemperature = %6.2f" % outsideTemperature
			print "outsideHumidity = %6.2f" % outsideHumidity
	
			# data 2
		
			print "batteryVoltage = %6.2f" % batteryVoltage
			print "batteryCurrent = %6.2f" % batteryCurrent
			print "loadCurrent = %6.2f" % loadCurrent
			print "solarPanelVoltage = %6.2f" % solarPanelVoltage
			print "solarPanelCurrent = %6.2f" % solarPanelCurrent
			print "auxA = %6.2f" % auxA
			print "messageID = %d" % (messageID )
			print "checksumHigh =0x%x" % (checksumHigh )
			print "checksumLow =0x%x" % (checksumLow )
	
			# open database
			con = mdb.connect('localhost', 'root', password, 'DataLogger' )
			cur = con.cursor()
		
			#
			# Now put the data in MySQL
			# 
        		# Put record in MySQL
	
        		print "writing SQLdata ";
		
			try:
				# get last record read
				query = "SELECT MessageID FROM "+WXLINKtableName+" ORDER BY id DESC LIMIT 1"
        			cur.execute(query)	
		
				results = cur.fetchone()
				lastMessageID = results[0]
				print "lastMessageID =", lastMessageID
			except:
				print "No data in Database"
				lastMessageID = -1
		
			if (lastMessageID != messageID):
        			# write record
        			deviceid = 0

				myTimeStamp = datetime.now(timezone('US/Pacific'))
        			query = 'INSERT INTO '+WXLINKtableName+(' (TimeStamp , deviceid , Protocol, Outdoor_Temperature , Outdoor_Humidity , Indoor_Temperature , Barometric_Pressure , Current_Wind_Speed , Current_Wind_Clicks , Current_Wind_Direction , Rain_Total_Clicks , Battery_Voltage , Battery_Current , Load_Current , Solar_Panel_Voltage , Solar_Panel_Current , MessageID , Time_Since_Reboot , AuxA) VALUES("%s", %i, %i, %.3f, %.3f, %.3f, %.3f, %.3f, %i, %i, %i, %.3f, %.3f, %.3f, %.3f, %.3f, %i, %i, %.3f)' % (myTimeStamp, 0, protocol, outsideTemperature, outsideHumidity, 0, 0, averageWindSpeed , windClicks, windDirection, totalRainClicks, batteryVoltage, batteryCurrent, loadCurrent, solarPanelVoltage, solarPanelCurrent,  messageID, timeSinceReboot, auxA)) 
		
		
       		 
				print("query=%s" % query)
		
        			cur.execute(query)	
		
			con.commit()
	except:
		print "Error in reading WXLINK"	
		print sys.exc_info()[0]	
	
	
# WXLINK graph building routine


def buildWXLINKGraphSolar(password, myGraphSampleCount):
    		print('buildWXLINKGraphSolar - The time is: %s' % datetime.now(timezone('US/Pacific')))

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		mycursor = con1.cursor()

		print myGraphSampleCount
		query = '(SELECT timestamp, deviceid, Outdoor_Temperature, OutDoor_Humidity, Battery_Voltage, Battery_Current, Solar_Panel_Voltage, Solar_Panel_Current,  Load_Current, id FROM '+WXLINKtableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

		print "query=", query
		try:
			mycursor.execute(query)
			result = mycursor.fetchall()
		except:
			e=sys.exc_info()[0]
			print "Error: %s" % e

		
		t = []   # time
		u = []   # Battery_Voltage
		v = []   # Battery_Current 
		x = []   # Solar_Panel_Voltage 
		y = []   # Solar_Panel_Current 
		z = []   # Load_Current 
		averagePowerIn = 0.0
		averagePowerOut = 0.0
 		currentCount = 0

		for record in result:
			t.append(record[0])
			u.append(record[4])
			v.append(record[5])
			x.append(record[6])
			y.append(record[7])
			z.append(record[8])

		print ("count of t=",len(t))

		lastSampleTime = t[-1]

		fds = dates.date2num(t) # converted
		# matplotlib date format object
		hfmt = dates.DateFormatter('%H:%M:%S')
		#hfmt = dates.DateFormatter('%m/%d-%H')

		fig = pyplot.figure()
		fig.set_facecolor('white')
		ax = fig.add_subplot(111,axisbg = 'white')
		ax.vlines(fds, -200.0, 1000.0,colors='w')
		
		ax2 = fig.add_subplot(111,axisbg = 'white')


		ax.xaxis.set_major_formatter(hfmt)
		pyplot.xticks(rotation='45')
		pyplot.subplots_adjust(bottom=.3)
		pylab.plot(t, u, color='red',label="Battery Voltage (V) ",linestyle="-",marker=".")
		pylab.plot(t, x, color='green',label="Solar Voltage (V) ",linestyle="-",marker=".")
		pylab.xlabel("Time")
		pylab.ylabel("Voltage (V)")
		pylab.legend(loc='upper left', fontsize='x-small')
		pylab.axis([min(t), max(t), 0, 7])

		ax2 = pylab.twinx()
		pylab.ylabel("Current (mA) ")
		pylab.plot(t, v, color='black',label="Battery Current (mA)",linestyle="-",marker=".")
		pylab.plot(t, y, color='blue',label="Solar Current (mA)",linestyle="-",marker=".")
		pylab.plot(t, z, color='purple',label="Load Current (mA)",linestyle="-",marker=".")
		pylab.axis([min(t), max(t), -60, 80])
		pylab.legend(loc='lower left', fontsize='x-small')

		pylab.figtext(.5, .01, ("Solar Performance WXLink\n%s\nLast Sample: %s") % (datetime.now(timezone('US/Pacific')), lastSampleTime ),fontsize=18,ha='center')
		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/WXLINKDataLoggerGraphSolar.png", facecolor=fig.get_facecolor())	



		mycursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------WXLINKGraphTemperature finished now"

def buildWXLINKGraphSolarCurrent(password, myGraphSampleCount):
    		print('buildWXLINKGraphSolarCurrent - The time is: %s' % datetime.now(timezone('US/Pacific')))

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		mycursor = con1.cursor()

		print myGraphSampleCount
		query = '(SELECT timestamp, deviceid, Outdoor_Temperature, OutDoor_Humidity, Battery_Voltage, Battery_Current, Solar_Panel_Voltage, Solar_Panel_Current,  Load_Current, id FROM '+WXLINKtableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

		print "query=", query
		try:
			mycursor.execute(query)
			result = mycursor.fetchall()
		except:
			e=sys.exc_info()[0]
			print "Error: %s" % e

		
		t = []   # time
		u = []   # Battery_Current 
		v = []   # Solar_Panel_Current 
		x = []   # Load_Current 
		averagePowerIn = 0.0
		averagePowerOut = 0.0
 		currentCount = 0

		for record in result:
			t.append(record[0])
			u.append(record[5])
			v.append(record[7])
			x.append(record[8])

		print ("count of t=",len(t))

		lastSampleTime = t[-1]

		fds = dates.date2num(t) # converted
		# matplotlib date format object
		hfmt = dates.DateFormatter('%H:%M:%S')
		#hfmt = dates.DateFormatter('%m/%d-%H')

		fig = pyplot.figure()
		fig.set_facecolor('white')
		ax = fig.add_subplot(111,axisbg = 'white')
		ax.vlines(fds, -200.0, 1000.0,colors='w')
		
		ax2 = fig.add_subplot(111,axisbg = 'white')


		ax.xaxis.set_major_formatter(hfmt)
		pyplot.xticks(rotation='45')
		pyplot.subplots_adjust(bottom=.3)
		pylab.plot(t, u, color='red',label="Battery Current (V) ",linestyle="-",marker=".")
		pylab.plot(t, v, color='green',label="Solar Panel Current (V) ",linestyle="-",marker=".")
		pylab.plot(t, x, color='blue',label="Load Current (V) ",linestyle="-",marker=".")
		pylab.xlabel("Time")
		pylab.ylabel("Current (mA)")
		pylab.legend(loc='upper left', fontsize='x-small')
		pylab.axis([min(t), max(t), min(u)-10, max(v) + 20])

		
		pylab.figtext(.5, 0.01, ("Solar Current Performance WXLink\n%s\nLast Sample: %s") % (datetime.now(timezone('US/Pacific')), lastSampleTime ),fontsize=18,ha='center')
		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/WXLINKDataLoggerGraphSolarCurrent.png", facecolor=fig.get_facecolor())	



		mycursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------WXLINKGraphCurrent finished now"



def buildWXLINKGraphSolarVoltage(password, myGraphSampleCount):
    		print('buildWXLINKGraphSolarVoltage - The time is: %s' % datetime.now(timezone('US/Pacific')))

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		mycursor = con1.cursor()

		print myGraphSampleCount
		query = '(SELECT timestamp, deviceid, Outdoor_Temperature, OutDoor_Humidity, Battery_Voltage, Battery_Current, Solar_Panel_Voltage, Solar_Panel_Current,  Load_Current, id FROM '+WXLINKtableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

		print "query=", query
		try:
			mycursor.execute(query)
			result = mycursor.fetchall()
		except:
			e=sys.exc_info()[0]
			print "Error: %s" % e

		
		t = []   # time
		u = []   # Battery_Voltage
		v = []   # Solar_Panel_Voltage 
		averagePowerIn = 0.0
		averagePowerOut = 0.0
 		currentCount = 0

		for record in result:
			t.append(record[0])
			u.append(record[4])
			v.append(record[6])

		print ("count of t=",len(t))

		lastSampleTime = t[-1]

		fds = dates.date2num(t) # converted
		# matplotlib date format object
		hfmt = dates.DateFormatter('%H:%M:%S')
		#hfmt = dates.DateFormatter('%m/%d-%H')

		fig = pyplot.figure()
		fig.set_facecolor('white')
		ax = fig.add_subplot(111,axisbg = 'white')
		ax.vlines(fds, -200.0, 1000.0,colors='w')
		
		ax2 = fig.add_subplot(111,axisbg = 'white')


		ax.xaxis.set_major_formatter(hfmt)
		pyplot.xticks(rotation='45')
		pyplot.subplots_adjust(bottom=.3)
		pylab.plot(t, u, color='red',label="Battery Voltage (V) ",linestyle="-",marker=".")
		pylab.plot(t, v, color='green',label="Solar Voltage (V) ",linestyle="-",marker=".")
		pylab.xlabel("Time")
		pylab.ylabel("Voltage (V)")
		pylab.legend(loc='upper left', fontsize='x-small')
		pylab.axis([min(t), max(t), 0, 7])


		pylab.figtext(.5, .01, ("Solar Voltage Performance WXLink\n%s\nLast Sample: %s") % (datetime.now(timezone('US/Pacific')), lastSampleTime),fontsize=18,ha='center')
		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/WXLINKDataLoggerGraphSolarVoltage.png", facecolor=fig.get_facecolor())	



		mycursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------WXLINKGraphSolarVoltage finished now"




def buildWXLINKGraphSolarPower(password, myGraphSampleCount):
    		print('buildWXLINKGraphSolarPower - The time is: %s' % datetime.now(timezone('US/Pacific')))

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		mycursor = con1.cursor()

		print myGraphSampleCount
		query = '(SELECT timestamp, deviceid, Outdoor_Temperature, OutDoor_Humidity, Battery_Voltage, Battery_Current, Solar_Panel_Voltage, Solar_Panel_Current,  Load_Current, id FROM '+WXLINKtableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

		print "query=", query
		try:
			mycursor.execute(query)
			result = mycursor.fetchall()
		except:
			e=sys.exc_info()[0]
			print "Error: %s" % e

		
		t = []   # time
		u = []   # Battery_Voltage
		v = []   # Battery_Current
		x = []   # Solar_Panel_Voltage 
		y = []   # Solar_Panel_Current 
		z = []   # Load_Current 

		sp = [] # Solar Power
		bp = [] # Battery Power
		lp = [] # Load Power

		averagePowerIn = 0.0
		averagePowerOut = 0.0
 		currentCount = 0

		for record in result:
			t.append(record[0])
			u.append(record[4])
			v.append(record[5])
			x.append(record[6])
			y.append(record[7])
			z.append(record[8])

			sp.append(record[6]*record[7])
			bp.append(record[4]*record[5])
			lp.append(5.0*record[8])   # assume 5V nominal output

			

		print ("count of t=",len(t))

		lastSampleTime = t[-1]

		fds = dates.date2num(t) # converted
		# matplotlib date format object
		hfmt = dates.DateFormatter('%H:%M:%S')
		#hfmt = dates.DateFormatter('%m/%d-%H')

		fig = pyplot.figure()
		fig.set_facecolor('white')
		ax = fig.add_subplot(111,axisbg = 'white')
		ax.vlines(fds, -200.0, 1000.0,colors='w')
		
		ax2 = fig.add_subplot(111,axisbg = 'white')


		ax.xaxis.set_major_formatter(hfmt)
		pyplot.xticks(rotation='45')
		pyplot.subplots_adjust(bottom=.3)
		pylab.plot(t, sp, color='green',label="Solar Power (mW) ",linestyle="-",marker=".")
		pylab.plot(t, bp, color='red',label="Battery Power (mW) ",linestyle="-",marker=".")
		pylab.plot(t, lp, color='black',label="Load Power (mW) ",linestyle="-",marker=".")
		pylab.xlabel("Time")
		pylab.ylabel("milli Watts (mW)")
		pylab.legend(loc='upper left', fontsize='x-small')
		fullpower = []
		fullpower.extend(sp)
		fullpower.extend(bp)
		fullpower.extend(lp)
		pylab.axis([min(t), max(t), min(fullpower)-100  , max(fullpower)+100])


		pylab.figtext(.5, .01, ("System Power Performance WXLink\n%s\nLast Sample: %s") % (datetime.now(timezone('US/Pacific')), lastSampleTime),fontsize=18,ha='center')
		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/WXLINKDataLoggerGraphPower.png", facecolor=fig.get_facecolor())	



		mycursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------WXLINKGraphPower finished now"




######################################
#
# readWXLINKData and buildWXLINKGraph
#
#
######################################

