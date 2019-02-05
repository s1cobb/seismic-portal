import sys
from datetime import datetime
import mysql.connector as mariadb

class DataDB:
   def __init__(self, logspk ):
       self.conn   = ''
       self.cursor = ''
       self.logspk = logspk

       self.confquery = "INSERT INTO conference_data (CoSpace_id, Name, Autogenerated," \
                         " Uri, CallId, SecondaryUri, date_received, Ip, local_remote," \
                         "contract, month ) " \
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
       self.devquery  = "INSERT INTO device_data (TotalDevices, TotalUsers, EnhancedPlus," \
                         " Enhanced, TelePresence,CuwlStandard, Basic, Essential, Timestamp," \
                         " Elm, ElmLastContact, date_received, Ip, local_remote, contract, month) " \
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

       try:
          self.conn = mariadb.connect(database='Billing')
          self.cursor = self.conn.cursor()
       except mariadb.Error as db_error:
         self.logspk.error("CUCM/CMS billing database connection failure: %s " % db_error) 


   def load_data_db(self, xml_type, tmplis, serv_info):
        ''' Inserts the device/usage and conference room data into database '''

        inserts_ok = 0
        d = datetime.today()
        month = d.strftime('%B')
        todays_date = d.strftime('%y-%m-%d') + ' ' + d.strftime('%H:%M:%S')
        
        if self.conn:
           if xml_type == 'conf_spaces':
              tmpdic = tmplis[1]
              try:
                 insert_data = (tmpdic['coSpace id'], tmpdic['name'], tmpdic['autogenerated'],
                                tmpdic['uri'], tmpdic['callId'], tmpdic.get('secondaryUri',
                                'None'), todays_date, serv_info['ip_address'], 
                                serv_info['local_or_remote'], serv_info['contract'], month)

                 self.cursor.execute(self.confquery, insert_data)
              except mariadb.Error as db_error:
                 inserts_ok = 1
                 self.logspk.error("%s:%s:%s:%s:%s Database inserting failure for conference data: %s" \
                                   % ( serv_info['contract'], month, serv_info['target'], serv_info['local_or_remote'],
                                       serv_info['ip_address'], db_error))

              if not inserts_ok:
                 self.conn.commit()
           elif xml_type == 'devices':
              tmpdic = tmplis[0]
              try:
                 # data to be inserted into database
                 insert_data = (tmpdic['TotalDevices'], tmpdic['TotalUsers'], tmpdic['EnhancedPlus'],
                                tmpdic['Enhanced'], tmpdic['TelePresence Room'], tmpdic['CUWL Standard'],
                                tmpdic['Basic'], tmpdic['Essential'], tmpdic['Timestamp'],
                                tmpdic['Elm'], tmpdic['ElmLastContact'], todays_date, serv_info['ip_address'], 
                                serv_info['local_or_remote'], serv_info['contract'], month )
                 self.cursor.execute(self.devquery, insert_data)
              except mariadb.Error as db_error:
                 inserts_ok = 1
                 self.logspk.error("%s:%s:%s:%s:%s Database inserting failure for device/usage data: %s" \
                                   % (serv_info['contract'], month, serv_info['target'], serv_info['local_or_remote'],
                                      serv_info['ip_address'], db_error))

              if not inserts_ok:
                 self.conn.commit()


   def close_db_access(self):
       if self.conn:
          self.conn.close()
