import re
import xml.sax
import logging

logger = logging.getLogger('my_logger')

######################## Class LicXMLHandler Definition ######################
class LicXMLHandler( xml.sax.ContentHandler ):
    ''' Class will process the device/usage XML data 
        returns a list of dictionaries.
    '''
    def __init__( self, xmlout = [] ):
        self.currtag  = ''
        self.billinfo = {}
        self.xmllis  = xmlout

        # D1 and D2 billing tags
        self.cuwl_standard = False 
        self.enhancedplus  = False 
        self.enhanced      = False
        self.basic         = False 
        self.essential     = False 
        self.telepresence  = False 
        self.totalusers    = False 
        self.totaldevices  = False 
        self.timestamp     = False
        self.lastcontact   = False
        self.elm           = False
 
    def startElement(self, tag, attributes):
       ''' set value for specific start tags '''
       self.currtag = tag

    def characters(self, content):
       ''' Get tag data '''

       if self.currtag == 'name':
          if re.search('^CUWL\sStandard',content):
             self.cuwl_standard = True
          elif re.search('^EnhancedPlus',content):
             self.enhancedplus = True
          elif re.search('^Enhanced',content):
             self.enhanced = True
          elif re.search('^Basic',content):
             self.basic = True
          elif re.search('^Essential',content):
             self.essential = True
          elif re.search('^TelePresence\sRoom',content):
             self.telepresence = True
          elif re.search('^TotalUsers',content):
             self.totalusers = True
          elif re.search('^TotalDevices',content):
             self.totaldevices = True
          elif re.search('^Timestamp',content):
             self.timestamp = True
          elif re.search('^ElmLastContact',content):
             self.lastcontact = True
          elif re.search('^Elm',content):
             self.elm = True

       if self.currtag == 'value':
          if self.cuwl_standard:
             self.billinfo['CUWL Standard'] = content    
             self.cuwl_standard = False
          elif self.enhancedplus:
             self.billinfo['EnhancedPlus'] = content
             self.enhancedplus = False    
          elif self.enhanced:
             self.billinfo['Enhanced'] = content
             self.enhanced = False    
          elif self.basic:
             self.billinfo['Basic'] = content
             self.basic = False    
          elif self.essential:
             self.billinfo['Essential'] = content
             self.essential = False    
          elif self.telepresence:
             self.billinfo['TelePresence Room'] = content
             self.telepresence = False    
          elif self.totalusers:
             self.billinfo['TotalUsers'] = content
             self.totalusers = False    
          elif self.totaldevices:
             self.billinfo['TotalDevices'] = content
             self.totaldevices = False    
          elif self.timestamp:
             self.billinfo['Timestamp'] = content
             self.timestamp = False    
          elif self.lastcontact:
             self.billinfo['ElmLastContact'] = content
             self.lastcontact = False    
          elif self.elm:
             self.billinfo['Elm'] = content
             self.elm = False    

    def endElement(self, tag):
       ''' Append and cleanup data structures ''' 

       if tag == 'return':
          self.xmllis.append(self.billinfo)
          self.billinfo = {}
       self.currtag = ''

######################## Class ConfXMLHandler Definition ######################
class ConfXMLHandler( xml.sax.ContentHandler ):
    ''' Class will process the devices XML data
        returns a list of dictionaries.
    '''
    def __init__( self, xmlout = [] ):
        self.currtag  = ''
        self.billinfo = {}
        self.xmllis  = xmlout
        self.cospace = False

    def startElement(self, tag, attributes):
       ''' set values for specific start tags '''
       self.currtag = tag
       if self.currtag == 'coSpaces':
          self.billinfo['total_cospaces'] = attributes['total']
          self.xmllis.append(self.billinfo)
          self.billinfo = {}
       elif self.currtag == 'coSpace':
          self.billinfo['coSpace_id'] = attributes['id']
          self.cospace = True

    def characters(self, content):
       ''' Get tag data '''

       if self.cospace:
          if self.currtag == 'name':
             self.billinfo['name'] = content
          elif self.currtag == 'autoGenerated':
             self.billinfo['autogenerated'] = content
          elif self.currtag == 'uri':
             self.billinfo['uri'] = content
          elif self.currtag == 'callId':
             self.billinfo['callId'] = content
          elif self.currtag == 'secondaryUri':
             self.billinfo['secondaryUri'] = content

    def endElement(self, tag):
       ''' Append and cleanup data structures '''

       if tag == 'coSpace':
          self.xmllis.append(self.billinfo)
          self.billinfo = {}
          self.cospace = False

       self.currtag = ''
