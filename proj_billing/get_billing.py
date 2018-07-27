#!/usr/bin/python

import sys
import logging
import xml.sax
import argparse
import mysql.connector as mariadb
from subprocess import Popen, PIPE
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

try:
   db_conn = mariadb.connect(database='Billing')
   cursor  = db_conn.cursor()
except mariadb.Error as db_error:
   logit.error(" Database connection issue: %s" % db_error)

# process the AXL conference room/Devices/Usage data
if inputs.devusage:
   try:
       proc = Popen('curl -k -s -u "administrator:fsp-WWcs!1" -H "Content-type: text/xml;" -H "SOAPAction:CUCM:DB ver=11.5" -d @LicUsageRequest.xml https://10.207.200.82:8443/axl/', stdout=PIPE, shell=True)
       output, err = proc.communicate()

       #  err = None if no errors returned from SOAP call
       if err:
          logit.error('%d: %s' % (proc.returncode, err.strip()))
       elif proc.returncode != 0 and not err:
          logit.error('*** Retrieve devices - No error msg returned, Unknown error occurred, retcode: %d' % proc.returncode)
       else:
           # Data from device/usage Api processed, logged here 
           if output:
               logit.info('***************************************************************')
               logit.info('\nFetching of Device/Usage XML data - successful')
               parse_billing = ProcessXML('devices',output, db_conn, cursor )
               parse_billing.process_xml() 
   except OSError as e:
       logit.error('errno: %d: %s' % (e.errno, e.strerror))

if inputs.confspaces:
   try:
       proc = Popen('curl -k -s -u "administrator:fsp-WWcs!1" -H "Content-type: text/xml;" -H "SOAPAction:CUCM:DB ver=11.5" https://10.207.200.84/api/v1/coSpaces', stdout=PIPE, shell=True)
       output, err = proc.communicate()

       #  err = None if no errors returned from SOAP call
       if err:
           logit.error('%d: %s' % (proc.returncode, err.strip()))
       elif proc.returncode != 0 and not err:
          logit.error('*** Retrieve conference space - No error msg returned, Unknown error occurred, retcode: %d' % proc.returncode)
       else:
          # Data from conferences spaces processed, logged here  
          if output:
              logit.info('\nFetching of Conference Room XML data - successful') 
              parse_billing = ProcessXML('conf_spaces',output, db_conn, cursor )
              parse_billing.process_xml()
              logit.info('*******************************************************************')
   except OSError as e:
       logit.error('errno: %d: %s' % (e.errno, e.strerror))

db_conn.close()
sys.exit(1)
