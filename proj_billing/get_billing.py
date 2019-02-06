#!/usr/bin/python

'''
   Filename: get_billing.py
   Version: Python 2.7.5
   Author: Steve Cobb (stcobb@cisco.com)
   Description:
        This script will retrieve the License/Device usage from the
        Call Manager and the Conference configuration from the Cisco
        Meeting Server.

        A web request is sent to each device and a XML response is
        returned, which is parsed before sending to log files and
        database.

        This script will be run from cron. 

        Example: get_billing.py --devusage --confspace 

'''

import os
import sys
import csv 
import ssl
import time
import logging
import xml.sax
import urllib2
import argparse
from datetime import datetime

# user created library
from BillingUtil import ProcessXML
from DataBaseUtil import DataDB
import misc_util

ssl._create_default_https_context = ssl._create_unverified_context

cmd_inputs = argparse.ArgumentParser()
cmd_inputs.add_argument('--devusage', help='Get Cisco License/Device Usage data', action='store_true')
cmd_inputs.add_argument('--confspace', help='Get Conference meeting data', action='store_true')
inputs = cmd_inputs.parse_args()

# setup logging, will log data to file and rotate files
logspk = logging.getLogger('spk_error_logger')

# initialize database access
db_access = DataDB(logspk)

cucm_usr = 'StcobbAXL'
cucm_pw = 'fsp-WWcs!1'

# Soap AXL request setup
soap_header = { 'content-type':'text/xml', 'SOAPAction':'CUCM:DB ver=11.5'}
dev_axl_req = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"'
dev_axl_req += ' xmlns:ns="http://www.cisco.com/AXL/API/11.5">'
dev_axl_req += '<soapenv:Header/><soapenv:Body><ns:executeSQLQuery sequence="">'
dev_axl_req += '<sql>select name,value FROM TABLE (FUNCTION LicenseTotals())'
dev_axl_req += ' (pkid,name,value,UserValue,DeviceValue)</sql>'
dev_axl_req += '</ns:executeSQLQuery></soapenv:Body></soapenv:Envelope>'

# get current date
currdate_info = {}
dat = datetime.now()

# load the billing configuration file
config_data = {}
try:
   with open('billing_config.csv', 'r') as fp:
      data = csv.DictReader(fp)
      for row in data:
         config_data[row['ser_type']] = row
         config_data[row['ser_type']]['month'] = dat.strftime('%B')
         config_data[row['ser_type']]['currdate'] = dat.strftime('%Y-%m-%d %H:%M:%S')
except IOError:
      logspk.error('Billing script failed to load configuration file, script not started.') 
      sys.exit()


for server in config_data.keys():
   if config_data[server]['target'] == 'CUCM':
      # process the AXL Devices/Usage data
      if inputs.devusage:
         dev_url  = 'https://' + config_data[server]['ip_address'] + ':8443/axl/'
         rsp = ''

         try:
            rsp = misc_util.axl_data_request(url=dev_url, add_header=soap_header,
                                              data=dev_axl_req, usr=cucm_usr, pw=cucm_pw)
         except (urllib2.HTTPError, urllib2.URLError) as e:
            misc_util.log_message(logspk, config_data[server],
                                   'Error with HTTP call to Call Manager', 'sys_error', e)
         if not rsp:
            misc_util.log_message(logspk, config_data[server],
                                   'No XML data returned from Call Manager', 'error')
         else:
            # Data from device/usage Api processed, logged here 
            parse_billing = ProcessXML('devices', rsp, db_access, config_data[server])
            parse_billing.process_xml() 
         time.sleep(3)
   elif config_data[server]['target'] == 'CMS':
      if inputs.confspace:
         # get the conference space data
         conf_url = 'https://' + config_data[server]['ip_address'] + '/api/v1/coSpaces'
         rsp = ''

         try:
            rsp = misc_util.axl_data_request(url=conf_url, add_header=soap_header, usr=cucm_usr, pw=cucm_pw)
         except (urllib2.HTTPError, urllib2.URLError) as e: 
            misc_util.log_message(logspk, config_data[server],
                                   'ERROR with HTTP call to Cisco Meeting Server', 'sys_error', e)
         if not rsp:
            misc_util.log_message(logspk, config_data[server],
                                   'No XML data returned from Cisco Meeting Server', 'error')
         else:
            # Data from conferences spaces processed, logged here  
            parse_billing = ProcessXML('conf_spaces', rsp, db_access, config_data[server])
            parse_billing.process_xml()
         time.sleep(3)

db_access.close_db_access()
sys.exit(1)
