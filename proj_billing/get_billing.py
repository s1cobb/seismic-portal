#!/usr/bin/python

import os
import sys
import smtplib
import logging
import xml.sax
import requests
import argparse
import mysql.connector as mariadb
from email.mime.text import MIMEText
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

# setup logging, will log errors only/rotate files for splunk auditing
logspk = logging.getLogger('splunk_logger')
logspk.setLevel(logging.DEBUG)
spklogfor = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fh2 = RotatingFileHandler('/root/billing/logs/devconf_error.log', maxBytes=500000, backupCount=10)
fh2.setFormatter(spklogfor)
logspk.addHandler(fh2)

# urls for data fetching
dev_url  = 'https://url:8443/axl/'
conf_url = 'https://url/api/v1/coSpaces'
soap_header = { 'content-type':'text/xml', 'SOAPAction':'CUCM:DB ver=11.5'}

# device/usage AXL request
dev_axl_req = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"'
dev_axl_req += ' xmlns:ns="http://www.cisco.com/AXL/API/11.5">'
dev_axl_req += '<soapenv:Header/><soapenv:Body><ns:executeSQLQuery sequence="">'
dev_axl_req += '<sql>select name,value FROM TABLE (FUNCTION LicenseTotals())'
dev_axl_req += ' (pkid,name,value,UserValue,DeviceValue)</sql>'
dev_axl_req += '</ns:executeSQLQuery></soapenv:Body></soapenv:Envelope>'

# setup database connection
try:
   db_conn = mariadb.connect(database='Billing')
   cursor  = db_conn.cursor()
except mariadb.Error as db_error:
   logit.error("\033[1;31;40m Database connection issue: %s " \
               "\033[0;37;40m" % db_error)
   logspk.error("\033[1;31;40m Database connection issue: %s " \
                "\033[0;37;40m" % db_error)

# process the AXL Devices/Usage data
if inputs.devusage:
    rsp = requests.post(dev_url, auth=('usr','pw'), 
                        headers=soap_header, data=dev_axl_req, verify=False)

    if not rsp.text:
       logit.error("\033[1;31;40m **** No XML data returned from the Web API request " \
                   "for device/usage report \033[0;37;40m")
       logspk.error("\033[1;31;40m **** No XML data returned from the Web API request " \
                    "for device/usage report \033[0;37;40m")
    else:
       # Data from device/usage Api processed, logged here 
       if rsp.text:
           logit.info('***************************************************************')
           logit.info('\nFetching of Device/Usage XML data - successful')
           parse_billing = ProcessXML('devices',rsp.text, db_conn, cursor )
           parse_billing.process_xml() 

# process the AXL conference room data
if inputs.confspaces:
    rsp = requests.get(conf_url, auth=('usr','pw'), 
                                       headers=soap_header, data=dev_axl_req, verify=False)

    if not rsp.text:
       logit.error("\033[1;31;40m **** No XML data returned from the Web API request for " \
                   "conference space report \033[0;37;40m")
       logspk.error("\033[1;31;40m **** No XML data returned from the Web API request for " \
                    " conference space report \033[0;37;40m")
    else:
       # Data from conferences spaces processed, logged here  
       if rsp.text:
           logit.info('\nFetching of Conference Room XML data - successful') 
           parse_billing = ProcessXML('conf_spaces',rsp.text, db_conn, cursor )
           parse_billing.process_xml()
           logit.info('*******************************************************************')

if db_conn:
   db_conn.close()

sys.exit(1)
