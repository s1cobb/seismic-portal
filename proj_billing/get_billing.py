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
import misc_util

ssl._create_default_https_context = ssl._create_unverified_context

cmd_inputs = argparse.ArgumentParser()
cmd_inputs.add_argument('--devusage', help='Get Cisco License/Device Usage data', action='store_true')
cmd_inputs.add_argument('--confspace', help='Get Conference meeting data', action='store_true')
inputs = cmd_inputs.parse_args()

# setup logging 
logspk = logging.getLogger('spk_error_logger')

# get current date
currdate_info = {}
dat = datetime.now()

# load the billing configuration file
config_data = {}
try:
   with open('billing_config.csv', 'r') as fp:
      data = csv.DictReader(fp)
      for row in data:
         config_data[row['serv_cnt']] = row
         config_data[row['serv_cnt']]['month'] = dat.strftime('%B')
         config_data[row['serv_cnt']]['currdate'] = dat.strftime('%Y-%m-%d %H:%M:%S')
except IOError:
      logspk.error('Billing script failed to load configuration file, script not started.') 
      sys.exit()


for server in config_data.keys():
   if config_data[server]['target'] == 'CUCM':
      # process the AXL Devices/Usage data
      if inputs.devusage:
         #dev_url  = 'https://' + config_data[server]['ip_address'] + ':8443/axl/'
         dev_url = 'http://' + config_data[server]['ip_address'] + ':' + config_data[server]['port'] + '/api/cucm'
         rsp = ''

         try:
            rsp = misc_util.axl_data_request(url=dev_url, req_type='devices',
                                             usr=config_data[server]['axlusr'],
                                             pw=config_data[server]['axlpwd'])
         except (urllib2.HTTPError, urllib2.URLError) as e:
            misc_util.log_message(logspk, config_data[server],
                                   ' with HTTP call to Call Manager', 'sys_error', e)
         if not rsp:
            misc_util.log_message(logspk, config_data[server],
                                   'No XML data returned from Call Manager', 'error')
         else:
            # Data from device/usage Api processed, logged here 
            parse_billing = ProcessXML('devices', rsp, config_data[server])
            parse_billing.process_xml() 
         time.sleep(3)
   elif config_data[server]['target'] == 'CMS':
      if inputs.confspace:
         # get the conference space data
         #conf_url = 'https://' + config_data[server]['ip_address'] + '/api/v1/coSpaces'
         conf_url = 'http://' + config_data[server]['ip_address'] + ':' + config_data[server]['port'] + '/api/v1/coSpaces' 
         rsp = ''

         try:
            rsp = misc_util.axl_data_request(url=conf_url, req_type='conf_spaces',
                                             usr=config_data[server]['axlusr'],
                                             pw=config_data[server]['axlpwd'])
         except (urllib2.HTTPError, urllib2.URLError) as e: 
            misc_util.log_message(logspk, config_data[server],
                                   ' with HTTP call to Cisco Meeting Server', 'sys_error', e)
         if not rsp:
            misc_util.log_message(logspk, config_data[server],
                                   'No XML data returned from Cisco Meeting Server', 'error')
         else:
            # Data from conferences spaces processed, logged here  
            parse_billing = ProcessXML('conf_spaces', rsp, config_data[server])
            parse_billing.process_xml()
         time.sleep(3)

sys.exit(1)
