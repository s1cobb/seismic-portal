import os
import re
import sys
import time
import json
import urllib
import requests
import xml.sax
import logging
from pprint import pprint
from ProcessXML import MyXMLHandler

############## Class for seismic and weather activity collection #####
class EarthData:
   def __init__( self ):
       self.seismic_data = {}   # holds earthquake data
       self.weath_data   = {}   # holds weather data at earthquake area
       self.merge_data   = {}   # merge weather and earthquake info needed 
       self.data_list    = []   # list of merge_data dict 
       self.earth_xdata = []    # seismic/weather in xml format 
       self.weat_xml    = []    # holds weather data
       self.total       = 0     # number of records to retrieve

   ###########################################################
   def get_latest_quake_activity( self, magnitude=None, total=0 ):
       ''' Will get the latest quake activity that was recorded
           overnight. Data returned in JSON format.
           Input:   magnitude  # size of earthquake
                    total      # number of records to get

           Output:  0  # failure
                    1  # pass
       ''' 
       self.total = total
       max_magnitude = magnitude + 1.0 

       # get seismic info in json format #
       path = 'http://www.seismicportal.eu/fdsnws/event/1/query?' \
              'format=json&minmagnitude=%f&maxmagnitude=%f&limit=%d ' \
              % (magnitude, max_magnitude, total)

       rsp  = requests.get(path)
       data = rsp.text

       # load quake data into dictionary 
       try:
          self.seismic_data = json.loads( data.decode() )
       except ValueError:
          print("ERROR: No quake data was returned from website...")
          return 0 
       return 1
      
   #############################################################
   def get_latest_quake_activity_in_xml( self, magnitude=None, total=0 ):
       ''' Will get the latest quake activity that was recorded
           overnight. Data returned in XML format.
           Input:   magnitude  # size of earthquake
                    total      # number of records to get

           Output:  0  # failure
                    1  # pass
       ''' 
       self.total = total
       max_magnitude = magnitude + 1.0 

       # get seismic info in xml format #
       path = 'http://www.seismicportal.eu/fdsnws/event/1/query?' \
              'format=xml&minmagnitude=%f&maxmagnitude=%f&limit=%d' \
               % (magnitude, max_magnitude, total)
       req  = urllib.urlopen( path )
       data = req.read()

       # call my XML handler to parse/load data 
       self.weath_data = []
       Handler = MyXMLHandler( self.earth_xdata )
       xml.sax.parseString(data, Handler)
       
       if not self.earth_xdata:
          print("ERROR: No quake data was returned from website...")
          return 0
       else:
          return 1

      
   ###############################################################
   def _get_latest_weather_activity( self, lon, lat ):
       '''Get the weather of the area where the earthquake
          occured. Data is returned in a JSON format.
                 JSON format.
          input -  lon --> longitude 
                   lat --> latitude 
          output - 0   --> Failure
                   1   --> Pass
       ''' 

       # get weather info in json format #
       path = 'http://api.openweathermap.org/data/2.5/weather?' \
              'lat=%f&lon=%f&appid=52c86a71c2d91476335ddaf0738e2987' % (lat,lon)
       req  = urllib.urlopen( path )
       data = req.read()

       # convert json data into dict data #
       try:
          self.weath_data = json.loads( data.decode() )
       except ValueError:
          print("ERROR: No weather data was returned from website")
          return 0 
       return 1
      

   ###############################################################
   def _get_latest_weather_activity_in_xml( self, lon, lat ):
       '''Get the weather of the area where the earthquake
          occured. Data is returned in a XML format.
                 JSON format.
          input -  lon --> longitude 
                   lat --> latitude 
          output - 0   --> Failure
                   1   --> Pass
       ''' 
       path = 'http://api.openweathermap.org/data/2.5/weather?' \
              'mode=xml&lat=%f&lon=%f&appid=52c86a71c2d91476335ddaf0738e2987' \
              % (float(lat),float(lon))
       req  = urllib.urlopen( path )
       data = req.read()

       # process the XML data
       self.weat_xml = []
       Handler = MyXMLHandler( self.weat_xml )
       xml.sax.parseString(data, Handler)

   
   ###############################################################
   def merge_xml_weather_data( self ):
       ''' Get the weather info from the quake site '''
 
       for elem in range(0, self.total):
           # setup weather elements needed #
           self.earth_xdata[elem]['pressure'] = ''
           self.earth_xdata[elem]['temp_min'] = ''
           self.earth_xdata[elem]['temp_max'] = ''
           self.earth_xdata[elem]['weather']  = ''
           self.earth_xdata[elem]['windspeed'] = ''

           # send request for weather info
           self._get_latest_weather_activity_in_xml( self.earth_xdata[elem]['longitude'],
                                                     self.earth_xdata[elem]['latitude'] )

           self.earth_xdata[elem]['pressure'] = self.weat_xml[0]['pressure'] 
           self.earth_xdata[elem]['temp_min'] = self.weat_xml[0]['temperature_min']
           self.earth_xdata[elem]['temp_max'] = self.weat_xml[0]['temperature_max']
           self.earth_xdata[elem]['weather']  = self.weat_xml[0]['weather']
           self.earth_xdata[elem]['windspeed'] = self.weat_xml[0]['windspeed']
           self.weat_xml = []

       return self.earth_xdata 
           

   ###############################################################
   def merge_earth_data( self ):
       ''' Combine seismic and weather activity at the earthquake 
           site into one dictionary data structure.
       '''
       for lis_elm in range(0, self.total):
           self.merge_data = { 'features' : {} }

           # add coordinates to list
           self.merge_data['features'][ 'coord'] = [] 
           self.merge_data['features']['coord'].append( \
                self.seismic_data['features'][lis_elm]['geometry']['coordinates'][0] )
           self.merge_data['features']['coord'].append( \
                self.seismic_data['features'][lis_elm]['geometry']['coordinates'][1] )
           self.merge_data['features']['coord'].append( \
                self.seismic_data['features'][lis_elm]['geometry']['coordinates'][2] )
           
           # setup for the seismic/weather data to be added.
           self.merge_data['features']['properties'] = { 'depth' : "", 'mag' : "", 'last_update' : "",
                                                   'time' : "", 'region' : "", "weather" : "",
                                                   'descrip' : "", 'sunrise' : "",
                                                   'country' : "", 'name' : "" }
           
           self._get_latest_weather_activity( self.merge_data['features']['coord'][0],
                                              self.merge_data['features']['coord'][1] )

           self.merge_data['features']['properties']['weather']  = self.weath_data['weather'][0]['main']
           self.merge_data['features']['properties']['descrip']  = self.weath_data['weather'][0]['description']
           self.merge_data['features']['properties']['sunrise']  = self.weath_data['sys']['sunrise']
           self.merge_data['features']['properties']['country']  = self.weath_data['sys']['country']
           self.merge_data['features']['properties']['name']     = self.weath_data['name']
           self.merge_data['features']['properties']['depth']       =  \
                    self.seismic_data['features'][lis_elm]['properties']['depth']
           self.merge_data['features']['properties']['mag']         = \
                    self.seismic_data['features'][lis_elm]['properties']['mag']
           self.merge_data['features']['properties']['last_update'] = \
                    self.seismic_data['features'][lis_elm]['properties']['lastupdate']
           self.merge_data['features']['properties']['time']        = \
                    self.seismic_data['features'][lis_elm]['properties']['time']
           self.merge_data['features']['properties']['region']      = \
                    self.seismic_data['features'][lis_elm]['properties']['flynn_region']

           # append each dict to list.
           self.data_list.append( self.merge_data )

       return self.data_list 


   ###############################################################
   def log_data( self ):
       ''' Log the earthquake information along with
           the weather conditions when quake occurred.
       '''
       print("Saving earth data to log file 'earth.log'...")
       logger = logging.getLogger('earth_logger')
       logger.setLevel(logging.DEBUG)
       fhdler = logging.FileHandler('earth.log')
       fhdler.setLevel(logging.DEBUG)
       formatter = logging.Formatter('%(asctime)s %(name)-15s %(levelname)-8s %(message)s',
                               datefmt='%m/%d/%Y %I:%M:%S %p')
       fhdler.setFormatter(formatter)
       logger.addHandler(fhdler)

       for lis_elm in range(0, self.total):
           logger.info("%s %s" % ('Long: ', self.data_list[lis_elm]['features']['coord'][0] ))
           logger.info("%s %s" % ('Lat: ', self.data_list[lis_elm]['features']['coord'][1] ))
           logger.info("%s %s" % ('Depth: ', self.data_list[lis_elm]['features']['properties']['depth']))
           logger.info("%s %s" % ('Magnitude: ', self.data_list[lis_elm]['features']['properties']['mag'])) 
           logger.info("%s %s" % ('LastUpdate: ', self.data_list[lis_elm]['features']['properties']['last_update']))
           logger.info("%s %s" % ('Occured: ', self.data_list[lis_elm]['features']['properties']['time'])) 
           logger.info("%s %s" % ('Region: ', self.data_list[lis_elm]['features']['properties']['region']))
           logger.info("%s %s" % ('Weather: ', self.data_list[lis_elm]['features']['properties']['weather'])) 
           logger.info("%s %s" % ('Descrip: ', self.data_list[lis_elm]['features']['properties']['descrip']))
           logger.info("%s %s" % ('Sunrise: ', self.data_list[lis_elm]['features']['properties']['sunrise'])) 
           logger.info("%s %s" % ('Country: ', self.data_list[lis_elm]['features']['properties']['country']))
           logger.info("%s %s" % ('City: ', self.data_list[lis_elm]['features']['properties']['name'])) 
           logger.info("%s" % ' End Record\n')

       return 1


   def print_xml_data( self ) :
       for lis_elm in range(0, self.total):
           print("{:>25}".format(self.earth_xdata[lis_elm]['depth']))
           print("{:>25}".format(self.earth_xdata[lis_elm]['mag'])) 
           print("{:>25}".format(self.earth_xdata[lis_elm]['created_date']))
           print("{:>25}".format(self.earth_xdata[lis_elm]['time'])) 
           print("{:>25}".format(self.earth_xdata[lis_elm]['region']))
           print("{:>25}".format(self.earth_xdata[lis_elm]['weather'])) 
           print("{:>25}".format(self.earth_xdata[lis_elm]['longitude']))
           print("{:>25}".format(self.earth_xdata[lis_elm]['latitude'])) 
           print("{:>25}".format(self.earth_xdata[lis_elm]['country']))
           print("{:>25}".format(self.earth_xdata[lis_elm]['pressure'])) 
           print("{:>25}".format(self.earth_xdata[lis_elm]['temp_min'])) 
           print("{:>25}".format(self.earth_xdata[lis_elm]['temp_max'])) 
           print("{:>25}".format(self.earth_xdata[lis_elm]['windspeed'])) 
           print(" End Record\n")

       return 1

if __name__ == '__main__':
   # seismic portal testing
   num_records = 2   
   quake_size = 2.0
   quake_data  = EarthData()

   if quake_data.get_latest_quake_activity(magnitude=quake_size, total=num_records):
      quake_data.merge_earth_data()
      quake_data.log_data()
   else:
      print("Error: No earthquake data processed")

   print("Sleep 5 seconds before testing XML")
   time.sleep(5)
   if quake_data.get_latest_quake_activity_in_xml(magnitude=3.0, total=2):
      quake_data.merge_xml_weather_data()
      quake_data.print_xml_data()
   else:
      print("Error: No earthquake data processed")
