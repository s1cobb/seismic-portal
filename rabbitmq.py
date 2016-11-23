import pika
import pymysql
import time


class Producer:
    ''' Class used to send messges to correct exchange 
         and queue
     '''         
    def __init__(self, exchange=None):
        self.msg       = ''
        self.route_key = ''
        self.exchange  = exchange
       
        self.conn = pika.BlockingConnection(pika.ConnectionParameters( host='localhost'))
        self.channel = self.conn.channel()

    def set_exchange(self):
        self.channel.exchange_declare(exchange=self.exchange, type='topic')
        
    def publish_msg(self, route_key, msg_body):
        self.channel.basic_publish( exchange=self.exchange,
                                 routing_key=route_key,
                                 body=msg_body)
        
    def close_conn(self):
        self.conn.close()
    
        
class Consumer:
    def __init__(self, exchange=None, debug=False):
       self.msg       = ''
       self.route_key  = ''
       self.exchange   = exchange
       self.queue_name = ''
       self.debug = debug
       
       self.conn = pika.BlockingConnection( pika.ConnectionParameters(host='localhost'))
       self.channel = self.conn.channel()
       
    def set_exchange(self):
        self.channel.exchange_declare( exchange=self.exchange, type='topic')
        
        # system will create queue name
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        
        
    #############################################################################
    def _callback(self, ch, method, properties, body ):
       ''' Save route key and message to MySql database '''
        
       conn = pymysql.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'messages')
       cur = conn.cursor()
        
       query = """
        insert into messages (route_key, message) 
        values(%s, %s)
        """
        
       cur.execute(query, (method.routing_key, body))
       conn.commit()
       
       print("wait 2 sec before selecting all, verify message in db")
       time.sleep(2)
       cur.execute('select * from messages')

       for row in cur:
         print(row)
   
       cur.close()
       conn.close()

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