#!/usr/bin/python

''' 
   Filename: cucm_axl_utilies.py 
   Version: Python 2.7.5 
   Author: Steve Cobb (stcobb@cisco.com)
   Description: 
        The utilies library holds the verification
        definitions and the main definition interface
        that ansible calls for each AXL api request. 
'''

import re
import sys
import time
import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#########################################################################
#   verify_response: 
#         This definition is used to verify each response from the AXL
#         Api.
#
#   Inputs:
#         verify_rsp  - holds the response value in text string
#         status_code - holds return code, 200, 404, etc.
######################################################################### 
def verify_response(verify_rsp=None, status_code=0):
   ''' Verify the return hash ID has been issued '''

   if status_code == requests.codes.ok:
       m = re.search("\<return\>\{(.*?)\}\<\/return", verify_rsp, re.I)
       if m:
           return m.group(1)
   else:
       m = re.search("\<faultstring\>(.*?)\<\/faultstring", verify_rsp, re.I)
       if m:
           return m.group(1)
       else:
           return 'Failed to get fault string value'

#########################################################################
#   verify_services_started:
#         This definition is used to verify each service that is required 
#         has been started.
#
#   Inputs:
#         verify_rsp  - holds the response value in text string
#         status_code - holds return code, 200, 404, etc.
#########################################################################
def verify_services_started(verify_rsp=None, status_code=0):
   ''' Verify each service has been started '''

   rsp_string = ''
   find_values = ['Cisco CallManager', 'Cisco Tftp', 'Cisco CTL Provider',
                  'Cisco Certificate Authority Proxy Function', 'Cisco DirSync',
                  'Cisco Bulk Provisioning Service', 'Cisco AXL Web Service',
                  'Cisco SOAP - CDRonDemand Service', 'Cisco CAR Web Service' ]

   
   if status_code == requests.codes.ok:
       for service in find_values:
           my_regex = "ServiceName\>(" + service + ")\<\/ns1\:ServiceName\>\<ns1\:ServiceStatus\>(Started)"
           m = re.search(my_regex, verify_rsp, re.I)
           if m:
               rsp_string +=  m.group(1) + '-' + m.group(2) + " "

       return rsp_string
   else:
       m = re.search("\<faultstring\>(.*?)\<\/faultstring", verify_rsp, re.I)
       if m:
           return m.group(1)
       else:
           return 'Error with Service start, fault string value empty'


def verify_services_started_req( usr, pw, headers, axl_file, url, logger ):
    with open(axl_file) as fp:
         body = fp.read()

    rsp = requests.post(url, auth=(usr, pw), verify=False, data=body, headers=headers)
     
    ver_started = verify_services_started(verify_rsp=rsp.text, status_code=rsp.status_code)
    return(ver_started)


#########################################################################
#   run_cm_web_api_req:
#         This is the main definition interface for the ansible calls. 
#         Inputs:
#              usr - user login
#              pw  - user password
#              headers  - web request headers
#              axl_file - file holds the AXL/Soap web request
#              modify_soap_body - yes/no, does web request need modification
#              url        - CUCM url path
#              ip_address - ip address
#              logger     - logger object for saving output
#
#         Outputs:
#              servs - returns the status of the services that were started
#              resp  - returns the status of each AXL web response
#
#########################################################################
def run_cm_web_api_req( usr, pw, headers, axl_file, modify_soap_body, url, ip_address, logger, mod_path ):
    body = ''

    with open(axl_file,'r') as fp:
         body = fp.read() 

    if modify_soap_body == 'no':
       rsp = requests.post(url, auth=(usr, pw), verify=False, data=body, headers=headers)
       logger.info('%s' % rsp.content)       
       resp = verify_response(verify_rsp=rsp.text, status_code=rsp.status_code)
       print(resp)
       time.sleep(1)
    elif modify_soap_body == 'yes':
       if re.search('soapDoServiceDeployment', axl_file):
          new_body = body.replace('add_ip_address', ip_address)
          
          axl_verify_req = mod_path + '/AxlCmds/AXL_verifyActivatedServices.txt'

          rsp = requests.post(url, auth=('AXLUser', 'fsp-WWcs!1'), verify=False, data=new_body, headers=headers)
          time.sleep(35)

          logger.info('%s' % rsp.content)
          servs = verify_services_started_req( usr, pw, headers, axl_verify_req, url, logger )
          print(servs)
