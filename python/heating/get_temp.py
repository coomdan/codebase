import sys
import time
import os
import platform
import subprocess
from socket import socket
import re

#change this to your carbon server and port
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

#get the sensor ids into an array
w1Slaves = open("/sys/devices/w1_bus_master1/w1_master_slaves", "r")
listOfSensors = w1Slaves.read().splitlines()
w1Slaves.close()

i = 0
sensorData = []
for sensor in listOfSensors:
    crc = '';
    #ensure we get valid data (crc must = yes)
    while crc.split("\n")[0].find("YES") == -1:
        currentSensor = open("/sys/devices/w1_bus_master1/%(sensor)s/w1_slave" % locals(), "r")
        data=currentSensor.readlines()
        currentSensor.close()

        #split the two lines into two variables
        crc=data[0]
        temp=data[1]

        currentReading = re.search(r't=.\d*', "%(temp)s" % locals())
        i+1

        #convert to a reasonable number, ie 12.02
        sensorData.append((float(currentReading.group().replace('t=','')))* .001)


sock = socket()
try:
    sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
    print "Couldn't connect to %(server)s on port %(port)d, is carbon running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
    sys.exit(1)

now = int( time.time() )
lines = []
i = 0
for sensor in listOfSensors:
    lines.append("%s %s %d" % (sensor,sensorData[i],now))   
    i=i+1


message = '\n'.join(lines) + '\n' #all lines must end in a newline
#print "sending message\n"
#print '-' * 80
#print message
#print
sock.sendall(message)
