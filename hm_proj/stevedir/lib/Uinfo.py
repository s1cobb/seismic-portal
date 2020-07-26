import re
import sys
from cx_Oracle import DatabaseError

from DataBase import DB

class Uinfo(object):
    def __init__(self, user_and_opts=[]):
        self.options = user_and_opts[0]
        self.allusers = user_and_opts[1]
        self.alluids = user_and_opts[2]

        # setup Data base object
        self.db = DB(self.options)
        self.db.load_db_config_file()
        self.db.connect()

    ###################################################################################
    def setup_uinfo_qry(self):
        '''
           Format the query message and return the query message.
        '''

        active = ''
        join_str = ','
        qry_strs = []

        # fields for uinfo
	fields =['removed']

        # set for active employee parameter
        if '--active' in self.options or '--Active' in self.options:
            active = " AND status IN ('A', 'L')"
                
        if self.allusers:
            qry_str = 'select ' + join_str.join(fields) + ' from where ' + \
            'userid in (' + join_str.join(self.allusers) + ')' + active + ' order by emp_no' 
            qry_strs.append(qry_str)
                   
        if self.alluids:
            qry_str = 'select ' + join_str.join(fields) + ' from  where ' + \
            'emp_no in (' + join_str.join(self.alluids) + ')' + active + ' order by emp_no' 
            qry_strs.append(qry_str)

        return qry_strs


    ####################################################################################
    def get_inputted_options(self):
        '''
            Grab all valid options and add to a list.
        '''

        prt_opts = []
        opt_order = ['-n', '-l', '-c', '-d']
        
        for opt_key in self.options.keys():
            if re.search('(^-a|--all)', opt_key):
                prt_opts.extend(opt_order)
                break
            else:
                if re.search('-n|--name', opt_key):
                    prt_opts.append('-n')
                if re.search('-l|--location', opt_key):
                    prt_opts.append('-l')
                if re.search('-d|--(dept|department)', opt_key):
                    prt_opts.append('-d')
                if re.search('-c|--contact', opt_key):
                    prt_opts.append('-c')
        return prt_opts


    ####################################################################################
    def display_uinfo_data(self):
        '''
           Display the database information to standard out.
        '''

        db = {}      # dictionary of data from database
        name = ''    # holds the full name
        data = []    # holds the parsed database record
        fld_len = 13 # size of field to print col name
        prt_all = 0  # if true print all data

        # remove config option, not needed now
        del self.options['--config']
        
        # returns the SQL select statements
        qstrs = self.setup_uinfo_qry()
        
        # set correct field print out order
        opt_flgs = {'removed'},

        opt_order = ['-n', '-l', '-c', '-d']
        
        # get all valid options
        val_opts = []
        val_opts = self.get_inputted_options()
        
        for q in qstrs:
            # call query request
            rsp = self.db.select_qry_data(q)

            # process query response
            for db in rsp:
                if not self.options:
                    print('%s     %s     %s' % (db['userid'], db['emp_no'], db['status']))
                else:
                    # set name, check for middle initial
                    name = db['f_name'] + ' ' + db['l_name']
                    db['name'] = name
                    
                    # print out record here
                    print("%s:  %s" % ('userid'.ljust(fld_len), db['userid']))
                    print("%s:  %s" % ('emp_no'.ljust(fld_len), db['emp_no']))
                    for op in opt_order:
                        if op in val_opts:
                            for fld in opt_flgs[op]:
                                print('%s:  %s' % (fld.ljust(fld_len), db[fld]))
                    print("%s:  %s" % ('emp_type'.ljust(fld_len), db['emp_type']))
                    print("%s:  %s\n" % ('status'.ljust(fld_len), db['status']))
        self.db.close_db()

