# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 13:10:36 2020

@author: asche
"""

#!/usr/bin/env python3
#

import solaredge
import csv
import dropbox
import graphyte
import json
import time
import argparse
import sys
import os
import glob

def download_DBX_file(acToken,file,rpath,lpath):
    l = os.path.join(lpath,file)
    r = os.path.join('/',rpath,file)
    dbx = dropbox.Dropbox(acToken)
    dbx.files_download_to_file(l,r)
    print(glob.glob(l))
    #print(os.listdir(lpath))

def get_SE_values():
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
    print(energy, power)
    write_graphite(timestamp,energy,'Produktion')

def read_csv(file,path):
    csv_list = []
    with open(os.path.join(path,file)) as csvfile:
        reader = csv.DictReader(csvfile,['date','time','value'])
        for row in reader:
            csv_list.append(row)
    return csv_list
<<<<<<< Updated upstream

def write_graphite():
    print('GF')
=======
    
def eval_csvrow(csvrow):
    dt = csvrow['date'] + csvrow['time']
    time = datetime.datetime.strptime(dt, '%Y-%m-%d%H:%M:%S').timestamp()
    value = csvrow['value'].rstrip('.0')
    write_graphite(time,value,'HT')

def write_graphite(timestamp,metricvalue,metricname):
    #print(type(timestamp), type(metric))
    #print('GF')
    graphyte.init(graphite_host, prefix=graphite_pre)
    graphyte.send(metricname, int(metricvalue), timestamp=timestamp)
    #print(metricname, int(metricvalue), timestamp)
>>>>>>> Stashed changes

def cleanup(file,lpath):
    print(glob.glob(os.path.join(lpath,file)))
    os.remove(os.path.join(lpath,file))
    print(glob.glob(os.path.join(lpath,file)))
    print('Cleanup everything!')

# defaults; set these or use the command line options to override
dbxtoken = 'FQZNhbPIQmsAAAAAAAAMhMv5YG74Gz0Gd5AIp1sF0I2u1qEjtkOepaMziWyBfSVl'
dbxfile = 'VB Strom HT.csv'
localpath = '/tmp'
remotepath = 'VerbrauchsKosten/csv'
graphite_host = 'graphite'
graphite_port = 2003
<<<<<<< Updated upstream
graphite_pre = 'solar.pv'
apikey = 'SOLAREDGE_API_KEY'
site_id = 'XXXXXX'
=======
graphite_pre = 'test.pv'
apikey = 'OOJ241QVF0YZAOC3RI2ID0GK9N2GCABW'
site_id = '1156342'
>>>>>>> Stashed changes
time_pattern = '%Y-%m-%d %H:%M:%S'

parser = argparse.ArgumentParser(description='Reads output from SolarEdge portal and ECAS export (in Dropbox) and submits to Graphite')
parser.add_argument('-t', '--token', dest='dbxtoken', default=None, help='Dropbox Token') #add in default set section
parser.add_argument('-f', '--file', dest='dbxfile', default=None, help='Dropbox File')
parser.add_argument('-l', '--localpath', dest='localpath', default=None, help='Local Path to save DBX file')
parser.add_argument('-r', '--remotepath', dest='remotepath', default=None, help='Remote Path to DBX file')
parser.add_argument('-a', '--apikey', dest='apikey', default=None, help='SolarEdge API key')
parser.add_argument('-s', '--site', dest='site_id', default=None, help='SolarEdge site ID')
parser.add_argument('-g', '--graphitehost', dest='graphite_host', default=None, help='Graphite hostname')
parser.add_argument('-p', '--graphiteprefix', dest='graphite_pre', default=None, help='Graphite prefix')
parser.add_argument('--graphiteport', dest='graphite_port', default=None, help='Graphite line receiver port')
parser.add_argument('-n', '--null', action='store_true', default=False, help='no action (send zero)')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='debug (print metrics only)')
args = parser.parse_args()

if args.graphite_host:
    graphite_host = args.graphite_host
if args.graphite_pre:
    graphite_pre = args.graphite_pre
if args.graphite_port:
    graphite_port = args.graphite_port
if args.apikey:
    apikey = args.apikey
if args.site_id:
    site_id = args.site_id
    
download_DBX_file(dbxtoken, dbxfile, remotepath, localpath)
csvcontent = read_csv(dbxfile,localpath)
for row in csvcontent:
    print(row['date'], int(row['value'].rstrip('.0')))
print('Now we would upload each entry to graphite, right?')
<<<<<<< Updated upstream
=======
print('YEP!!! And start implementing the SolarEdge stuff!!')
get_SE_values()
>>>>>>> Stashed changes
cleanup(dbxfile,localpath)