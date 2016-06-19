
######################################
#
# readOURWEATHERData and buildOURWEATHERGraph
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


import httplib2 as http
import json


try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from datetime import datetime
import MySQLdb as mdb


OURWEATHERtableName = 'OURWEATHERTable'

# set up your OurWeather IP Address here
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





def readOURWEATHERData(password):
    	print('readOURWEATHERData - The time is: %s' % datetime.now())

	data = fetchJSONData(uri, path)


	# pre split weather data
	preSplitData = data['FullDataString']
	WData = preSplitData.split(",")
	print WData

	if (len(WData) < 18):   
		# we have a bad read
		# try again later
		print "bad read from OurWeather"
		return 0

	if (len(WData) == 18):
		# Version does not have air quality
		WData.append(0)
		WData.append(4)

	# open database
	con = mdb.connect('localhost', 'root', password, 'DataLogger' )
	cur = con.cursor()

	#
	# Now put the data in MySQL
	# 
        # Put record in MySQL

        print "writing SQLdata ";


        # write record
        deviceid = 0
        query = 'INSERT INTO '+OURWEATHERtableName+('(timestamp, deviceid, Outdoor_Temperature , Outdoor_Humidity , Indoor_Temperature , Barometric_Pressure , Altitude , Current_Wind_Speed , Current_Wind_Gust , Current_Wind_Direction , Rain_Total , Wind_Speed_Minimum , Wind_Speed_Maximum , Wind_Gust_Minimum , Wind_Gust_Maximum , Wind_Direction_Minimum , Wind_Direction_Maximum , Display_English_Metrice , OurWeather_DateTime , OurWeather_Station_Name , Current_Air_Quality_Sensor , Current_Air_Quality_Qualitative ) VALUES(UTC_TIMESTAMP(),  %i, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %i, "%s" , "%s", %i, %i)' % ( int(data['id']), float(WData[0]), float(WData[1]), float(WData[2]), float(WData[3]), float(WData[4]), float(WData[5]), float(WData[6]), float(WData[7]), float(WData[8]), float(WData[9]), float(WData[10]), float(WData[11]), float(WData[12]), float(WData[13]), float(WData[14]), int(WData[15]), WData[16], WData[17], int(WData[18]), int(WData[19])) ) 
        
	print("query=%s" % query)

        cur.execute(query)	
	con.commit()





# OURWEATHER graph building routine




def buildOURWEATHERGraphTemperature(password, myGraphSampleCount):
    		print('buildOURWEATHERGraph - The time is: %s' % datetime.now())

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		mycursor = con1.cursor()

		print myGraphSampleCount
		query = '(SELECT timestamp, deviceid, Outdoor_Temperature, OutDoor_Humidity, OurWeather_Station_Name, id FROM '+OURWEATHERtableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

		print "query=", query
		try:
			mycursor.execute(query)
			result = mycursor.fetchall()
		except:
			e=sys.exc_info()[0]
			print "Error: %s" % e


		t = []   # time
		u = []   # Outdoor temperature
		v = []   # Outdoor humidity
		averageTemperature = 0.0
 		currentCount = 0

		for record in result:
			t.append(record[0])
			u.append(record[2])
			v.append(record[3])
			averageTemperature = averageTemperature+record[2]
			currentCount=currentCount+1
			StationName = record[4]

		averageTemperature = averageTemperature/currentCount
		
		print ("count of t=",len(t))

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
		pylab.plot(t, u, color='r',label="Outside Temp (C) ",linestyle="-",marker=".")
		pylab.xlabel("Time")
		pylab.ylabel("degrees C")
		pylab.legend(loc='upper left')
		pylab.axis([min(t), max(t), -20, 50])

		ax2 = pylab.twinx()
		pylab.ylabel("% ")
		pylab.plot(t, v, color='b',label="Outside Hum %",linestyle="-",marker=".")
		pylab.axis([min(t), max(t), 0, 100])
		pylab.legend(loc='lower left')
		pylab.figtext(.5, .05, ("%s Average Temperature %6.2f\n%s") %( StationName, averageTemperature, datetime.now()),fontsize=18,ha='center')
		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/OURWEATHERDataLoggerGraphTemperature.png", facecolor=fig.get_facecolor())	



		mycursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------OURWEATHERGraphTemperature finished now"


def buildOURWEATHERGraphWind(password, myGraphSampleCount):
    		print('buildOURWEATHERGraph - The time is: %s' % datetime.now())

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		mycursor = con1.cursor()

		print myGraphSampleCount
		query = '(SELECT timestamp, deviceid, Current_Wind_Speed, Current_Wind_Gust, OurWeather_Station_Name, id FROM '+OURWEATHERtableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

		print "query=", query
		try:
			mycursor.execute(query)
			result = mycursor.fetchall()
		except:
			e=sys.exc_info()[0]
			print "Error: %s" % e


		t = []   # time
		u = []   # Current Wind Speed
		v = []   # Current Wind Gust 
		averageWindSpeed = 0.0
 		currentCount = 0

		for record in result:
			t.append(record[0])
			u.append(record[2])
			#v.append(record[3])
			averageWindSpeed = averageWindSpeed+record[2]
			currentCount=currentCount+1
			StationName = record[4]

		averageWindSpeed = averageWindSpeed/currentCount
		
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
		pylab.plot(t, u, color='r',label="Wind Speed (kph)" ,linestyle="o",marker=".")
		#pylab.plot(t, v, color='b',label="Wind Gust (kph)" ,linestyle="o",marker=".")
		pylab.xlabel("Time")
		pylab.ylabel("Wind (kph)")
		pylab.legend(loc='lower center')
		pylab.axis([min(t), max(t), min(u)-20, max(u)+20])
		pylab.figtext(.5, .05, ("%s Average Windspeed %6.2f\n%s") %( StationName, averageWindSpeed, datetime.now()),fontsize=18,ha='center')

		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/OURWEATHERDataLoggerGraphWind.png", facecolor=fig.get_facecolor())	



		mycursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------OURWEATHERGraphWind finished now"


######################################
#
# readOURWEATHERData and buildOURWEATHERGraph
#
#
######################################

