import re
import time
import pika
import pymysql
import requests
from pprint import pprint

class Producer:
    ''' Class used to send messges to rabbitmq.
        Setup the exchange and queue then send 
        message.        
     '''         
    def __init__(self, exchange=None):
        self.msg       = ''
        self.route_key = ''
        self.exchange  = exchange
       
        # establish connection to rabbitmq server
        self.conn = pika.BlockingConnection(pika.ConnectionParameters( host='localhost'))
        self.channel = self.conn.channel()
        
        
    #######################################################
    def set_exchange(self):
        self.channel.exchange_declare(exchange=self.exchange, type='topic')
        
        
    #######################################################   
    def publish_msg(self, route_key, msg_body):
        self.channel.basic_publish( exchange=self.exchange,
                                 routing_key=route_key,
                                 body=msg_body)
                                 
                                 
    #######################################################    
    def close_conn(self):
        self.conn.close()
    
        
class Consumer:
    ''' Class will grap messages from rabbitmq and
        depending on the exchange and queue will 
        send the messages to the Flask rest api.
        Interface is a rest api to the MySql database.
    '''
    def __init__(self, exchange=None, debug=False):
       self.msg       = ''
       self.route_key  = ''
       self.exchange   = exchange
       self.queue_name = ''
       self.debug = debug
       
       self.conn = pika.BlockingConnection( pika.ConnectionParameters(host='localhost'))
       self.channel = self.conn.channel()
       
    ######################################################   
    def set_exchange(self):
        self.channel.exchange_declare( exchange=self.exchange, type='topic')
        
        # system will create queue name
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        
        
    ########################################################
    def _callback(self, ch, method, properties, body ):
       m = re.search('^(\d+)\s(\w+)(.*)', body.decode(), re.I)
       if m:
          mysql_id_num = m.group(1)  # database id
          rest_api = m.group(2)      # post,delete,put,update
          msg = m.group(3)          # message to save
       
       
          if 'get' == rest_api.lower():
             print("%s %s %s" % (rest_api, mysql_id_num, msg ))
             path = 'http://127.0.0.1:5000/id/%s' % mysql_id_num
          
             try:
                r = requests.get(path)
                if r.status_code == 200:
                   print(r.text)
                else:
                   print("Error request failed with code: %s" % r.status_code)
             except requests.exceptions.ConnectionError as e:
                print("Connection Failure %s" % e )
             except requests.exceptions.Timeout as e:
                print("Connection Timeout: %s" % e)
             except requests.exceptions.HTTPError as e:
                print("HTTP error: %s" % e)
          elif 'post' == rest_api.lower():
              print("%s %s %s" % (rest_api, mysql_id_num, msg ))
              path = 'http://127.0.0.1:5000/id/%s' % mysql_id_num
              dat = {'route':method.routing_key, 'message':msg}
           
              try:
                 r = requests.post(path, data=dat).json()
                 pprint(r)
              except ValueError as e:
                 print("Error inserting into MySql database: %s" % e)
              except requests.exceptions.ConnectionError as e:
                 print("Connection Failure %s" % e )
              except requests.exceptions.Timeout as e:
                 print("Connection Timeout: %s" % e)
              except requests.exceptions.HTTPError as e:
                 print("HTTP error: %s" % e)
              except requests.RequestsException as e:
                 print("Error while handling request: %s" % e)
          elif 'delete' == rest_api.lower():
              print("delete %s" % mysql_id_num, msg)
              path = 'http://127.0.0.1:5000/id/%s' % mysql_id_num
           
              try:
                 r = requests.delete(path).json()
                 pprint(r)
              except ValueError as e:
                 print("ERROR deleting from MySql database: %s" % e)
              except requests.exceptions.ConnectionError as e:
                 print("Connection Failure %s" % e )
              except requests.exceptions.Timeout as e:
                 print("Connection Timeout: %s" % e)
              except requests.exceptions.HTTPError as e:
                 print("HTTP error: %s" % e)
          elif 'put' == rest_api.lower():
             print("%s %s %s" % (rest_api, mysql_id_num, msg ))
             path = 'http://127.0.0.1:5000/id/%s' % mysql_id_num
             dat = {'route':method.routing_key, 'message':msg}
           
             try:
                r = requests.put(path, data=dat).json()
                pprint(r)
             except ValueError as e:
                print("Error with updating MySql database: %s" % e)
             except requests.exceptions.ConnectionError as e:
                print("Connection Failure %s" % e )
             except requests.exceptions.Timeout as e:
                print("Connection Timeout: %s" % e)
             except requests.exceptions.HTTPError as e:
                print("HTTP error: %s" % e)
          else:
             print("ERROR: non http requests")      
       else:
          print("ERROR: invalid message format: %s" % body.decode())
           
    ########################################################    
    def set_binding_keys(self, *binding_keys):
       for binding_key in binding_keys:
           self.channel.queue_bind(exchange=self.exchange,
                                queue=self.queue_name,
                                routing_key=binding_key)
       
       print(" [x] waiting for logs. to exit press ctrl+c")       
       self.channel.basic_consume(self._callback,
                               queue=self.queue_name,
                               no_ack=True)
                               
       self.channel.start_consuming()
        
        
if __name__ == '__main__':
    pass