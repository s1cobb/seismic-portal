import xml.sax
import logging
from datetime import datetime
from xml.sax.saxutils import unescape
from xml.sax._exceptions import SAXParseException

# user defined Classes
import misc_util
from XMLHandlers import LicXMLHandler
from XMLHandlers import ConfXMLHandler

class ProcessXML:
    ''' Class will process xml from the Call Manager and Cisco Meeting Server.
        Make calls to the xml handlers for parsing and log output to logfiles.

        Input Parameters:
           xml_type: which xml data to process, device usage or conference spaces
           xml_data: actual xml data returned from web Api
           server_data: dictionary holding server information from the
                        billing_config.csv file. 
        
        Example:
           obj = ProcessXML('devices',xml_data, server_data )
           obj.process_xml()
    '''

    def __init__(self, xml_type, xml_data, server_data ):
        self.serv_info  = server_data
        self.xml_type = xml_type
        self.xml_data = xml_data
        self.billdata = []

        # setup logging
        self.logger   = logging.getLogger('my_logger')
        self.logspk   = logging.getLogger('spk_error_logger')
        
    #########################################################################
    # process_xml:  
    #########################################################################
    def process_xml(self):
        ''' Process the XML data and save to log file and database

            Call the XML handlers here to process XML data
            Handler ConfXMLHandler - parse Conference room data
            Handler LicXMLHandler  - parse Device/Usage data
            Returned data will be in a list of dictionaries 
        '''

        if self.xml_type == 'conf_spaces':
           try:
               # setup xml handler with self.billdata as the return value. 
               Handler = ConfXMLHandler( self.billdata )

               # convert apos and guotes with actual character
               new_xml_data = unescape(self.xml_data, {"&apos;": "'", "&quot;": '"'})

               # parse the XML conference space info with custom handler
               xml.sax.parseString(new_xml_data, Handler)
           except SAXParseException as e:
               misc_util.log_message(self.logspk, self.serv_info,
                                   'ERROR - Conf Meeting XML Parsing,', 'sys_error', e)

           # if no data, xml parsing failed
           if not self.billdata:
               misc_util.log_message(self.logspk, self.serv_info,
                                   'No Conference data returned from XML parser', 'error')
           else:
               self._log_all_data()
        elif self.xml_type == 'devices':
           try:
               # setup xml handler with self.billdata as the return value.
               Handler = LicXMLHandler( self.billdata )

               # parse the XML device/usage info with custom handler
               xml.sax.parseString(self.xml_data, Handler)
           except SAXParseException as e:
               misc_util.log_message(self.logspk, self.serv_info,
                                   'ERROR - Device/Usage XML Parsing,', 'sys_error', e)

           # if no data, xml parsing failed
           if not self.billdata:
               misc_util.log_message(self.logspk, self.serv_info,
                                   'No Device/User data returned from XML parser', 'error')
           else:
               self._log_all_data()


    def _log_all_data(self):
        ''' Logs data to logger file and to the billing database '''

        key_tags = ['coSpace id', 'name', 'autogenerated', 'uri', 'callId']

        loginfo = ''
        tag_err = []

        if self.xml_type == 'conf_spaces':
           for tmp in self.billdata:
              # tmp holds a dictionary of conference space data
              # append conf data to variable loginfo before logging
              # to the log file.
              if 'total_cospaces' in tmp:
                 loginfo = "coSpace_Total:" + tmp['total_cospaces'] + ','
              else:
                 # verify all conference space tags are present
                 tag_err = [x for x in key_tags if x not in tmp]
                 if not tag_err:
                    if 'secondaryUri' not in tmp:
                       loginfo += 'secondaryUri:None,'
                    for k,v in tmp.items():
                        loginfo += k + ':' + v + ','
                 else:
                    misc_util.log_message(self.logspk, self.serv_info,
                                   'Missing conference meeting XML tag data', 'error')
           
           misc_util.log_message(self.logger, self.serv_info, loginfo, 'info')
        elif self.xml_type == 'devices':
           for tmp in self.billdata:
               # append device data to variable loginfo before logging
               for k,v in tmp.items():
                 loginfo += k + ':' + v + ','

               misc_util.log_message(self.logger, self.serv_info, loginfo, 'info')
               loginfo = ''

