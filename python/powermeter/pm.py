# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:09:19 2020

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
    
def current_dbx_file_exists(acToken,file,path):
    dbx = dropbox.Dropbox(acToken)
    print('Trying to get ' + str(os.path.join('/',path,file)))
    try:
        dbx.files_get_metadata(os.path.join('/',path,file))
        return True
    except:
        return False
        
        
dbxtoken = 'FQZNhbPIQmsAAAAAAAAMhMv5YG74Gz0Gd5AIp1sF0I2u1qEjtkOepaMziWyBfSVl'
#dbxfile = '2020-03-21-ecas-export.db'
localpath = '/tmp'
remotepath = 'VerbrauchsKosten/ECAS'

now = datetime.datetime.now()
dbxfile = now.strftime("%Y-%m-%d") + "-ecas-export.db"
#print(dbxfile)

# build current file (YYYY-mm-dd-ecas-export.db) from date
if current_dbx_file_exists(dbxtoken,dbxfile,remotepath):
    print('get current file')
    # get current (daily) file
    # read and upload current file
else:
    print('No current file')

# SE hopurly
# s.get_energy_details for meter in r['energyDetails']['meters']:
# read get_overview today = o['lastDayData']['energy']

# Varta quarter hourly
'''
    state = root.find("./inverter[@id='M460879']/var[@name='State']")
    power = root.find("./inverter[@id='M460879']/var[@name='P']")
    charge = root.find("./inverter[@id='M460879']/var[@name='SOC']")
'''