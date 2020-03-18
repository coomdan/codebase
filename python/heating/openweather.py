#!/usr/bin/python
import requests
import json
import sys
import os
import time
import datetime
from socket import socket

#CARBON_SERVER = 'raspy.fritz.box'
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
apikey = "b60767ab6059b9b7f2226433d9cc5bee"
apilocid = "2893328"
#apiurl="http://api.openweathermap.org/data/2.5/weather?id=2893328&mode=json&units=metric&APPID=b60767ab6059b9b7f2226433d9cc5bee"
apiurl="http://api.openweathermap.org/data/2.5/weather?id=" + apilocid +"&mode=json&units=metric&APPID=" + apikey

delay = 20
if len(sys.argv) > 1:
  delay = int( sys.argv[1] )

pid = str(os.getpid())
pidfile = "/tmp/openweather2carbon.pid"

if os.path.isfile(pidfile):
  print str(datetime.datetime.now()) + " - %s already exists, exiting" % pidfile
  sys.exit()
file(pidfile, 'w').write(pid)

try:
  while True:
    r = requests.get(apiurl)
    j = json.loads(r.text)
    temperature = j['main']['temp']
    #print temperature
    sock = socket()
    try:
      sock.connect( (CARBON_SERVER,CARBON_PORT) )
    except:
      print "Couldn't connect to %(server)s on port %(port)d, is carbon running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
      sys.exit(1)
    now = int( time.time() )
    message = "asche.openweather.temperature " + str(temperature) + " " + str(now) + "\n"
    sock.sendall(message)

    time.sleep(int(delay))
    
finally:
  os.unlink(pidfile)
