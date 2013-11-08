#!/usr/bin/env python

#
# Roberto J. R. Paz
# 2013-11-08
#
# This script reads time data from DS1307.
# RTC is connected using i2c as a slave
# i2c address is 0x68.
#
# Must be executed as superuser
#

import smbus
import time
import sys

# RPI version 1 => "bus = smbus.SMBus(0)"
# RPI version 2 => "bus = smbus.SMBus(1)"
bus = smbus.SMBus(0)
 
# Direccion del RTC
address = 0x68
 
def format(value):
    return ((value>>4 & 0x0f) * 10 + (value & 0x0f))

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

data = [0, 0, 0, 0, 0, 0]

stay = 0
if (len(sys.argv) == 2):
    if (sys.argv[1] == "-i"):
        stay = 1
    else:
        print "Use: \n";
        print "\t" + str(sys.argv[0]) + " [-i|-h]\n";
        print "\t\t-h: this help\n";
        print "\t\t-i: continuous mode\n";
        sys.exit(0)

while True:
    var = 0x0
    bus.write_byte(address, var)

    # seg, min, hour
    for i in range(0, 3):
    	data[i] = readNumber()
    	data[i] = format(data[i])

    # discard dow
    readNumber()

    # day, month, year
    for i in range(3, 6):
    	data[i] = readNumber()
    	data[i] = format(data[i])

    print ("20%02d-%02d-%02d %02d:%02d:%02d" % (data[5], data[4], data[3], data[2], data[1], data[0]))

    if (not stay):
	sys.exit(0)

    time.sleep(1)

