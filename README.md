Raspberry Pi DataLogger
SwitchDoc Labs
June 2016

Set up to measure current using INA3221 3 channel Current Measuring Breakout Board and display with MatPlotLib

Uses the INA3221 Grove Breakout Board or SunAirPlus on switchdoc.com

SunAirPlus - https://store.switchdoc.com/sunairplus-solar-controller-charger-sun-tracker-data-gathering-grove-header/
INA3221 - https://store.switchdoc.com/ina3221-breakout-board-3-channel-current-voltage-monitor-grove-headers-compare-to-ina219-grove-headers/


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


Finally, copy DataLogger.html to /var/www/html

sudo cp Datalogger.html /var/www/html

Now you can run DataLogger
