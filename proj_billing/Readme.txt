get_billing.py
   Description:
        This script will retrieve the License/Device usage from the
        Call Manager and the Conference configuration from the Cisco
        Meeting Server.

        A web request is sent to each device and a XML response is
        returned, which is parsed before sending to log files and
        database.

        There are two log files used for logging. These files will be
        rotated on a continuous basis up to 10 files, then they will
        start to be overridden.
           logs/error.log   -- errors for splunk use
           logs/data.log -- data from devices

        We are using Mariadb with database named 'billing' for testing.
        Two tables are used to store the AXL data:
            device_data table - holds license information
            conference_data table - holds conference information

        We will execute this script from cron.
        get_billing.py --devusage --confspace

