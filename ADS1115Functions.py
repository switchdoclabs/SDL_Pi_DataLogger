######################################
#
# readADS1115Data and buildADS1115Graph
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


from datetime import datetime
import MySQLdb as mdb

from MADS1x15 import ADS1x15

ADS1115tableName = 'ADS1115Table'

# Initialise the ADC using the default mode (use default I2C address)
ADS1115 = 0x01  # 16-bit ADC
ads1115 = ADS1x15(ic=ADS1115)


def readADS1115Data(password):
    	print('readADS1115Data - The time is: %s' % datetime.now())


	# open database
	con = mdb.connect('localhost', 'root', password, 'DataLogger' )
	cur = con.cursor()



        gain = 6144  # +/- 6.144V

        # Select the sample rate
        sps = 250  # 250 samples per second


  	print "------------------------------"
        rawData = []
	Voltage = []

 	for x in range (0,4):
		rawData.append(ads1115.readRAW_ADCSingleEnded(x, gain, sps))
		Voltage.append(ads1115.readADCSingleEnded(x, gain, sps)/1000)

	# set Label
	# myLabel = "Output"
        myLabel = ""  
  
	#
	# Now put the data in MySQL
	# 
        # Put record in MySQL

        print "writing SQLdata ";


        # write record
        deviceid = 0
        query = 'INSERT INTO '+ADS1115tableName+('(timestamp, deviceid, channel0_voltage, channel0_raw, channel1_voltage, channel1_raw, channel2_voltage, channel2_raw, channel3_voltage, channel3_raw) VALUES(UTC_TIMESTAMP(),  %i,  %.3f, %i, %.3f, %i, %.3f, %i, %.3f, %i)' %( deviceid,  Voltage[0], rawData[0], Voltage[1], rawData[1], Voltage[2], rawData[2], Voltage[3], rawData[3] ))
        print("query=%s" % query)

        cur.execute(query)	
	con.commit()





# ADS1115 graph building routine




def buildADS1115Graph(password, myGraphSampleCount):
    		print('buildADS1115Graph - The time is: %s' % datetime.now())

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		mycursor = con1.cursor()

		print myGraphSampleCount
		query = '(SELECT timestamp, deviceid, channel0_voltage, channel0_raw, channel1_voltage, channel1_raw, channel2_voltage, channel2_raw, channel3_voltage, channel3_raw, id FROM '+ADS1115tableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

		print "query=", query
		try:
			mycursor.execute(query)
			result = mycursor.fetchall()
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
			u.append(record[3])
			averageCurrent = averageCurrent+record[3]
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
		pylab.plot(t, u, color='r',label="Air Quality Sensor",linestyle="-",marker=".")
		pylab.xlabel("Seconds")
		pylab.ylabel("Raw Data")
		pylab.legend(loc='lower center')
		pylab.axis([min(t), max(t), min(u)-20, max(u)+20])
		pylab.figtext(.5, .05, ("Average Air Quality %6.2f\n%s") %(averageCurrent, datetime.now()),fontsize=18,ha='center')

		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/ADS1115DataLoggerGraph.png", facecolor=fig.get_facecolor())	



		mycursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------ADS1115Graph finished now"


######################################
#
# readADS1115Data and buildADS1115Graph
#
#
######################################

