#  python -m unittest discover simple_example_dir

import json
import unittest
import requests


class CndbRest( unittest.TestCase ):
       def setUp(self):
             self.serdata = {}
             self.r = requests.get('http://127.0.0.1:5000/api/server/NPOWRTPVWSVDCS1')
             self.serdata = json.loads(self.r.text)
       
       def test_status_code( self ):
             self.assertEqual(self.r.status_code,200, msg="status code not equal to 200")
             
       def test_server_name(self):
             self.assertEqual(self.serdata['ServerData'][0]['server'],"NPOWRTPVWSVDCS1", msg = 'requested server name was not returned')
             
       def test_server_patch(self):
            self.assertRegex(self.serdata['ServerData'][0]['patched'],"y|n", msg = 'patched value was not y or n')
             
if __name__ == '__main__':
      unittest.main()

