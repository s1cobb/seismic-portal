import os
import sys
import csv
from xml.dom import minidom
from datetime import datetime
import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from DataBase import DB
from ValidColumns import column_list

class OrgInfo:
    '''
        This class will gather data from the HRMS database by issuing
        database queries. Data can be collected by using the userid,
        emp_no or uid_no. The whole record can be printed or individual
        fields can be selected depending on if the --display options is 
        used.
    '''
 
    def __init__(self, opts_user):
        self.options = opts_user[0]
	self.qry_str = ''
	
	# setup Data base object
	self.db = DB(self.options)
	self.db.load_db_config_file()
	self.db.connect()

        
    ##################################################################################
    def verify_or_show_valid_col_flds(self):
        '''
           For the display option verify the column names used are valid column
           names in the database. Print all columns if option <nicknames> is used.
        '''
           
	err = 0
	fixusr = ''
	disp_rsp = []
	err_msg = '\nUsage Error: The following display attributes are invalid ' 

	# show valid column names that are valid for --display attribute
	if 'nicknames' in self.options:
	    print('\nYou can use the following nicknames to limit your output to' + \
                  ' only those values\nsupplied in the comma delimited list of the' + \
	          ' --display parameter:\n')

            for k in column_list:
                print('   - %s' % k)
            print('\nFor Example:\n   $ orginfo --userid=jsmith --display=tech_group')	    
            sys.exit(1)

	# verify display attributes are valid
        if 'display' in self.options:
            for fld in self.options['display'].split(','):
                if not fld in column_list:
                    err = 1
                    err_msg += '  - ' + fld

            if err:
                err_msg += '\nType orginfo --nicknames for a list of valid values\n'
                print(err_msg)
                self.db.close_db()
                sys.exit()

        if '--debug' in self.options:
            print('**** OrgInfo --> verify_or_show_valid_col_flds ****')
            print(self.options['display'])
            print('****************************************************')
	

    ##################################################################################
    def create_qry_request(self):
        '''
           Format the query message and return the query message.
        '''

	fixusr = ''
	col_name = ''

	for op in self.options.keys():
	    if op == 'userid': 
		self.qry_str = 'select * from where lower(userid) in ('
                for usr in self.options[op].split(','):
                    lower_usr = usr.lower()
                    fixusr += "'" + lower_usr + "',"
	        break
	    elif op == 'emp_no':
		self.qry_str = 'select * from where emp_no in ('
                for usr in self.options[op].split(','):
                    fixusr += "'" + usr + "',"
                break
	    elif op == 'uid_no':
		self.qry_str = 'select * from where emp_no in ('
                for usr in self.options[op].split(','):
                    usr = str(int(usr) - 1000).zfill(5)
                    fixusr += "'" + usr + "',"
                break
	    elif op == 'mgr':
                if self.options[op] == self.ceo:
                    print('Error: The result set will be too large for ' + self.ceo)
                    sys.exit()

		self.qry_str = 'select * from where rchain ' + \
	                  "like '%" + self.options[op].lower() + \
                          "%' and status in ('A', 'L', 'P')"
                break
	    elif op == 'dept_no':
		self.qry_str = 'select * from ' + \
	                  "where dept_no = '" + self.options[op].lower() + \
                          "' and status in ('A', 'L', 'P')"
                break
	    elif op == 'bu':
		self.qry_str = 'select * from ' + \
	                  "where lower(business_unit_name) = '" + self.options[op].lower() + \
                          "' and status in ('A', 'L', 'P')"
                break
	    elif op == 'tg':
		self.qry_str = 'select * from ' + \
	                  "where lower(tech_group) = '" + self.options[op].lower() + \
                          "' and status in ('A', 'L', 'P')"
                break

        if op in ('userid', 'emp_no', 'uid_no'):
	    newfix = fixusr.rstrip(',')
	    self.qry_str += newfix + ')'

        if '--debug' in self.options:
            print('**** OrgInfo --> create_qry_request ****')
            print('qry_str - ', self.qry_str)
            print('*****************************************')


    ##################################################################################
    def output_text_format(self):
        ''' Outputs the data in TEXT format. Default output. '''

	total_objs = 0
	
	# query database
        disp_rsp = self.db.select_qry_data(self.qry_str)
        if not disp_rsp:
	    self.db.close_db()
            print('ERROR: The ID used was not found in database...') 
            sys.exit()
            

        # process each database record 
	for record in disp_rsp:
            total_objs += 1
            
            if 'label' in self.options:
                print('%s : %s' % ('LABEL'.rjust(20), self.options['label']))
            print('%s : %s' % ('USERID'.rjust(20), record['userid']))

            # remove userid, already printed above
            del record['userid']

            if 'display' in self.options:
                sorted_flds = sorted(self.options['display'].split(','))

                # if display value found in database record, then print
                for fld in sorted_flds:
                    if type(record[fld]) is datetime:
                        record[fld] = record[fld].strftime('%d-%b-%y')
                    if fld.lower() in record:
                        print('%s : %s' % (fld.upper().rjust(20), record[fld]))
            else:
                for k in sorted(record.keys()):
                    if type(record[k]) is datetime:
                        record[k] = record[k].strftime('%d-%b-%y')
                    print('%s : %s' % (k.upper().rjust(20), record[k]))
            print(' ')
	print("Total objects: %i" % total_objs)


    ##################################################################################
    def output_csv_format(self):
        ''' Outputs the data in CSV format. '''
 
        csv_hdr = []
        tmp_lis = []
        csv_data = []
        csv_col = 0
    
	# query database
        disp_rsp = self.db.select_qry_data(self.qry_str)

        wr = csv.writer(sys.stdout)
	for total, record in enumerate(disp_rsp, start=1):
             
            # setup csv header information, do only once
            if total == 1:
                if 'label' in self.options:
                    csv_data.append('LABEL')
                csv_data.append('REC#')
                csv_data.append('USERID')
 
                if 'display' in self.options:
                    csv_hdr = sorted(self.options['display'].split(','))
                else:
                    csv_hdr = sorted(record.keys())
                csv_data.extend([x.upper() for x in csv_hdr])

                if 'noheader' in self.options or 'no' in self.options:
                    pass
                else: 
                    wr.writerow(csv_data) 

            # if label option, add it to record, increment col length
            if 'label' in self.options:
                tmp_lis.append(self.options['label'])
                csv_col = 3
            else:
                csv_col = 2

            tmp_lis.append(str(total))
            tmp_lis.append(record['userid'])

            # append data to list, write out the list
            for fld in csv_data[csv_col:]:
                if fld == 'USERID':
                    pass
                if type(record[fld.lower()]) is datetime:
                    record[fld.lower()] = record[fld.lower()].strftime('%d-%b-%y')
                tmp_lis.append(record[fld.lower()])
            wr.writerow(tmp_lis)
            tmp_lis = []


    ##################################################################################
    def output_xml_format(self):
        ''' Outputs the data in XML format. '''

        num_rec = ''
        num_tag = ''
        tmp_rec = {}
 

	# query database
        disp_rsp = self.db.select_qry_data(self.qry_str)

        start = et.Element('UserOrgInfo')     
        for rec_num, record in enumerate(disp_rsp, start=1):
            if 'display' in self.options:
                self.options['display'] += ',userid'
                for tmp in sorted(self.options['display'].split(',')):
                    tmp_rec[tmp] = record[tmp]

                if 'label' in self.options:
                    tmp_rec['label'] = self.options['label']
            else:
                tmp_rec = record
                if 'label' in self.options:
                    tmp_rec['label'] = self.options['label']

            # setup xml record number, num_rec is subelement
            num_tag = '_' + str(rec_num)
            num_rec = et.SubElement(start, num_tag)
                
            # each value is added to the xml subelement
            for k in sorted(tmp_rec.keys()):
                if type(tmp_rec[k]) is datetime:
                     tmp_rec[k] = tmp_rec[k].strftime('%d-%b-%y')
                et.SubElement(num_rec, k.upper()).text = tmp_rec[k]
        xml_data = et.tostring(start, 'utf-8')
        reparsed = minidom.parseString(xml_data)
        print(reparsed.toprettyxml(indent="   "))
        

    ##################################################################################
    def output_perl_format(self):
        ''' Outputs the data in PERL format. '''

	# query database
        disp_rsp = self.db.select_qry_data(self.qry_str)

        print("my $orgResult = {")
	for record in disp_rsp:
            print("   '" + record['userid'] + "' => {")
            
            if 'label' in self.options:
                print("      '%s' => '%s'," % ('LABEL', self.options['label']))
            print("      '%s' => '%s'," % ('USERID', record['userid']))
            del record['userid']

            if 'display' in self.options:
                sorted_flds = sorted(self.options['display'].split(','))
                for fld in sorted_flds:
                    if type(record[fld]) is datetime:
                        record[fld] = record[fld].strftime('%d-%b-%y')
                    if fld.lower() in record:
                        print("      '%s' => '%s'," % (fld.upper(), record[fld]))
            else:
                for k in sorted(record.keys()):
                    if type(record[k]) is datetime:
                        record[k] = record[k].strftime('%d-%b-%y')
                    print("      '%s' => '%s'," % (k.upper(), record[k]))
            print('   },')
        print('};')


    ##################################################################################
    def display_orginfo_data(self):
        ''' Check the format option and print in that format. '''

        # default format value
        wr_fmt = 'text'

	self.verify_or_show_valid_col_flds()
	self.create_qry_request()
	
        if 'format' in self.options:
            wr_fmt = self.options['format']

	if wr_fmt == 'text': 
	    self.output_text_format()
	elif wr_fmt == 'csv':
            self.output_csv_format()
        elif wr_fmt == 'xml':
            self.output_xml_format()
        elif wr_fmt == 'perl':
            self.output_perl_format()
	self.db.close_db()
