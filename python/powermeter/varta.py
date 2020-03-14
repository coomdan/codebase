# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 21:09:57 2020

@author: asche
"""

import urllib.request
import xml.etree.ElementTree as ET

with urllib.request.urlopen('http://192.168.1.51/cgi/ems_data.xml') as response:
   xml = response.read()
#print(xml)



root = ET.fromstring(xml)
print(root.tag,root.attrib)
timestamp = root.attrib['Timestamp']
state = root.find("./inverter[@id='M460879']/var[@name='State']")
power = root.find("./inverter[@id='M460879']/var[@name='P']")
charge = root.find("./inverter[@id='M460879']/var[@name='SOC']")

st = state.attrib['value']
#print(st)

print(timestamp, state.attrib['value'],power.attrib['value'],charge.attrib['value'])