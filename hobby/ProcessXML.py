import xml.sax

class MyXMLHandler( xml.sax.ContentHandler ):
    ''' Class will process the XML seismic portal and weather
        data, returns a list of dictionaries.
    '''
    def __init__( self, xmlout = [] ):
        self.currtag  = ''
        self.tmp      = ''
        self.tdic     = {}
        self.event    = False
        self.desc     = False
        self.mag      = False 
        self.mag      = False 
        self.latitude = False 
        self.longitude= False 
        self.depth    = False 
        self.time     = False 
        self.xmllis  = xmlout

        # weather tags here
        self.tempature = ''
        self.pressure  = ''
        self.windspeed = ''
        self.weather   = ''

    ############################################################# 
    def startElement(self, tag, attributes):
       ''' set values for specific start tags '''

       self.currtag = tag
       if tag == 'event':
          self.event = True
       if tag == 'description':
          self.desc = True
       if tag == 'magnitude':
          self.mag = True
       if tag == 'latitude':
          self.latitude = True
       if tag == 'longitude':
          self.longitude = True
       if tag == 'depth':
          self.depth = True
       if tag == 'time':
          self.time = True

       # weather tags here
       if tag == 'temperature':
          self.tdic['temperature_min'] = attributes['min']
          self.tdic['temperature_max'] = attributes['max']
       if tag == 'pressure':
          self.tdic['pressure'] = attributes['value']
       if tag == 'speed':
          self.tdic['windspeed'] = attributes['name']
       if tag == 'weather':   
          self.tdic['weather'] = attributes['value']


    ############################################################# 
    def characters(self, content):
       ''' Get tag data '''

       if self.currtag == 'creationTime':
          self.tdic['created_date'] = content
       elif self.currtag == 'text':
          self.tdic['country'] = content
       elif self.currtag == 'type' and self.desc:
          self.tdic['region'] = content
          self.desc = False    
       elif self.currtag == 'value' and self.time:
          self.tdic['time'] = content    
          self.time = False
       elif self.currtag == 'value' and self.latitude:
          self.tdic['latitude'] = content    
          self.latitude = False
       elif self.currtag == 'value' and self.longitude:
          self.tdic['longitude'] = content
          self.longitude = False    
       elif self.currtag == 'value'and self.depth:
          self.tdic['depth'] = content
          self.depth = False    
       elif self.currtag == 'value' and self.mag:
          self.tdic['mag'] = content
          self.mag = False    


    ############################################################# 
    def endElement(self, tag):
       ''' Append and cleanup data structures ''' 

       if tag == 'event' or tag == 'current':
          self.xmllis.append(self.tdic)
          self.tdic = {}

       self.currtag = ''
