######################################
#
# readINA3221Data and buildINA3221Graph
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

from datetime import datetime
import MySQLdb as mdb
import SDL_Pi_INA3221

# the three channels of the INA3221 named for SunAirPlus Solar Power Controller channels (www.switchdoc.com)
LIPO_BATTERY_CHANNEL = 1
SOLAR_CELL_CHANNEL   = 2
OUTPUT_CHANNEL       = 3

INA3221tableName = 'INA3221Table'

#initialize the ina3221 board
ina3221 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)

def readINA3221Data(password):
    	print('readINA3221Data - The time is: %s' % datetime.now())


	# open database
	con = mdb.connect('localhost', 'root', password, 'DataLogger' )
	cur = con.cursor()
  	print "------------------------------"
  	shuntvoltage1 = 0
  	busvoltage1   = 0
  	current_mA1   = 0
  	loadvoltage1  = 0


  	busvoltage1 = ina3221.getBusVoltage_V(LIPO_BATTERY_CHANNEL)
  	print "------------------------------"
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
        query = 'INSERT INTO '+INA3221tableName+('(timestamp, deviceid, channel1_load_voltage, channel1_current, channel2_load_voltage, channel2_current, channel3_load_voltage, channel3_current) VALUES(UTC_TIMESTAMP(),  %i,  %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' %( deviceid,  busvoltage1, current_mA1, busvoltage2, current_mA2, busvoltage3, current_mA3))
        print("query=%s" % query)

        cur.execute(query)	
	con.commit()





# INA3221 graph building routine




def buildINA3221Graph(password, myGraphSampleCount):
    		print('buildINA3221Graph - The time is: %s' % datetime.now())

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		mycursor = con1.cursor()

		print myGraphSampleCount
		query = '(SELECT timestamp, deviceid, channel1_load_voltage, channel1_current, channel2_load_voltage, channel2_current, channel3_load_voltage, channel3_current, id FROM '+INA3221tableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

		print "query=", query
		try:
			mycursor.execute(query)
			result = mycursor.fetchall()
			print "---------"
		except:
			print "3---------"
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
		ax.set_ylim(bottom = 0.0)
		pyplot.xticks(rotation='45')
		pyplot.subplots_adjust(bottom=.3)
		pylab.plot(t, u, color='r',label="OurWeather Current",linestyle="-",marker=".")
		pylab.xlabel("Seconds")
		pylab.ylabel("Current mA")
		pylab.legend(loc='lower center')
		print "-----"
		print max(u)
		print "-----"
		pylab.axis([min(t), max(t), 0, max(u)+20])
		pylab.figtext(.5, .05, ("Average Current %6.2fmA\n%s") %(averageCurrent, datetime.now()),fontsize=18,ha='center')

		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/INA3221DataLoggerGraph.png", facecolor=fig.get_facecolor())	



		mycursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------INA3221Graph finished now"


######################################
#
# readINA3221Data and buildINA3221Graph
#
#
######################################

