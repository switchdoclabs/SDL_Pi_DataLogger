Raspberry Pi DataLogger
SwitchDoc Labs

Version 3.0

March 25, 2018: Fixed MatPlot issues related to Raspberry Stretch Release

June 01, 2016: Set up to measure current using Grove INA3221 3 channel Current Measuring Breakout Board and display with MatPlotLib

June 11, 2016: Set up to measure voltage using Grove ADS1115 4 Channel 16 Bit ADC Board

June 15, 2016: Added configuration variables

June 18, 2016: Installed OurWeather suppot / Fixed multiple graph generation

June 30, 2016: Added software to measure three solar panels at once through an I2C Mux and Three SunAirPlus boards

July 16, 2016: Added WXLink support (Wireless link for the WeatherRack Weather Sensors to the Raspberry Pi) 

September 19, 2016:  Added OurWeather Solar Extender to the Database 

October 20, 2016: Improved WXLink Error Checking

December 29, 2016:  Added additional graphs for ADS1115 display

January 7, 2017:  Calibrated scaling on O2 sensor graph

Supports the INA3221 Grove Breakout Board or SunAirPlus on switchdoc.com
Supports the ADS1115 Grove Breakout Board on switchdoc.com
Supports the OurWeather Full Weather Kit
Supports the Grove 4 Channel I2C Mux
Supports the SwitchDoc Labs WXLink and Mini Pro LP

SunAirPlus - https://store.switchdoc.com/sunairplus-solar-controller-charger-sun-tracker-data-gathering-grove-header/
INA3221 - https://store.switchdoc.com/ina3221-breakout-board-3-channel-current-voltage-monitor-grove-headers-compare-to-ina219-grove-headers/
ADS1115 - http://store.switchdoc.com/grove-4-channel-16-bit-analog-to-digital-converter/
OurWeather - http://store.switchdoc.com/ourweather-complete-weather-kit/ 
Grove 4 CHannel I2C Mux - http://store.switchdoc.com/i2c-4-channel-mux-extender-expander-board-grove-pin-headers-for-arduino-and-raspberry-pi/
WXLink - http://store.switchdoc.com/wxlink-wireless-data-link-designed-for-the-weatherrack-and-the-weatherboard/


See the blog posting on www.switchdoc.com about setting up the DataLogger:
http://www.switchdoc.com/2016/06/datalogger-measuregraphlog-current-raspberry-pi/


To Install:

Install the following tools and libraries:

Installing MySQL
MySQL - Use the following tutorial:   http://pimylifeup.com/raspberry-pi-mysql-phpmyadmin/

and then install the python bindings:

sudo apt-get install python-mysqldb


Installing apscheduler 

sudo pip install setuptools --upgrade
sudo pip install apscheduler

Installing Apache

sudo apt-get install apache2 -y

Installing MatPlotLib


matplotlib - Install the following packages (This will take quite a while)

$ sudo apt-get install libblas-dev        ## 1-2 minutes

$ sudo apt-get install liblapack-dev      ## 1-2 minutes

$ sudo apt-get install python-dev        ## Optional

$ sudo apt-get install libatlas-base-dev ## Optional speed up execution

$ sudo apt-get install gfortran           ## 2-3 minutes

$ sudo apt-get install python-setuptools  ## ?

$ sudo easy_install scipy                 ## 2-3 hours

$ sudo apt-get install python-matplotlib  ## 1 hour


Installing httplib2

sudo apt-get install python-httplib2


Finally, copy DataLogger.html to /var/www/html

sudo cp DataLogger.html /var/www/html

and finally, set up the database:

Use phpmyadmin or sql command lines to add the included SQL file to your MySQL databases.

example: mysql -u root -p < DataLogger.sql

user: root

password: password

Obviously with these credentials, don't connect port 3306 to the Internet. Change them if you aren't sure.

Now you can run DataLogger

To Use:

Change the configuration variables to support your setup:
<pre>
# configuration variables
# set to true if present, false if not

INA3221_Present = True
ADS1115_Present = True
</pre>

To Add Devices:

1) Add a configuration Variable<BR>
2) Add device initialization code<BR>
3) Build your custom functions file containing the read device/MySQL code and the graph building function<BR>
4) Add your graph to the provided HTML file and copy it to /var/www/html<BR>


