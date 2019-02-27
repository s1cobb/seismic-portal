
Description:
       This script uses ansible, perl and python scripts
       for a basic configuration of the Call Manager. The
       configuration is broken down into two parts. 

       The CUCM_cli_setup role uses ansible task/main.yml file
       to call the file/enable_fips.pl and file/cucm_cli_setup.pl 
       for command line configuration.

       The CUCM_axl_setup role uses ansible task/main.yml
       to call the file/cucm_axl_setup.py file for web AXL 
       Api request configuration. 

       Two log files are created during the configuration.
       axlconfig.log - holds the AXL responses from each of
                       the Axl web requests.
       cliconfig.log - holds the command line interface dialogue.


       Errors:
         Any errors will be collected and printed out at the
         end of the run for now. An array of errors will print
         the path to the AXL request file that failed or the
         CLI fail message.

Setup:
      Before running this playbook the group_vars/all file
      needs to be populated with the correct parameters
      that are required.

      These are the variable that will need changing:

      # user and password for Expect CLI commands
        cucm_login: 'administrator@10.207.200.82'
        cucm_pass: 'fsp-WWcs!1'

      # user and password for AXL Api commands
        cucm_axl_usr: 'administrator'
        cucm_axl_pw: 'fsp-WWcs!1'
        cucm_axl_ip: '10.207.200.82'

      # working directory path
        working_dir_path: '/root/cns-ssa/ansible/cucmv2'


Example:
     In the working directory run:
     >ansible-playbook cucm_setup.py

