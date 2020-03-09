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
import datetime
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

def read_csv(file,path):
    csv_list = []
    with open(os.path.join(path,file)) as csvfile:
        reader = csv.DictReader(csvfile,['date','time','value'])
        for row in reader:
            csv_list.append(row)
            eval_csvrow(row)
    return csv_list
    
def eval_csvrow(csvrow):
    dt = csvrow['date'] + csvrow['time']
    #print(dt)
    time = datetime.datetime.strptime(dt, '%Y-%m-%d%H:%M:%S').timestamp()
    #print(time)
    #print("Call upload2graphite with " + str(time), csvrow['value'])
    value = csvrow['value'].rstrip('.0')
    write_graphite(time,value)

def write_graphite(timestamp,metric):
    #print(type(timestamp), type(metric))
    #print('GF')
    graphyte.init(graphite_host, prefix=graphite_pre)
    graphyte.send('ht', int(metric), timestamp=timestamp)
    print('ht', int(metric), timestamp)

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
graphite_host = 'raspy.fritz.box'
graphite_port = 2003
graphite_pre = 'test.pv'
apikey = 'SOLAREDGE_API_KEY'
site_id = 'XXXXXX'
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
#for row in csvcontent:
#    print(row['date'], int(row['value'].rstrip('.0')))
print('Now we would upload each entry to graphite, right?')
print('YEP!!! And start implementing the SolarEdge stuff!!')
cleanup(dbxfile,localpath)