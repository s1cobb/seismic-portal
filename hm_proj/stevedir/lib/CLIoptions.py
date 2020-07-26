import re
import sys
import select
import argparse
from getopt import getopt
from getopt import GetoptError

import UsageMsg

# currently --fi and --no instead

############################################################################
def process_options(input_args):
    ''' 
        This definition will check which option list to use depending on
        which command is being called.
        
        Verification/processing of options is done and a dictionary is 
        created with the option value.
    '''

    users = []
    optlist = []
    usr_list = []
    uid_list = []
    opt_dic = {}

    if re.search('uinfo', input_args[0]):
        optlist, usr_list, uid_list = gather_options(input_args)
        opt_dic = verify_opt_list(input_args[0], optlist, usr_list, uid_list)    
        return [opt_dic, usr_list, uid_list]
    elif re.search('rchain', input_args[0]):
        optlist, usr_list = gather_options(input_args)
        opt_dic = verify_opt_list(input_args[0], optlist, usr_list, uid_list)
        return [opt_dic, usr_list, uid_list]
    elif re.search('orginfo', input_args[0]):
        std_in = ''
        std_in = chk_stdin_orginfo()
        optlist = gather_options(input_args)
        opt_dic = verify_opt_list(input_args[0], optlist, usr_list, uid_list, std_in)    
        return [opt_dic]
    else:
        print('Error: Invalid command name: %s' % input_args[0])
        sys.exit()
        

############################################################################
def gather_options(input_args):
    '''
        Get the CLI option list. Modify the arguments before checking the options.
    '''
 
    users = []
    op_list = {}
    optlist = []
    usr_list = []
    uid_list = []
    fixed_args = []

    if re.search('uinfo', input_args[0]):
        # check for single dash, multiple chars
        fixed_args = fix_single_dash(input_args[1:])

        # process modified command line arguments
        try:
            option = ['all', 'name', 'location', 'help',
                      'contact','dept', 'department',
                      'pod', 'man', 'active', 'Active']

            optlist, users = getopt(fixed_args, 'acdnlh', option)
            usr_list, uid_list = cleanup_uinfo_options(users)
        except GetoptError as err:
            err_msg = '%s --> %s' % (err.msg, err.opt)
            print(err_msg)
            UsageMsg.uinfo_usage_info()
            sys.exit(1)
        return optlist, usr_list, uid_list
    elif re.search('rchain', input_args[0]):
         try:
             option = ['pod', 'man', 'help', 'debug']
             optlist, users = getopt(input_args[1:], 'OMRmrhdelnpt', option)
         except GetoptError as err:
             err_msg = '%s --> %s' % (err.msg, err.opt)
             print(err_msg)
             UsageMsg.rchain_usage_info()
             sys.exit(1)
         return optlist, users
    elif re.search('orginfo', input_args[0]):
        option = ['config=', 'userid=', 'emp_no=', 'dept_no=', 'bu=', 'tg=', 'format=',
                  'mgr=', 'display=', 'uid_no=', 'noheader', 'no', 'fi=', 'file=',
                  'nicknames', 'label=', 'uid=',  'man', 'pod', 'help', 'debug', 'stdin']

        # this definition is to give ability to have an argument on the
        # command line without an option. Perl was forgiving on this,
        # but Python was strict (not allowed), so this is the workaround. 
        fixed_args = format_fix_args(input_args[1:])

        # parse option list into dict
        try:
            optlist, users = getopt(fixed_args, 'c:u:e:d:b:t:f:m:nh', option)
        except GetoptError as err:
            err_msg = '%s --> %s' % (err.msg, err.opt)
            print(err_msg)
            UsageMsg.orginfo_usage_info()
            sys.exit(1)
        return optlist
    else:
        print('Error: Invalid command name: %s' % input_args[0])
        sys.exit()


############################################################################
def verify_opt_list(prog_name, op_list, usr_list, uid_list, std_input=''):
    '''
       Verify and validate the CLI option list.
    '''

    opt_dic = {}
    std_in = ''
    fixed_args = []

    if re.search('uinfo', prog_name):    
        # parse option list into dict
        for op in op_list:
            opt_dic[op[0]] = 1

        if '--help' in opt_dic or '-h' in opt_dic:
            UsageMsg.uinfo_help_msg()

        if '--pod' in opt_dic or '--man' in opt_dic:
            UsageMsg.uinfo_usage_info()

        if not usr_list and not uid_list:
            UsageMsg.uinfo_help_msg()

        if '--debug' in opt_dic:
            print('**** CLIoptions --> Uinfo processing ****')
            print('optlist -->', op_list)
            print('users   -->', usr_list)
            print('opt_dic -->', opt_dic)
            print('******************************************')
        return opt_dic
    elif re.search('rchain', prog_name):
        # parse option list into dict
        for op in op_list:
            opt_dic[op[0]] = 1

        # basic usage
        if '-h' in opt_dic or '--help' in opt_dic:
            UsageMsg.rchain_basic_info()

        # man page
        if '--pod' in opt_dic or '--man' in opt_dic:
            UsageMsg.rchain_usage_info()
        
        if not usr_list:
            UsageMsg.rchain_basic_info()

        if usr_list[0].isdigit():
            print('Error: Not a userid, you must use a userid...')
            sys.exit() 

        # can only have one userid
        if re.search(',', usr_list[0]):
            print('ERROR: Only one userid is valid...')
            UsageMsg.rchain_basic_info()

        # if -O, overrides -r,-R,-m, so remove them
        if '-O' in opt_dic:
            for fnd_opt in opt_dic.keys():
                if fnd_opt in ['-r', '-R', '-m']:
                    del opt_dic[fnd_opt]

        if '--debug' in opt_dic:
            print('**** CLIoptions --> Rchain processing ****')
            print('optlist -->', op_list)
            print('users   -->', usr_list)
            print('opt_dic -->', opt_dic)
            print('******************************************')
        return opt_dic
    elif re.search('orginfo', prog_name):
        std_in = std_input
        opt_dic = orginfo_optlist_to_dic(op_list)

        if 'man' in opt_dic or 'pod' in opt_dic or 'help' in opt_dic:
            UsageMsg.orginfo_usage_info()

        if std_in:
            if chk_for_usr_parm(opt_dic):
                UsageMsg.orginfo_usage_info() 
            else:
               opt_dic['userid'] = std_in
               
        chk_for_issues(opt_dic)
        
        # check for file option and value
        if 'file' in opt_dic:
            opt_dic['userid'] = chk_if_file_input(opt_dic['file'])
        
        if 'format' in opt_dic:
            if not opt_dic['format'] in ('text', 'csv', 'xml', 'perl'):
                print('\nUsage Error: Invalid display format, please select ' + \
                      "'text', 'xml', 'perl' or 'csv'\n\n")
                UsageMsg.orginfo_usage_info() 

        # check for one value only for specific options
        chk_for_only_one_value(opt_dic)

        if '--debug' in opt_dic:
            print('**** CLIoptions --> OrgInfo processing ****')
            print('optlist -->', op_list)
            print('opt_dic -->', opt_dic)
            print('******************************************')
        return opt_dic
    else:
        print('Error: Invalid command name: %s' % prog_name)
        sys.exit()


############################################################################
def cleanup_uinfo_options(all_users):
    '''
       Cleanup uinfo CLI parameters before processing.
    '''

    clean_users = []
    clean_uids = []

    ### IMPORTANT: Pay Attention Below ###
    # Note: empno_width should be 5 and not 6.  HR is not putting
    # a new 0 in front of old uids to pad them.  -ljr
    empno_width = 5;
    ### IMPORTANT: Pay Attention Above ###

    # remove this user before processing
    if 'devxads' in all_users:
        print('WARNING: User >devxads< rejected.')
        get_index = all_users.index('devxads')
        all_users.pop(get_index)

    # check for alpha or numeric id's, if TC in id
    # if TC in id add zeros to pad uid
    for emp_id in all_users:
        if emp_id.isalpha():
            clean_users.append("'" + emp_id + "'")
        elif emp_id.isdigit():
            clean_uids.append("'" + emp_id + "'")
        elif emp_id.isalnum():
            m = re.match('(TC)(\d+)$', emp_id)
            if m:
                tc =  m.group(1)
                emp = str(m.group(2))
                clean_uids.append("'" + tc + emp.zfill(empno_width) + "'")
            else:
                print('Invalid Employee ID: %s' % emp_id)
    return [clean_users, clean_uids]
    
############################################################################
def fix_single_dash(in_args):
    '''
       Add a - to short option form with mulitple chars.
       Example: -contact --> --contact
    '''

    fix_args = []

    chk_single_dash = ['-contact', '-location', '-name', '-help',
                       '-all', '-dept', '-department', '-pod',
                       '-man', '-active', '-Active']

    for o in in_args:
        if o in chk_single_dash:
            fix_args.append('-' + o)
        else:
            fix_args.append(o) 
    return fix_args

    
################ Section: definitions for orginfo processing ###############

############################################################################
def format_fix_args(op_list):
    '''
       Perl allowed short form options with multiple chars, Python does
       not allow this. This workaround will allow this for Python.

       Also check for non option CLI value, Perl allowed but Python
       does not allow. If found append userid to corrected args.
    '''
 
    cnt = 0
    usr_id = ''
    fixed_args = []
    tot_len = len(op_list)

    # workaround for option short form with multiple chars
    # pad with a extra -, to create a long option.
    for op in op_list:
        if re.match('^-\w{2,}', op):
            fixed_args.append('-' + op) 
        else:
            fixed_args.append(op)

    # check for userid without an option on CLI.
    for val in fixed_args:
        if cnt < tot_len: 
            if re.match('-\w', fixed_args[cnt]):
                cnt += 2 
                continue
            elif not re.match('-', fixed_args[cnt]):
                usr_id = fixed_args[cnt]
                fixed_args.pop(cnt) 
                tot_len -= 1
            elif re.match('--', fixed_args[cnt]):
                cnt += 1 

    if usr_id:
        fixed_args.append('--userid=' + usr_id)
    return fixed_args


def orginfo_optlist_to_dic(in_args):
    '''
       Convert the option list parameters into an dictionary for processing.
    '''

    op_dic = {}

    dic_val = {'-c': 'config', '-u': 'userid', '-e': 'emp_no', '-h': 'help',
               '-m': 'mgr', '-d': 'dept_no', '-b': 'bu', '-t': 'tg',
               '-f': 'format', '-n': 'nicknames'}

    for op in in_args:
        if op[0] in dic_val:
            if not op[1]:
                op_dic[dic_val[op[0]]] = 1
            else:
                op_dic[dic_val[op[0]]] = op[1]
        else:
            clean_op = op[0].lstrip('--')
            op_dic[clean_op] = op[1]
    return op_dic


############################################################################
def chk_stdin_orginfo():
    '''
       Check for userid info from the command line stdin
    '''

    uid_str = ''
    join_str = ','

    # get stdin, save input as a string        
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        uidstdin = sys.stdin.readlines()
        if uidstdin:
            uid_str = join_str.join(uidstdin)
            uidstr = uid_str.replace('\n', '')
            return uidstr
            break
        else:
            print('No stdin, keep trucking...')
            break


############################################################################
def chk_for_usr_parm(optdic):
    '''
       Check for userid option in command line options.
    '''

    for op in optdic:
        if op == 'userid' or op == 'emp_no':
            print("""Usage Error: Please use ONLY one of the following context options:
                  userid | mgr | dept_no | bu | tg | nicknames | file | stdin""")
            return True
    else:
        return False


############################################################################
def chk_for_issues(opt_dic={}):
    '''
       Verify we are not using a mix of options that are not allowed.
    '''

    cntall = []
    mat = re.compile('(userid|emp_no|uid_no|mgr|dept_no|bu|tg|' + \
                     'nicknames|file|help)')

    # verify total contexts from CLI
    cntall = [k for k in opt_dic.keys() if mat.search(k)]

    if len(cntall) == 0:
        UsageMsg.orginfo_help_msg() 

    if len(cntall) > 1:
        UsageMsg.orginfo_help_msg() 


############################################################################
def chk_if_file_input(filename=''):
    '''
       Check if a file is being used for userid input.
    '''

    if filename:
        join_str = ','

        try:
            with open(filename, "r") as fp:
                uids = fp.readlines()
            new_uids = join_str.join(uids).replace('\n','')
            return new_uids
        except IOError as err:
            print("Failed to open Filename: %s" % err)
            sys.exit(1)

    
############################################################################
def chk_for_only_one_value(opt_dic={}):
    '''
       Verify we are using only one value for the given option.
    '''

    chk_opts = ['mgr', 'dept_no', 'bu', 'tg']

    for one_val in chk_opts:
        if one_val in opt_dic:
            if re.search(',', opt_dic[one_val]):
                print('\nUsage Error: Please provide only one value for this context.\n')
                UsageMsg.orginfo_usage_info()

