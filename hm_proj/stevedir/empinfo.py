#!/usr/bin/python

# This script implements the integration of the 
# uinfo, rchain and orginfo scripts into one 
# application. 

import re
import sys

from lib.CLIoptions import process_options

# holds the command line options and user ids
opts_users = []
opts_users = process_options(sys.argv)

if re.search('uinfo', sys.argv[0]):
    from lib.Uinfo import Uinfo

    uinfo = Uinfo(opts_users)
    uinfo.display_uinfo_data()
elif re.search('rchain', sys.argv[0]):
    from lib.Rchain import Rchain

    rchain = Rchain(opts_users)
    rchain.display_rchain_data()
elif re.search('orginfo', sys.argv[0]):
    from lib.OrgInfo import OrgInfo

    org = OrgInfo(opts_users)
    org.display_orginfo_data()
