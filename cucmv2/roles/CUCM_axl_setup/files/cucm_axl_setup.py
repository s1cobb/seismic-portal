#!/usr/bin/python

''' 
   Filename: cucm_axl_setup.py 
   Version: Python 2.7.5 
   Author: Steve Cobb (stcobb@cisco.com)
   Description: 
        This script will configure the Call Manager with preset values
        using the AXL web Api. We are using SOAP/XML requests to input
        the configuration values and each request will return a response.
        Each response will be checked for valid status code of 200 and
        that a valid hash ID was created for each AXL input request.

        This script is called by Ansible in tasks/main.yml
'''

import os
import sys
import requests
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# get module path from group_vars/all
module_path = sys.argv[7]
sys.path.append(module_path)

from cucm_axl_utils import run_cm_web_api_req

# input variables
usr = sys.argv[1]
pw  = sys.argv[2]
ip_address = sys.argv[3]
axl_file_to_run = sys.argv[4]
need_to_modify  = sys.argv[5]
url = sys.argv[6]

headers = {'Content-type' : 'text/xml'}

# log each axl web configuration to file axlconfig.log
logit = logging.getLogger('axl_logger')
logit.setLevel(logging.DEBUG)
logfor = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fh = logging.FileHandler('axlconfig.log', 'a')
fh.setFormatter(logfor)
logit.addHandler(fh)


run_cm_web_api_req(usr, pw, headers, axl_file_to_run,
                   need_to_modify, url, ip_address, logit, module_path)
