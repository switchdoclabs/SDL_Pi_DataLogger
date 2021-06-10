#!/usr/bin/python

#SwitchDoc Labs May 2016
#
# reads all four channels from the Grove4Ch16BitADC Board in single ended mode
# also reads raw values
#


from __future__ import print_function
import time, signal, sys

from MADS1x15 import ADS1x15

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

ADS1115 = 0x01  # 16-bit ADC

# Select the gain
gain = 6144  # +/- 6.144V
#gain = 4096  # +/- 4.096V
# gain = 2048  # +/- 2.048V
# gain = 1024  # +/- 1.024V
# gain = 512   # +/- 0.512V
# gain = 256   # +/- 0.256V

# Select the sample rate
# sps = 8    # 8 samples per second
# sps = 16   # 16 samples per second
# sps = 32   # 32 samples per second
# sps = 64   # 64 samples per second
# sps = 128  # 128 samples per second
sps = 250  # 250 samples per second
# sps = 475  # 475 samples per second
# sps = 860  # 860 samples per second

# Initialise the ADC using the default mode (use default I2C address)
adc = ADS1x15(ic=ADS1115)
while (1):

        # Read channels  in single-ended mode using the settings above

        print("--------------------")
        voltsCh0 = adc.readADCSingleEnded(0, gain, sps) / 1000
        rawCh0 = adc.readRAW_ADCSingleEnded(0, gain, sps)
        print("Channel 0 =%.6fV raw=%d raw=0x%4X" % (voltsCh0, rawCh0, rawCh0))

        voltsCh1 = adc.readADCSingleEnded(1, gain, sps) / 1000
        rawCh1 = adc.readRAW_ADCSingleEnded(1, gain, sps)

	# O2 Sensor
        sensorVoltage = voltsCh1 *(5.0/6.144)
	AMP  = 121
	K_O2  = 7.43
    	sensorVoltage = sensorVoltage/AMP*10000.0
    	Value_O2 = sensorVoltage/K_O2 - 1.05
	print("Channel 1 =%.6fV raw=0x%4X O2 Percent=%6.2f" % (voltsCh1, rawCh1, Value_O2))

        voltsCh2 = adc.readADCSingleEnded(2, gain, sps) / 1000
        rawCh2 = adc.readRAW_ADCSingleEnded(2, gain, sps)
        print("Channel 2 =%.6fV raw=0x%4X" % (voltsCh2, rawCh2))

        voltsCh3 = adc.readADCSingleEnded(3, gain, sps) / 1000
        rawCh3 = adc.readRAW_ADCSingleEnded(3, gain, sps)
        print("Channel 3 =%.6fV raw=0x%4X" % (voltsCh3, rawCh3))
        print("--------------------")

        time.sleep(0.5)

