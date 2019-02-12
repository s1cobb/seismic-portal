Billing capture process:

   Description:
        This script will retrieve the License/Device usage from the
        Call Manager and the Conference configuration from the Cisco
        Meeting Server.

        A web request is sent to each device and a XML response is
        returned, which is parsed before sending to log files. 
        
        There are two log files used for logging. These files will be
        rotated on a continuous basis up to 10 files, then they will
        start to be overridden.
           logs/error.log   -- errors captured 
           logs/data.log    -- data for devices and conference spaces 

        Script will be executed from cron.
           get_billing.py --devusage --confspace

 

   Setup required:
        billing_config.csv - setup Call Manager and Meeting Server
                             information into the comma seperated 
                             file that you want to monitor.

        Fields of billing_config.csv:
        contract -  customer contract number
        target   -  is it CUCM or CMS
        axlusr   - user with AXL Web Api access
        axlpwd   - user password
        ip_address - CUCM/CMS ip address
        local_or_rmote - ip address local or remote
        serv_cnt - each time you add a new CUCM or CMS for monitoring
                   increment the count.

        Example of billing_config.csv:
              contract,target,local_or_remote,ip_address,axlusr,axlpwd,serv_cnt
              22222222,CUCM,local,127.0.0.1,StcobbAXL,fsp-WWcs!1,CUCM1
              33333333,CUCM,remote,127.0.0.1,StcobbAXL,fsp-WWcs!1,CUCM2
              77777777,CMS,local,127.0.0.1,StcobbAXL,fsp-WWcs!1,CMS1
              88888888,CMS,local,127.0.0.1,StcobbAXL,fsp-WWcs!1,CMS2
 

   Process Flow:

     -----------------|    call axl_data_request         ------------------
     | get_billing.py | -------------------------------> | misc_util.py   |
     |                |    AXL Xml Response              | logger setup   |<--/ call log_message
     |                | <------------------------------- | http request   |  /
     |                |                                  ------------------ /
     |                |                                                    / 
     |                |    call ProcessXML               ------------------                     --------------------- 
     |                | -------------------------------> | BillingUtil.py | call LicXMLHandler  |   XMLHandlers.py  |
     |                |                                  |                | ------------------> |   LicXMLHandler   |
     |                |                                  |  process_xml   |                     |   ConfXMLHandler  |
     |                |                                  |                | call ConfXMLHandler |                   |
     |                |    ---------------------         |                | ------------------> |                   |
     |                |--->|        load       |         |                |                     |                   |
     |                |    |billing_config.csv |         |  _log_all_data | parsed XML returned |                   |
     |                |    |                   |         |                | <-------------------|                   |
     |----------------|    |--------------------         |----------------|                     |-------------------|
