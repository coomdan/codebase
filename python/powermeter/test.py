# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:05:10 2020

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

apikey = 'OOJ241QVF0YZAOC3RI2ID0GK9N2GCABW'
site_id = 1156342
time_pattern = '%Y-%m-%d %H:%M:%S'


def write_graphite(prefix,timestamp,metricvalue,metricname,host): ## Add metric path / prefix
    ## Add Exception Handler
    graphyte.init(host, prefenergy = o["lifeTimeData"]["energy"]ix=prefix)
    #print(metricname, int(metricvalue))
    graphyte.send(metricname, int(metricvalue), timestamp=timestamp)

def se(apikey,site_id,starttime,endtime):
    timestamp = int(round(time.time()))
    energy = float('nan')
    s = solaredge.Solaredge(apikey)
    try: 
        r = s.get_energy_details(site_id, starttime, endtime)
    except:
        print("Unexpected error accessing SolarEdge portal:", sys.exc_info()[0])
        raise
    for meter in r['energyDetails']['meters']:
        print(meter['type'])
        for value in meter['values']:
            timestamp = int(time.mktime(time.strptime(value["date"], time_pattern)))
            print('Update Graphite: {} {} {}'.format(meter['type'],value['value'],timestamp))
            write_graphite('pv.solaredge',timestamp,value['value'],meter['type'],'raspy.fritz.box')
    #print(r)
    #o = r["overview"]
    #timestamp = int(time.mktime(time.strptime(o["lastUpdateTime"], time_pattern)))
    #energy = o["lifeTimeData"]["energy"]
    
#print(dir(solaredge.Solaredge))
for d in ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18']:
    startdate = '2020-03-' + d + ' 00:00:00'
    enddate = '2020-03-' + d + ' 23:59:59'
    print(startdate, enddate)
    se(apikey,site_id,startdate,enddate)
#day = '2020-03-16'
#startdate = day + ' 00:00:00'
#enddate = day + ' 23:59:59'
#se(apikey,site_id,startdate,enddate)