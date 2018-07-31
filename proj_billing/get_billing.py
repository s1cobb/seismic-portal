#!/usr/bin/python

import sys
import logging
import xml.sax
import requests
import argparse
import mysql.connector as mariadb
from logging.handlers import RotatingFileHandler

# user created library
from BillingUtil import ProcessXML

db_conn = None
cursor  = None

cmd_inputs = argparse.ArgumentParser()
cmd_inputs.add_argument('--devusage',   help='Get the number of Cisco License/Device Usage', action='store_true')
cmd_inputs.add_argument('--confspaces', help='Get the number of Cisco Conference spaces',    action='store_true')
inputs = cmd_inputs.parse_args()

# setup logging, will log to file and rotate files
logit = logging.getLogger('my_logger')
logit.setLevel(logging.DEBUG)
logfor = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fh = RotatingFileHandler('/root/billing/logs/device_conf.log', maxBytes=500000, backupCount=20)
fh.setFormatter(logfor)
logit.addHandler(fh)

# urls for data fetching
dev_url  = 'https://10.207.200.82:8443/axl/'
conf_url = 'https://10.207.200.84/api/v1/coSpaces'
soap_header = { 'content-type':'text/xml', 'SOAPAction':'CUCM:DB ver=11.5'}

# device/usage AXL request
dev_axl_req = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/11.5">'
dev_axl_req += '<soapenv:Header/><soapenv:Body><ns:executeSQLQuery sequence="">'
dev_axl_req += '<sql>select name,value FROM TABLE (FUNCTION LicenseTotals()) (pkid,name,value,UserValue,DeviceValue)</sql>'
dev_axl_req += '</ns:executeSQLQuery></soapenv:Body></soapenv:Envelope>'

# setup database connection
try:
   db_conn = mariadb.connect(database='Billing')
   cursor  = db_conn.cursor()
except mariadb.Error as db_error:
   logit.error(" Database connection issue: %s" % db_error)

# process the AXL Devices/Usage data
if inputs.devusage:
   try:
       rsp = requests.post(dev_url, auth=('usr','pw'), headers=soap_header, data=dev_axl_req, verify=False)

       if not rsp.text:
          logit.error('**** No XML data returned from the Web API request for device/usage report')
       else:
           # Data from device/usage Api processed, logged here
           if rsp.text:
               logit.info('***************************************************************')
               logit.info('\nFetching of Device/Usage XML data - successful')
               parse_billing = ProcessXML('devices',rsp.text, db_conn, cursor )
               parse_billing.process_xml()
   except OSError as e:
       logit.error('errno: %d: %s' % (e.errno, e.strerror))

# process the AXL conference room data
if inputs.confspaces:
   try:
       rsp = requests.get(conf_url, auth=('usr','pw'), headers=soap_header, data=dev_axl_req, verify=False)

       if not rsp.text:
           logit.error('**** No XML data returned from the Web API request for conference space report')
       else:
          # Data from conference spaces processed, logged here
          if rsp.text:
              logit.info('\nFetching of Conference Room XML data - successful')
              parse_billing = ProcessXML('conf_spaces',rsp.text, db_conn, cursor )
              parse_billing.process_xml()
              logit.info('*******************************************************************')
   except OSError as e:
       logit.error('errno: %d: %s' % (e.errno, e.strerror))

db_conn.close()
sys.exit(1)
