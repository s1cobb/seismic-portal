Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

# Version 1.0
# Main playbook to install AD domain server, AD certificate server
# and window boxes to the doamin.
#
# **** STEP 1 -  Verify group_vars/all file has all domain information correct before running
#                ansible-vault edit group_vars/all
#
# **** STEP 2 -  For now these playbooks need to be run for setup
#                ansible-playbook --tags 'ad,cert' setup_windows_domain.yml --ask-vault-pass
#                              then 
#                ansible-playbook --tags 'mems' setup_windows_domain.yml --ask-vault-pass
#                              depending on what servers you need to setup
#                ansible-playbook --tags 'mems,filsrv,sqlsrv,fedsrv,remsrv,wsusrv,ticsrv,oinsrv' setup_windows_domain.yml --ask-vault-pass
#
#                ansible-playbook --tags 'ad,cert,mems' setup_windows_additionalADDC.yml --ask-vault-pass
#                ansible-playbook setup_gpos.yml --ask-vault-pass
#
#
# **** STEP 4 - Two webservice features can only be loaded at the end.
#               ansible-playbook --tags 'cert' add_webservices.yml --ask-vault-pass
#


### setup the AD domain server
- include: add_domain_controller.yml

### setup the AD certificate server
- include: add_certificate_srv.yml

### add new members in this playbook
- include: add_member_to_domain.yml

### add reverse lookup info to domain controller
- include: add_resource_ptr.yml

### add add FILE server setup
- include: add_file_server.yml

### add SQL server setup
- include: add_sql_server.yml

### add WSUS server setup
- include: add_wsus_server.yml



License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
