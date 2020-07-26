import os
import re
import sys
import cx_Oracle

class DB(object):
    '''
       This class does all the work for database interaction. 
       Definitions will load the database configuration file, 
       connect to the database, send the query request to the
       database and close connection to database.
    '''
       
    def __init__(self, opts):
        self.db_info = {} 
        self.opts = opts
        self.cursor = ''


    ###################################################################################
    def load_db_config_file(self):
        '''
           This definition will check for a database config and load the user,
           password and SID for the database connection.
        '''

        if not '--config' in self.opts:
            self.opts['--config'] = '/opt/db/db.cfg'
        
        # does file exists
        if not os.path.isfile(self.opts['--config']):
            print('Required config file was either not found or readable,' + \
                  ' please either:\n- Run from an EngIT secured Admin Host\n' + \
                  '- Or supply a valid configuration file using the' + \
                  '--config option')
            sys.exit(1)

        # is file readable
        try:
            fp = open(self.opts['--config'], 'r')
        except IOError:
            print('File is not readable: %s' % self.opts['--config'])
            sys.exit(1)

        # load database config
        for line in fp:
            k, v = line.split(':')
            if re.match('sid|usr|pwd', k):
                self.db_info[k] = v.replace('\n','')

        if 'sid' not in self.db_info:
            print('sid db key not found in ' + self.opts['--config'] + ' config file')
            fp.close()
            sys.exit()
        fp.close()


    ###################################################################################
    def select_qry_data(self, qry_str):
        '''
           Execute the query string and return the data in a dictionary format.
        '''

	res_dic = []
    	try:
            self.cursor.execute(qry_str)
            column_names = list(map(lambda x: x.lower(), [d[0] for d in self.cursor.description]))
            rows = list(self.cursor.fetchall())
            res_dic = [dict(zip(column_names, row)) for row in rows]

            if not res_dic:
                print('Error: No data returned, your input values may be invalid...')
                self.close_db()
                sys.exit()
            else:
	        return res_dic
        except cx_Oracle.DatabaseError as err:
            print('Error: Failed to fetch data - %s' % err)
	    self.close_db()
	    sys.exit()
 

    ###################################################################################
    def connect(self):
        '''
           Connect to HR database and return the cursor for query execution.
        '''

        dsn_tsn = cx_Oracle.makedsn('removed', 'removed', sid=self.db_info['sid'])
        try:
            self.db = cx_Oracle.connect(user=self.db_info['usr'],
                                        password=self.db_info['pwd'],
                                        dsn=dsn_tsn)
            self.cursor = self.db.cursor()
        except cx_Oracle.DatabaseError as err:
            print('Database connection failure - %s' % err)
            sys.exit(1)
    
    
    ####################################################################################
    def close_db(self):
        '''
            Close cursor and database connection.
        '''

        try:
            self.cursor.close()
            self.db.close()
        except cx_Oracle.DatabaseError as err:
            print('Failed to close database connection - %s' % err)

if __name__ == '__main__':
   # for testing connection, query and return data
   qry_str = 'select * removed where rownum < 2'
   opts = {'--file': '/opt/db/db.cfg'}

   db = DB(opts)
   db.load_db_config_file()
   db.connect()
   resp = db.select_qry_data(qry_str)
   print(resp)
   db.close_db()
