Raspberry Pi DataLogger
SwitchDoc Labs
June 01, 2016: Set up to measure current using Grove INA3221 3 channel Current Measuring Breakout Board and display with MatPlotLib
June 11, 2016: Set up to measure voltage using Grove ADS1115 4 Channel 16 Bit ADC Board
June 15, 2016: Added configuration variables
June 18, 2016: Installed OurWeather suppot / Fixed multiple graph generation

Supports the INA3221 Grove Breakout Board or SunAirPlus on switchdoc.com
Supports the ADS1115 Grove Breakout Board on switchdoc.com
Supports the OurWeather Full Weather Kit

SunAirPlus - https://store.switchdoc.com/sunairplus-solar-controller-charger-sun-tracker-data-gathering-grove-header/
INA3221 - https://store.switchdoc.com/ina3221-breakout-board-3-channel-current-voltage-monitor-grove-headers-compare-to-ina219-grove-headers/
ADS1115 - http://store.switchdoc.com/grove-4-channel-16-bit-analog-to-digital-converter/
OurWeather - http://store.switchdoc.com/ourweather-complete-weather-kit/ 

See the blog posting on www.switchdoc.com about setting up the DataLogger:
http://www.switchdoc.com/2016/06/datalogger-measuregraphlog-current-raspberry-pi/


To Install:

Install the following tools and libraries:

Installing MySQL
MySQL - Use the following tutorial:   http://pimylifeup.com/raspberry-pi-mysql-phpmyadmin/


Installing apscheduler 

sudo pip install setuptools --upgrade
sudo pip install apscheduler

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

sudo cp Datalogger.html /var/www/html

Now you can run DataLogger

To Use:

Change the configuration variables to support your setup:

# configuration variables
# set to true if present, false if not

INA3221_Present = True
ADS1115_Present = True

To Add Devices:

1) Add a configuration Variable
2) Add device initialization code
3) Build your custom functions file containing the read device/MySQL code and the graph building function
4) Add your graph to the provided HTML file and copy it to /var/www/html


