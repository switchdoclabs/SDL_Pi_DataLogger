from __future__ import print_function
######################################
#
# readINA219Data and buildINA219Graph
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
import matplotlib.dates as mdates

from datetime import datetime
import pymysql as mdb
import sys

from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1


INA219tableName = 'INA219Table'

#initialize the ina3221 board
ina219 =  INA219(SHUNT_OHMS,address=0x45)
ina219.configure()


def readINA219Data(username, password):
        print('readINA219Data - The time is: %s' % datetime.now())


	# open database
        con = mdb.connect('localhost', username, password, 'DataLogger' )
        cur = con.cursor()
        print("------------------------------")

    

        voltage = ina219.voltage()	
        current = ina219.current()
        power = ina219.power()
        print("------------------------------")
        # minus is to get the "sense" right.   - means the battery is charging, + that it is discharging
        # set Label
        myLabel = ""  

        print("%s Voltage :  %3.2f V" % (myLabel, voltage))
        print("%s Current :  %3.2f mA" % (myLabel, current))
        print("%s Power :  %3.2f mW" % (myLabel, power))
        print()

	#
	# Now put the data in MySQL
	# 
        # Put record in MySQL

        print("writing SQLdata ")


        # write record
        deviceid = 0
        query = 'INSERT INTO '+INA219tableName+('(TimeStamp, Voltage, Current, Power) VALUES(UTC_TIMESTAMP(3),   %.3f, %.3f, %.3f )' %( voltage, current, power ))
        print("query=%s" % query)

        cur.execute(query)	
        con.commit()





# INA219 graph building routine

def strftime_ms(datetime_obj):
    y,m,d,H,M,S = datetime_obj.timetuple()[:6]
    ms = timedelta(microseconds = round(datetime_obj.microsecond/1000.0)*1000)
    ms_date = datetime(y,m,d,H,M,S) + ms
    return ms_date.strftime('%M:%S.%f')[:-3]


def buildINA219Graph(username, password, myGraphSampleCount):
                print('buildINA219Graph - The time is: %s' % datetime.now())

		# open database
                con1 = mdb.connect('localhost', username, password, 'DataLogger' )
		# now we have to get the data, stuff it in the graph 

                mycursor = con1.cursor()

                print(myGraphSampleCount)
                query = '(SELECT timestamp, voltage, current, power, id FROM '+INA219tableName+' ORDER BY id DESC LIMIT '+ str(myGraphSampleCount) + ') ORDER BY id ASC' 

                print(("query=", query))
                try:
                    mycursor.execute(query)
                    result = mycursor.fetchall()
                    print("---------")
                except:
                    print("3---------")
                    e=sys.exc_info()[0]
                    print("Error: %s" % e)


                print(result[0])
                t = []   # time
                u = []   # channel Current 
                v = []   # channel Voltage 
                averageCurrent = 0.0
                currentCount = 0
                peakCurrent = 0.0
                minimumVoltage = 6.0
                for record in result:
                    t.append(record[0])
                    v.append(record[1])
                    u.append(record[2])
                    averageCurrent = averageCurrent+record[2]
                    if (record[2] > peakCurrent):
                        peakCurrent = record[2]
                    if (record[1] > 4.75):
                        if (record[1] < minimumVoltage):
                            minimumVoltage = record[1]
                    currentCount=currentCount+1

                averageCurrent = averageCurrent/currentCount
                ''
                print(("count of t=",len(t)))
                x1 =  t

		# matplotlib date format object
                hfmt = dates.DateFormatter('%M:%S')
		#hfmt = dates.DateFormatter('%m/%d-%H')

                fig = pyplot.figure()
                fig.set_facecolor('white')
                #ax = fig.add_subplot(111,axisbg = 'white')
                ax1 = fig.add_subplot(211)
                ax1.xaxis.set_major_formatter(hfmt)
                ax1.plot(x1, u, '-', color='r', label = 'current')
                ax1.grid()
                
                ax2 = fig.add_subplot(212)
                ax2.xaxis.set_major_formatter(hfmt)

                ax2.plot(x1, v, '-', color='b', label = 'voltage')
                ax2.grid()
              
                ax1.legend(loc=0)

                ax2.legend(loc=0)

                ax1.set_ylabel("Current mA")
                ax2.set_ylabel("Voltage V")
                
                ax2.set_ylim(4.5, 5.5)
                ax1.set_ylim(0,1400)

                
                #ax2.xaxis.set_tick_params(rotation=45)
                #pyplot.xticks(rotation='45')

                pyplot.subplots_adjust(bottom=.3)

                name = "Pi3B+ Turn On Current SmallPS w/Cap "
                pylab.figtext(.5, .05, ("%s\nAverage Current %6.2fmA\nPeak Current %6.2fmA\nMinimum Voltage %6.2fV\n%s UTC") %(name,averageCurrent, peakCurrent, minimumVoltage, x1[0]),fontsize=12,ha='center')


                pyplot.show()
                pyplot.savefig("/var/www/html/INA219DataLoggerGraph.png", facecolor=fig.get_facecolor())	



                mycursor.close()       	 
                con1.close()
                
                fig.clf()
                pyplot.close()
                pylab.close()
                gc.collect()
                print("------INA219Graph finished now")
                


                '''
                # plot
                pyplot.plot(t,u)
                
                # beautify the x-labels
                pyplot.gcf().autofmt_xdate()
                pylab.axis([min(fds), max(fds), 0, max(u)+20])
                pylab.figtext(.5, .05, ("Average Current %6.2fmA\n%s") %(averageCurrent, datetime.now()),fontsize=18,ha='center')
                
                pylab.grid(True)
                
                pyplot.show()
                pyplot.savefig("/var/www/html/INA219DataLoggerGraph.png")	
                pyplot.close()
                '''
######################################
#
# readINA219Data and buildINA219Graph
#
#
######################################

