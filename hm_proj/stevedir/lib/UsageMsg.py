from sys import exit

#####################################################################
def orginfo_help_msg():
    msg = '''
    Please use one of the following context options:
       userid | emp_no | uid_no | mgr | dept_no | bu | tg | nicknames | file | stdin

    Usage:
        Display organization information for a supplied UserID, Manager,
        Department, Business Unit or Technical Group.

     $ orginfo -h (for help)
'''
    print(msg)
    exit()


def orginfo_usage_info():
    msg = '''
    This script displays organization information for a supplied UserID,
    Manager, Department, Business Unit or Technical Group. Multiple output
    formats (text/tag, xml, perl hash & csv) are available for the user to
    choose from.

  Examples:
    Display a user's org info in standard text/tag format (the default).
    $ orginfo jsmith <default behavior>
    $ orginfo jsmith --config=/path/to/configfile
    $ orginfo --userid=jsmith(,bjones,jcarson)
    $ orginfo --file=userid.list
    $ cat userid.list | orginfo

    Display a user's org info by employee number.
    $ orginfo --emp_no 180176

    Display a user's org info by UID number.
    $ orginfo --uid_no 181176

    Display a manager's org info in CSV format.
    $ orginfo --mgr=vbollapr --format=csv

    Display a BU's org info in XML format.
    $ orginfo --bu=IMSBU --format=xml

    Display a TG's org info, but display specified fields only.
    $ orginfo --tg=WSTG --display=building,dept_name,business_unit_name

    Display the list of org info attribute nicknames.
    $ orginfo --nicknames

OPTIONS

   --config|c configfile

   DB config file (db read access) in the following format:

   sid:engitdb
   usr:your_db_usr
   pwd:your_db_pw

   --userid|u=userid1(,2,3...)
   UserID or comma separated list of UserIDs to display their org info data.

   --emp_no|e=emloyee_number(,2,3...)
   Employee Number or comma separated list of Employee #s to display their org info data.

   --uid_no|uid=uid_no(,2,3...)
   UID Number or comma separated list of UID #s to display their org info data.

   --mgr|m=mgr_userid
   A manager's UserID to display his team's org info.

   --dept_no|d="dept no"
   A department number to display dept team's related org info.

   --bu|b="bu name"
   A business unit name to display bu team's related org info.

   --tg|t="tg name"
   A tech group name to display tg team's related org info.

   --nicknames|n
   To list org info attribute nicknames available for display.

   --display=nickname_1,nickname_2,nickname_3...
   Specify a list of org info attribute nicknames to display.

   --format=text|perl|xml|csv [suppress CSV header with --noheader]
   Specify the desired output format (text is default).

   --label
   Add the supplied label string to each record (for example a host name).

   --debug
   Option for debugging the code

   --help|h
   Option to display a help page.

   --pod|man
   Option to display complete POD/MAN documentation.

   ********************************************************
   OTHER INPUT OPTIONS


   --file=path-to-file
   An input file containing a list of UserIDs (one per line).

   STDIN
   An input stream of UserIDs (one per line).


   AUTHOR
   Steve Cobb (18-May-2020)
'''
    print(msg)
    exit()

######################################################################
def uinfo_help_msg():
    msg = '''
Usage:
    uinfo [-acdln] { userid | emp_no } ...

    uinfo { --pod | --man | --bugit }
'''
    print(msg)
    exit()


######################################################################
def uinfo_usage_info():
    msg = '''
    uinfo - display user information from the HR database


    uinfo [-acdln] { userid | emp_no } ...

    uinfo { --pod | --man | --bugit }

 DESCRIPTION

    Display information from the HR database given an emp_no or userid.
    The user's employee number, userid, and status are always displayed.

 OPTIONS

    -a | --all
       Turn on all options.

    -c | --contact
       Display contact information.  This consists of the user's work
       number, beeper number, cellular number, fax number and mailstop.

    -d | --department
       Display department information.  This consists of the user's
       department name, department number, supervisor's name,
       supervisor's employee number, and support orginazation.

    -l | --location
       Display location information.  This consists of the user's site,
       building, floor, and cube number.

    -n | --name
    Display naming information.  This consists of the user's name
    and title.

    --Active
      The <Active> option will only return active employees.  (I.e.,
      those with a status of 'Employee' or 'Contingent Worker'.)

    --bugit
      Option for debugging code


 AUTHOR
     Steve Cobb 5/27/20 '''

    print(msg)
    exit()


######################################################################
def rchain_usage_info():
    msg = '''
NAME

    rchain - display reporting chains.

SYNOPSIS

    rchain [--debug] [-O|MRmr] [-hdelnpt] user

    rchain { --pod | --man | --debug }

    NOTICE: Please note that rchain is provided as a convenience utility.
    The supported method of reporting chain look-up in Cisco is the
    web page found at http://directory.cisco.com

DESCRIPTION

    Displays reporting chain information queried from the HR database.
    The rchain script connects to the rchain daemon and echos back
    the information received.

OPTIONS

    O - Show org chart.  (Overrides -R, -m, and -r options.)
    M - Act on user's manager instead of user.
    R - Show user's reports recursively.  (Overrides -r option.)
    m * Show user's management chain.  (This is the default.)
    r - Show user's reports.
    h - Do not show Cisco Confidentiality header.
    d - Show department numbers.
    e - Show employee numbers.
    l - Show locations.
    n - Show names.
    p - Show phone numbers.
    t - Show titles.

    --pod | --man  
    Display this documentation.

    --debug
    Option for debugging code
'''
    print(msg)
    exit()


######################################################################
def rchain_basic_info():
    msg = '''
Usage:
    rchain [-O|MRmr] [-dehlnpt] user

    rchain { --pod | --man | --debug }

    * Please note that rchain is provided as a convenience utility.
    The supported method of reporting chain look-up in Cisco is the
    web page found at http://directory.cisco.com
'''
    print(msg)
    exit()
