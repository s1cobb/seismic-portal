import logging
import urllib2
from logging.handlers import RotatingFileHandler

#setup logging, will log billing data to file and rotate files
logit = logging.getLogger('my_logger')
logit.setLevel(logging.DEBUG)
logfor = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fh = RotatingFileHandler('/root/billing/logs/data.log', maxBytes=100000, backupCount=10)
fh.setFormatter(logfor)
logit.addHandler(fh)

# setup logging, will log errors only/rotate files for splunk auditing
logspk = logging.getLogger('spk_error_logger')
logspk.setLevel(logging.DEBUG)
spklogfor = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fh2 = RotatingFileHandler('/root/billing/logs/error.log', maxBytes=100000, backupCount=10)
fh2.setFormatter(spklogfor)
logspk.addHandler(fh2)

############################################################################
def axl_data_request(url=None, add_header=None, data=None, usr=None, pw=None):
    # create a password manager
    #password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    #password_mgr.add_password(None, url, usr, pw)

    #handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    #opener = urllib2.build_opener(handler)

    # use the opener to fetch a URL
    #opener.open(url)

    # Install the opener, Now all calls to urllib2.urlopen use our opener.
    #urllib2.install_opener(opener)

    #req = urllib2.Request(url, data, add_header)
    req = urllib2.Request(url)

    response = urllib2.urlopen(req)
    xml_rsp = response.read()

    str1 = xml_rsp.rstrip('"\n')
    str2 = str1.lstrip('"')
    str3 = str2.replace('\\','')

    return str3


def log_message( logger, serv_info, log_msg, err_type, error=None ):
    if err_type == 'sys_error':
       logger.error("%s:%s:%s:%s:%s - ERROR %s: %s" \
                     % (serv_info['contract'], serv_info['month'], serv_info['target'],
                        serv_info['local_or_remote'], serv_info['ip_address'],
                        log_msg, str(error.reason)))
    elif err_type == 'error':
       logger.error("%s:%s:%s:%s:%s - ERROR %s " \
                     % (serv_info['contract'], serv_info['month'],
                        serv_info['target'], serv_info['local_or_remote'],
                        serv_info['ip_address'], log_msg))
    elif err_type == 'info':
       logger.info('%s:%s:%s:%s:%s - %s' \
                    % (serv_info['contract'], serv_info['month'], serv_info['target'],
                       serv_info['local_or_remote'], serv_info['ip_address'], log_msg))
    return None
