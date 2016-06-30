
######################################
#
# readThreePanelTestData and buildThreePanelTestGraph
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

import sys

sys.path.append('./SDL_Pi_TCA9545')

import SDL_Pi_TCA9545
#/*=========================================================================
#    I2C ADDRESS/BITS
#    -----------------------------------------------------------------------*/
TCA9545_ADDRESS =                         (0x73)    # 1110011 (A0+A1=VDD)
#/*=========================================================================*/

#/*=========================================================================
#    CONFIG REGISTER (R/W)
#    -----------------------------------------------------------------------*/
TCA9545_REG_CONFIG            =          (0x00)
#    /*---------------------------------------------------------------------*/

TCA9545_CONFIG_BUS0  =                (0x01)  # 1 = enable, 0 = disable
TCA9545_CONFIG_BUS1  =                (0x02)  # 1 = enable, 0 = disable
TCA9545_CONFIG_BUS2  =                (0x04)  # 1 = enable, 0 = disable
TCA9545_CONFIG_BUS3  =                (0x08)  # 1 = enable, 0 = disable

#/*=========================================================================*/


tca9545 = SDL_Pi_TCA9545.SDL_Pi_TCA9545(addr=TCA9545_ADDRESS, bus_enable = TCA9545_CONFIG_BUS0)

# the three channels of the ThreePanelTest named for SunAirPlus Solar Power Controller channels (www.switchdoc.com)
LIPO_BATTERY_CHANNEL = 1
SOLAR_CELL_CHANNEL   = 2
OUTPUT_CHANNEL       = 3

ThreePanelTesttableName = 'ThreePanelTestTable'


def readThreePanelTestData(password):
    	print('readThreePanelTestData - The time is: %s' % datetime.now())


	# open database
	con = mdb.connect('localhost', 'root', password, 'DataLogger' )
	cur = con.cursor()
  	print "------------------------------"
	print "Panel 1"
  	print "------------------------------"
	tca9545.write_control_register(TCA9545_CONFIG_BUS1)

	#initialize the ina3221 board
	ina3221 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)

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
        deviceid = 1
        query = 'INSERT INTO '+ThreePanelTesttableName+('(timestamp, deviceid, channel1_load_voltage, channel1_current, channel2_load_voltage, channel2_current, channel3_load_voltage, channel3_current) VALUES(UTC_TIMESTAMP(),  %i,  %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' %( deviceid,  busvoltage1, current_mA1, busvoltage2, current_mA2, busvoltage3, current_mA3))
        print("query=%s" % query)

        cur.execute(query)	

  	print "------------------------------"
	print "Panel 2"
  	print "------------------------------"

	tca9545.write_control_register(TCA9545_CONFIG_BUS2)
	#initialize the ina3221 board
	ina3221 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)

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
        deviceid = 2
        query = 'INSERT INTO '+ThreePanelTesttableName+('(timestamp, deviceid, channel1_load_voltage, channel1_current, channel2_load_voltage, channel2_current, channel3_load_voltage, channel3_current) VALUES(UTC_TIMESTAMP(),  %i,  %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' %( deviceid,  busvoltage1, current_mA1, busvoltage2, current_mA2, busvoltage3, current_mA3))
        print("query=%s" % query)

        cur.execute(query)	

  	print "------------------------------"
	print "Panel 3"
  	print "------------------------------"


	tca9545.write_control_register(TCA9545_CONFIG_BUS3)
	#initialize the ina3221 board
	ina3221 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)


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
        deviceid = 3
        query = 'INSERT INTO '+ThreePanelTesttableName+('(timestamp, deviceid, channel1_load_voltage, channel1_current, channel2_load_voltage, channel2_current, channel3_load_voltage, channel3_current) VALUES(UTC_TIMESTAMP(),  %i,  %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' %( deviceid,  busvoltage1, current_mA1, busvoltage2, current_mA2, busvoltage3, current_mA3))
        print("query=%s" % query)

        cur.execute(query)	
	con.commit()


# ThreePanelTest graph building routine




def buildThreePanelTestGraphCurrent(password, myGraphSampleCount):
    		print('buildThreePanelTestGraphCurrent - The time is: %s' % datetime.now())

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		mycursor = con1.cursor()

		print myGraphSampleCount
		query = '(SELECT timestamp, deviceid, channel1_load_voltage, channel1_current, channel2_load_voltage, channel2_current, channel3_load_voltage, channel3_current, id FROM '+ThreePanelTesttableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

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
		u = []   # Panel 1 - Current 
		v = []   # Panel 2 - Current 
		x = []   # Panel 3 - Current 
		averageCurrent1 = 0.0
		averageCurrent2 = 0.0
		averageCurrent3 = 0.0
 		currentCount = 0
		for record in result:
			if (record[1] == 1):
				t.append(record[0])
			if (record[1] == 1):
				u.append(-record[3])
				averageCurrent1  = averageCurrent1-record[3]
			if (record[1] == 2):
				v.append(-record[3])
				averageCurrent2  = averageCurrent2-record[3]
			if (record[1] == 3):
				x.append(-record[3])
				averageCurrent3  = averageCurrent3-record[3]
			
			currentCount=currentCount+1

		currentCount = currentCount /3
		averageCurrent1 = averageCurrent1/currentCount
		averageCurrent2 = averageCurrent2/currentCount
		averageCurrent3 = averageCurrent3/currentCount
		
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
		pylab.plot(t, u, color='r',label="Panel 1 Current",linestyle="-",marker=".")
		pylab.plot(t, v, color='b',label="Panel 2 Current",linestyle="-",marker=".")
		pylab.plot(t, x, color='g',label="Panel 3 Current",linestyle="-",marker=".")
		pylab.xlabel("Time")
		pylab.ylabel("Current mA")
		pylab.legend(loc='lower center')
		print "-----"
		print max(u)
		print "-----"
		pylab.axis([min(t), max(t), 0, max(u)+20])
		pylab.figtext(.5, .05, ("Ave Cur 1/2/3 %5.2fmA/%5.2fmA/%5.2fmA\n%s") %(averageCurrent1, averageCurrent2, averageCurrent3,  datetime.now()),fontsize=18,ha='center')

		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/ThreePanelTestDataLoggerGraphCurrent.png", facecolor=fig.get_facecolor())	



		mycursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------ThreePanelTestGraphCurrent finished now"




def buildThreePanelTestGraphVoltage(password, myGraphSampleCount):
    		print('buildThreePanelTestGraphVoltage - The time is: %s' % datetime.now())

		# open database
		con1 = mdb.connect('localhost', 'root', password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

    		mycursor = con1.cursor()

		print myGraphSampleCount
		query = '(SELECT timestamp, deviceid, channel1_load_voltage, channel1_current, channel2_load_voltage, channel2_current, channel3_load_voltage, channel3_current, id FROM '+ThreePanelTesttableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

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
		u = []   # Panel 1 - Voltage 
		v = []   # Panel 2 - Voltage 
		x = []   # Panel 3 - Voltage 
		averageCurrent1 = 0.0
		averageCurrent2 = 0.0
		averageCurrent3 = 0.0
 		currentCount = 0
		for record in result:
			if (record[1] == 1):
				t.append(record[0])
			if (record[1] == 1):
				u.append(record[4])
				averageCurrent1  = averageCurrent1+record[4]*(-record[3])
			if (record[1] == 2):
				v.append(record[4])
				averageCurrent2 = averageCurrent2+record[4]*(-record[3])
			if (record[1] == 3):
				x.append(record[4])
				averageCurrent3  = averageCurrent3+record[4]*(-record[3])
			
			currentCount=currentCount+1

		currentCount = currentCount /3
		averageCurrent1 = averageCurrent1/currentCount
		averageCurrent2 = averageCurrent2/currentCount
		averageCurrent3 = averageCurrent3/currentCount
		
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
		pylab.plot(t, u, color='r',label="Panel 1 Voltage",linestyle="-",marker=".")
		pylab.plot(t, v, color='b',label="Panel 2 Voltage",linestyle="-",marker=".")
		pylab.plot(t, x, color='g',label="Panel 3 Voltage",linestyle="-",marker=".")
		pylab.xlabel("Time")
		pylab.ylabel("Voltage V")
		pylab.legend(loc='lower center')
		pylab.axis([min(t), max(t), 0, 7])
		pylab.figtext(.5, .05, ("Ave Power 1/2/3 %5.2fW/%5.2fW/%5.2fW\n%s") %(averageCurrent1/1000, averageCurrent2/1000, averageCurrent3/1000,  datetime.now()),fontsize=18,ha='center')

		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/html/ThreePanelTestDataLoggerGraphVoltage.png", facecolor=fig.get_facecolor())	



		mycursor.close()       	 
		con1.close()

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "------ThreePanelTestGraphVoltage finished now"
######################################
#
# readThreePanelTestData and buildThreePanelTestGraph
#
#
######################################

