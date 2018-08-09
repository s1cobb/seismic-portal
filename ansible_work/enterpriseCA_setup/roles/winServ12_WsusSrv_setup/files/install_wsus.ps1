#Install Windows Features
#
# Install-WindowsFeature -Name UpdateServices-Services,UpdateServices-DB -IncludeManagementTools
#

param( [string] $safe_passwd, [string] $safe_domain_nm )

try {
   Install-windowsfeature -Name UpdateServices, UpdateServices-WidDB, UpdateServices-Services, UpdateServices-RSAT, UpdateServices-API, UpdateServices-UI  -IncludeManagementTools
}
catch {
   Throw "Failed to install the WSUS  services"
}

#$wsus_path = "C:\WSUS"
#if( !(test-path $wsus_path) ) {
#     try {
#        New-Item -Path $wsus_path -ItemType Directory 
#     }
#     catch {
#        Throw "Failed to create the WSUS directory"
#     } 
#}
