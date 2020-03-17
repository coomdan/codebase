# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 17:31:20 2020

@author: asche
"""

#!/usr/bin/env python3
#
## Imports
import argparse
import datetime
import dropbox
import glob
import graphyte
import json
import os
import sys
import solaredge
import sqlite3
import time
import urllib.request
import xml.etree.ElementTree as ET

"""
Functions
"""

def cleanup(file,lpath):
    # Cleanup files    
    print(glob.glob(os.path.join(lpath,file)))
    os.remove(os.path.join(lpath,file))
    print(glob.glob(os.path.join(lpath,file)))
    print('Cleanup everything!')

def vartametrics(url,ghost,prefix='pv.varta'):
    # read from Storage
    with urllib.request.urlopen(url) as response: ## Add Exception Handler
        xml = response.read()
    root = ET.fromstring(xml)
    # parse xml
    timestamp = root.attrib['Timestamp']
    state = root.find("./inverter[@id='M460879']/var[@name='State']")
    power = root.find("./inverter[@id='M460879']/var[@name='P']")
    charge = root.find("./inverter[@id='M460879']/var[@name='SOC']")
    if charge.attrib['value'] == '0':
        c = 0
    else:
        c = charge.attrib['value'][:-1]
        
    print('Timestamp: {}, Status:  {}, Power: {}W, Ladung: {}%'.format(timestamp, state.attrib['value'],power.attrib['value'],c))
    #write_graphite(prefix,int(timestamp),charge.attrib['value'].rstrip('0'),'Ladung',ghost)
    write_graphite(prefix,int(timestamp),state.attrib['value'],state.attrib['name'],ghost)
    write_graphite(prefix,int(timestamp),power.attrib['value'],power.attrib['name'],ghost)
    write_graphite(prefix,int(timestamp),c,charge.attrib['name'],ghost)
        
def download_DBX_file(token,file,rpath,lpath):
    l = os.path.join(lpath,file)
    r = os.path.join('/',rpath,file)
    ## Add Exception Handler
    dbx = dropbox.Dropbox(token)
    dbx.files_download_to_file(l,r)
    #print(glob.glob(l))

def se_hourly(apikey,site_id,ghost,prefix='pv.solaredge.production'):
    timestamp = int(round(time.time()))
    today = 0
    s = solaredge.Solaredge(apikey)
    try: 
        r = s.get_overview(site_id)
    except:
        print("Unexpected error accessing SolarEdge portal:", sys.exc_info()[0])
        raise
    o = r["overview"]
    timestamp = int(time.mktime(time.strptime(o["lastUpdateTime"], time_pattern)))
    today = o['lastDayData']['energy']
    write_graphite(prefix,timestamp,today,'today',ghost)
    
def se_daily(apikey,site_id,ghost,prefix='pv.solaredge.production'):
    timestamp = int(round(time.time()))
    energy = float('nan')
    s = solaredge.Solaredge(apikey)
    try: 
        r = s.get_overview(site_id)
    except:
        print("Unexpected error accessing SolarEdge portal:", sys.exc_info()[0])
        raise
    o = r["overview"]
    timestamp = int(time.mktime(time.strptime(o["lastUpdateTime"], time_pattern)))
    energy = o["lifeTimeData"]["energy"]
    #print("Lifetime: {} Wh".format(energy))
    write_graphite(prefix,timestamp,energy,'total',ghost)
    
def solaredgemetrics():
    print('SE')
    timestamp = int(round(time.time()))
    energy = float('nan')
    power = 0
    s = solaredge.Solaredge(apikey)
    try: 
        r = s.get_overview(site_id)
    except:
        print("Unexpected error accessing SolarEdge portal:", sys.exc_info()[0])
        raise
    o = r["overview"]
    timestamp = int(time.mktime(time.strptime(o["lastUpdateTime"], time_pattern)))
    energy = o["lifeTimeData"]["energy"]
    power = o["currentPower"]["power"]
    today = o['lastDayData']['energy']
    #print("Current: {} W, Today: {} Wh, Lifetime: {} Wh".format(power, today, energy))
    write_graphite(timestamp,energy,'Produktion')
    write_graphite(timestamp,power,'Power')
    write_graphite(timestamp,today,'Today')

def write_graphite(prefix,timestamp,metricvalue,metricname,host): ## Add metric path / prefix
    ## Add Exception Handler
    graphyte.init(host, prefix=prefix)
    #print(metricname, int(metricvalue))
    graphyte.send(metricname, int(metricvalue), timestamp=timestamp)

"""
Args
"""
parser = argparse.ArgumentParser(description='Reads status from SolarEdge portal, Varta storage and ECAS export (in Dropbox) and submits to Graphite')
parser.add_argument('-a', '--apikey',
                    dest='apikey',
                    default=None,
                    required=True,
                    help='SolarEdge API key')

parser.add_argument('-f', '--file',
                    dest='dbxfile',
                    default=None,
                    help='Dropbox File Name') #set default to today's filename ('2020-03-13-ecas-export.db')
parser.add_argument('-g', '--graphitehost',
                    dest='graphite_host',
                    default='raspy.fritz.box',
                    help='Graphite hostname')
parser.add_argument('-l', '--localpath',
                    dest='localpath',
                    default='/tmp',
                    help='Local Path to save DBX file')
parser.add_argument('-m', '--mode',
                    dest='mode',
                    type=int,
                    default=1,
                    help='Program mode: 1 - 15 min values, 2 - hourly, 3 - daily')                    
parser.add_argument('-r', '--remotepath',
                    dest='remotepath',
                    default=None,
                    required=True,
                    help='Remote Path to DBX file')
parser.add_argument('-s', '--site',
                    dest='site_id',
                    default=None,
                    required=True,
                    help='SolarEdge site ID')
parser.add_argument('-t', '--token',
                    dest='dbxtoken',
                    default=None,
                    required=True,
                    help='Dropbox Token')
parser.add_argument('-x', '--xmlurl',
                    dest='vartaurl',
                    default=None,
                    required=True,
                    help='URL to Varta state XML file')
#parser.add_argument('-', '--graphiteprefix', dest='graphite_pre', default=None, help='Graphite prefix')
parser.add_argument('-p', '--graphiteport',
                    dest='graphite_port',
                    default=2003,
                    help='Graphite line receiver port')
args = parser.parse_args()

## set vars
graphite_host = args.graphite_host
time_pattern = '%Y-%m-%d %H:%M:%S'

## main
if args.mode == 1:
    vartametrics(args.vartaurl,graphite_host)
    se_hourly(args.apikey,args.site_id,graphite_host)
    se_daily(args.apikey,args.site_id,graphite_host)
elif args.mode == 2:
    se_hourly(args.apikey,args.site_id,graphite_host)
    se_daily(args.apikey,args.site_id,graphite_host)
elif args.mode == 3:
    se_daily(args.apikey,args.site_id,graphite_host)
else:
    print('Invalid mode, exiting...')
    sys.exit(2)