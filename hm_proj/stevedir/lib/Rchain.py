import re
import sys
import cx_Oracle

import pdb
from DataBase import DB

class Rchain(object):
    def __init__(self, opts_usr_ids=[]):
        self.options = opts_usr_ids[0]
        self.allusers = opts_usr_ids[1]
        self.qry_flds = ''
        self.mgr_order = []

        # setup Data base object
        self.db = DB(self.options)
        self.db.load_db_config_file()
        self.db.connect()


    ###################################################################################
    def format_rchain_output(self, rsp):
        '''
           Formats the output based on the number of fields to print.
           Uses an eval command to process the created print strings.
        '''

        resp = []

        # data comes back from database out of order, this corrects the order for print out
        if '-r' in self.options or '-R' in self.options:
            resp = rsp
        else:
            resp = [rec for nam in self.mgr_order for rec in rsp if rec['userid'] == nam]


        # column to print and the field size to print the data
        outp = [('userid',14), ('f_name',1), ('l_name', 10), ('title', 30),
                ('work_number', 16), ('dept_no',11), ('building', 20), ('emp_no',7)]

        if '--debug' in self.options:
            print('***** Rchain --> format_rchain_ouput ****')
            print(rsp if rsp else 'missing database data response')
            print('******************************************')

        # if -r and -m and len of rsp is 1 then dont print single user value
        if len(resp) == 1 and '-m' in self.options and \
                     ('-r' in self.options or '-R' in self.options):
            return

        if resp:
            prt_this_many = ''

            # depending on num of cols, add %s's to print each col
            for i in range(len(resp[0])):
                if i == 6:
                    prt_this_many += r'\n%s'
                else:
                    prt_this_many += '%s '

            # format fields for printing similiar to the old rchain format
            # check each output record for the column values in outp dic.
            for r in resp:
                vals = ''

                for val in outp:
                    if val[0] in r:
                        if val[0] == 'userid':
                            vals += "'" + r[val[0]] + "'.ljust(" + str(val[1]) + "),"
                        else:
                            vals += "'" + str(r[val[0]]) + "'.ljust(" + str(val[1]) + "),"

                try:
                    print(eval("'" + prt_this_many + "' % " + '(' + vals + ')'))
                except TypeError as err:
                    print(err)


    ###################################################################################
    def format_manager_output(self, rsp):
        ''' Get and process the remove column data, parse the data
            into a comma separated string.
        '''

        join_str = ','
        mgr_list = []
        fixed_str = ''

        # reverse the rchain data for correct output order
        mgr_list = rsp[0]['removed'].rstrip(':').split(':')
        self.mgr_order = list(reversed(mgr_list))

        # -M, use the manager's name instead of user, so remove user
        if '-M' in self.options:
            self.mgr_order.pop(-1)

        for val in self.mgr_order:
            fixed_str += "'" + val.lower() + "',"
        fixed_str = fixed_str.rstrip(',')

        if '--debug' in self.options:
           print('**** Rchain --> format_manager_output ****')
           print('rchain data --> ', fixed_str)
           print('*******************************************')
        return fixed_str


    ###################################################################################
    def get_user_reports(self):
        ''' If the userid is a manager get the immediate reports. '''

        user_str = ''

        # Show user's reports. ex: who reports to the manager
        qry_str = 'select remove from  ' + \
                  "where remove LIKE '%" + self.allusers[0].lower() + \
                  "%' and status in ('A', 'L', 'P')"
        rsp = self.db.select_qry_data(qry_str)

        # if > 1, then you have immediate reports, process then
        if len(rsp) > 1:
            for val in rsp:
                if val['userid'].lower() == self.allusers[0].lower():
                    # don't print userid value when -O,-m
                    if '-O' in self.options or '-m' in self.options:
                        continue
                user_str += "'" + val['userid'].lower() + "',"
            user_str = user_str.rstrip(',')

            # create query string of column fields
            qry_str = 'select ' + self.qry_flds + ' from ' + \
                      'where lower(userid) in (' + user_str + ') order by lower(userid)'
            rsp = self.db.select_qry_data(qry_str)

            if '--debug' in self.options:
                print('**** Rchain --> get_user_reports ****')
                print('    user reports --> ', user_str)
                print('    rsp --> ',rsp)
                print('**************************************')
            return rsp
        else:
            # create query string of column fields, user has no reports
            user_str = rsp[0]['userid']
            qry_str = 'select ' + self.qry_flds + ' from  ' + \
                      "where lower(userid) in ('" + user_str + "') order by lower(userid)"
            rsp = self.db.select_qry_data(qry_str)
            return rsp


    ###################################################################################
    def format_print_org_chart(self, ppl_data, reports):
        '''
           For printing similiar to the old rchain format. (-O option)
           Format a print string, use eval to process the print string.
           example:
           potter
             |--sammy 
             |    |--joel 
        '''

        sp_cnt = 0         # number of spaces to indent
        prt_fld = ''       # number of %s to use for printing
        ppldata = []       # holds the ordered records
        subtract_num = 1   # used for indent positions
        prt_this_many = '' # formats the number of %s
        hdrs = ['  |', '    |', '--']

        outp = [('userid',0), ('f_name',1), ('l_name', 1), ('title', 1), ('work_number', 1),
                ('dept_no',2), ('building',1), ('emp_no',1)]

        # data comes back from database out of order,  this corrects the order for print out
        ppldata = [rec for nam in self.mgr_order for rec in ppl_data if rec['userid'] == nam]

        if '--debug' in self.options:
             print('**** Rchain --> format_print_org_chart ****')
             print(ppldata)
             print('********************************************')

        if ppldata:
            prt_this_many = ''
            for i in range(len(ppldata[0])):
                if i == 5:
                    prt_this_many += r'\n%s '
                else:
                    prt_this_many += '%s '

            # output org chart with header spacing, etc
            for space_cnt, resp in enumerate(ppldata, start=0):
                vals = ''

                for val in outp:
                    if val[0] in resp:
                        if val[0] == 'userid':
                            vals += "'" + resp[val[0]] + "',"
                        else:
                            vals += "'" + str(resp[val[0]]) + "',"

                # eval the format setup and print data
                try:
                    if space_cnt == 0:
                        print(eval("'" + prt_this_many + "' % " + '(' + vals + ')'))
                    elif space_cnt == 1:
                        hdr = hdrs[0] + hdrs[2]
                        prt_fld = '%s' + prt_this_many
                        print(eval("'" + prt_fld + "' % " + "('" + hdr + "'," + vals + ')'))
                    else:
                        sp_cnt = space_cnt - subtract_num
                        hdr = hdrs[0] +  hdrs[1] * sp_cnt + hdrs[2]
                        prt_fld = '%s' + prt_this_many
                        print(eval("'" + prt_fld + "' % " + "('" + hdr + "'," + vals + ')'))
                except TypeError as err:
                    print(err)
        else:
            print("No valid data returned, cannot output Org chart")

        if '--debug' in self.options:
             print('**** Rchain --> format_print_org_chart ****')
             print('user reports ' , ppldata)
             print('********************************************')

        # print the userid's immediate reports
        if len(reports) > 1:
            if reports:
                sp_cnt += 1
                hdr = hdrs[0] +  hdrs[1] * sp_cnt + hdrs[2]

                for resp in reports:
                    vals = ''

                    for val in outp:
                        if val[0] in resp:
                            vals += "'" + str(resp[val[0]]) + "',"

                    try:
                        print(eval("'" + prt_fld + "' % " + "('" + hdr + "'," + vals + ')'))
                    except TypeError as err:
                        print(err)

        if '--debug' in self.options:
            print('processing in format_print_org_chart...\n')


    ###################################################################################
    def basic_rchain_output(self):
        ''' Prints the data in basic format.
        '''

        join_str = ','
        prt_order = []
        get_fields = []
        fixed_flds = []

        # used to print correct sequence
        outp = ['userid', 'f_name', 'title', 'work_number', 'dept_no', 'building', 'emp_no']

        # depending on which option used, get the correct column to print
        opt_flds = {'-d': 'dept_no', '-e': 'emp_no', '-l': 'building',
                 '-n': 'f_name', '-p': 'work_number', '-t': 'title', '-M': 'userid',
                 '-m': 'userid', '-r': 'userid', '-R': 'userid', '-O': 'userid'}

        # for each option get the required SQL field
        get_fields = [opt_flds[opt] for opt in self.options if opt in opt_flds]
        if 'userid' in get_fields:
            pass
        else:
            get_fields.append('userid')

        # set the correct field order for printing
        for fld in outp:
            if fld in get_fields:
               fixed_flds.append(fld)

               # if fname used, get the lname field
               if fld == 'f_name':
                   fixed_flds.append('l_name')

        self.qry_flds = join_str.join(fixed_flds)
        qry_str = 'select rchain from ' + \
                  ' where lower(userid) = ' + "'" + self.allusers[0].lower() + "'"

        # -r, -R get users immediate reports
        if '-r' in self.options or '-R' in self.options:
            # if -M, need to get users manager instead of user
            if '-M' in self.options:
                rsp = self.db.select_qry_data(qry_str)
                names = self.format_manager_output(rsp)
                self.allusers[0] = names.split(',')[-1].strip("'")
            elif '-m' in self.options:
                rsp = self.db.select_qry_data(qry_str)
                names = self.format_manager_output(rsp)
                qry_str = 'select ' + self.qry_flds + ' from ' + \
                          'where lower(userid) in (' + names + ')'
                rsp = self.db.select_qry_data(qry_str)
                self.format_rchain_output(rsp)
            rsp = self.get_user_reports()
            return rsp

        # get management chain
        rsp = self.db.select_qry_data(qry_str)
        if rsp:
            names = self.format_manager_output(rsp)

            # if -M, need to get users manager instead of user
            if '-M' in self.options:
               self.allusers[0] = names.split(',')[-1].strip("'")
        else:
            self.db.close_db()
            print('No data returned from query for the userid given:' ,self.allusers[0])
            sys.exit()

        # process -m,d,e,l,n,p,t with manager names list
        qry_str = 'select ' + self.qry_flds + ' from ' + \
                  'where lower(userid) in (' + names + ')'
        rsp = self.db.select_qry_data(qry_str)

        if '-O' in self.options:
            return rsp
        else:
            self.format_rchain_output(rsp)


    ###################################################################################
    def display_rchain_data(self):
        ''' Depending on which options used, this definition will call the
            correct sequence of class methods for data processing. '''

        reports = {}
        if '-R' in self.options or '-r' in self.options:
            self._basic_rchain_output()
            reports = self.get_user_reports()
            self.format_rchain_output(reports)
        elif '-O' in self.options:
            # Show org chart
            basic_data = self.basic_rchain_output()
            reports = self.get_user_reports()
            self.format_print_org_chart(basic_data, reports)
        else:
            self.basic_rchain_output()
        self.db.close_db()
