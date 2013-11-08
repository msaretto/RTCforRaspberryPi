#!/usr/bin/python

#
# Roberto J. R. Paz
# 2013-11-08
#
# This script writes time data to DS1307.
# RTC is connected using i2c as a slave
# i2c address is 0x68.
#
# Date argument must be formatted as: "%y-%m-%d %H:%M:%S"
# (must include ")
# Must be executed as superuser
#

import smbus
import time
import sys
import re

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(0)
 
# Direccion del RTC
address = 0x68
 
def formatAndWrite(reg, data):
	data = ((int(data) / 10) << 4) + ((int(data) % 10) & 0x0f)
	bus.write_byte_data(address, reg, data)

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1
 
def usage():
	print "Use: \n";
	print "\t" + str(sys.argv[0]) + " \"13-02-11 13:14:01\"\n\n";
	sys.exit(0)
 
if (len(sys.argv) != 2):
	usage()

data = re.search(r"(\d{2})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})", sys.argv[1])

if data:
	for i in range(0,3):
		formatAndWrite(i, int(data.group(6-i)))
	for i in range(4,7):
		formatAndWrite(i, int(data.group(6-i+1)))
else:
	print "Mal formato\n"
	usage()

