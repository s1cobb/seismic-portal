import re
import time
import pika
import pymysql
import requests

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
       mysql_id_num = m.group(1)  # database id
       rest_api = m.group(2)      # post,delete,put,update
       msg = m.group(3)          # message to save
       
       if 'get' == rest_api.lower():
          print("%s %s %s" % (rest_api, mysql_id_num, msg ))
          path = 'http://127.0.0.1:5000/id/%s' % mysql_id_num
          r = requests.get(path)
          print(r.text)
       elif 'post' == rest_api.lower():
           print("%s %s %s" % (rest_api, mysql_id_num, msg ))
           path = 'http://127.0.0.1:5000/id/%s' % mysql_id_num
           dat = {'route':method.routing_key, 'message':msg}
           requests.post(path, data=dat).json()
       elif 'delete' == rest_api.lower():
           print("delete %s" % mysql_id_num, msg)
           path = 'http://127.0.0.1:5000/id/%s' % mysql_id_num
           requests.delete(path).json()
       elif 'put' == rest_api.lower():
           print("%s %s %s" % (rest_api, mysql_id_num, msg ))
           path = 'http://127.0.0.1:5000/id/%s' % mysql_id_num
           dat = {'route':method.routing_key, 'message':msg}
           requests.put(path, data=dat).json()
       else:
           print("non http requests")      

           
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