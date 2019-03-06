import re
import json
import mock
import pytest
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# system tests #
class TestApi:
   def test_valid_contract_number(self):
      r = requests.get('http://127.0.0.1:5010/api/device/11111111')
      data = json.loads(r.json()) 
      assert(data[0]['contract'] == '11111111')  

   def test_invalid_contract_non_numeric(self):
      r = requests.get('http://127.0.0.1:5010/api/device/11ert111')
      data = json.loads(r.text)
      assert( data['contract'][0] == 'Contract number must be numeric only')

   def test_contract_bad_length_less(self):
      r = requests.get('http://127.0.0.1:5010/api/device/2222')
      data = json.loads(r.text)
      assert( data['contract'][0] == 'Contract number must be 8 digits only')
  
   def test_contract_bad_length_greater(self):
      r = requests.get('http://127.0.0.1:5010/api/device/44444444444')
      data = json.loads(r.text)
      assert( data['contract'][0] == 'Contract number must be 8 digits only')

   def test_contract_num_bad_address(self):
      r = requests.get('http://127.0.0.1:5010/api/device/dev/11111111')
      assert( r.status_code == 404)

   def test_valid_month_date(self):
      r = requests.get('http://127.0.0.1:5010/api/devices', data={'month':'January', 'date':'2019-01-28'})
      data = json.loads(r.json()) 
      assert(data[0]['month'] == 'January')  
      assert(re.search('\d{4}-\d{2}-\d{2}', data[0]['date_received']))

   def test_request_all(self):
      r = requests.get('http://127.0.0.1:5010/api/alldevices')
      data = json.loads(r.json()) 
      assert(r.status_code == 200)  
      assert(data[0]['TotalUsers'] != '4300')
  
   def test_conference_call_id(self):
      r = requests.get('http://127.0.0.1:5010/api/conference/5555100')
      data = json.loads(r.json()) 
      assert(r.status_code == 200)  
      assert(data[0]['CallId'] == '5555100')

   def test_conference_iptype(self):
      r = requests.get('http://127.0.0.1:5010/api/conferences/remote')
      data = json.loads(r.json()) 
      assert(r.status_code == 200)  
      assert(data[0]['local_remote'] == 'remote')

   def test_conference_all(self):
      r = requests.get('http://127.0.0.1:5010/api/allconferences')
      data = json.loads(r.json()) 
      assert(r.status_code == 200)  
      assert(data[0]['Uri'] == '003036010003')
