param( [string] $domain, [string] $gpo_name, [string] $unlinkit )

if ($gpo_name -eq "ADM - Domain Administrators Policy" -and $unlinkit -eq "yes") {
      Remove-GPLink -Name "ADM - Domain Administrators Policy" -Target "ou=Domain Administrators,dc=$domain,dc=cns"
}

if ( $gpo_name -eq "ADM - Google Chrome Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "ADM - Google Chrome Policy" -Target "ou=Domain Administrators,dc=$domain,dc=cns" 
}

if ($gpo_name -eq "ADM - IE11 Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "ADM - IE11 Policy" -Target "ou=Domain Administrators,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "ADM - Office 2016 Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "ADM - Office 2016 Policy" -Target "ou=Domain Administrators,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "ALL - Domain Custom Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "ALL - Domain Custom Policy" -Target "dc=$domain,dc=cns" 
}

if ($gpo_name -eq "DIS - Disabled Administrator Accounts" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "DIS - Disabled Administrator Accounts" -Target "ou=Disabled Administrator Accounts ADM,ou=Domain Administrators,dc=$domain,dc=cns" 
}

if ($gpo_name -eq "DIS - Disabled Domain Service Accounts" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "DIS - Disabled Domain Service Accounts" -Target "ou=Disabled Domain Service Accounts SAC,ou=Domain Service Accounts,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "DIS - Disabled Domain Service Accounts" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "DIS - Disabled Domain Service Accounts" -Target "ou=Disabled Domain Server Accounts SVR,ou=Domain Servers,dc=$domain,dc=cns"
}

if ( $gpo_name -eq "ipam_DC_NPS" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "ipam_DC_NPS" -Target "dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "ipam_DHCP" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "ipam_DHCP" -Target "dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "ipam_DNS" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "ipam_DNS" -Target "dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SAC - Domain Service Accounts Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SAC - Domain Service Accounts Policy" -Target "ou=Domain Service Accounts,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SAC - IE11 Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SAC - IE11 Policy" -Target "ou=Domain Service Accounts,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SAC - Office 2016 Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SAC - Office 2016 Policy" -Target "ou=Domain Service Accounts,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SAC - Splunk" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SAC - Splunk" -Target "ou=Splunk SAC,ou=Domain Service Accounts,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - AppLocker Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - AppLocker Policy" -Target "ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - Domain Server Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - Domain Server Policy" -Target "ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - Office 2016 Policy" -and $unlinkit -eq "yes") {
   #Remove-GPLink -Name "SVR - Office 2016 Policy" -Target "ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - Firewall Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - Firewall Policy" -Target "ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - Google Chrome Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - Google Chrome Policy" -Target "ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - IE11 Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - IE11 Policy" -Target "ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - Cisco Unified Communications Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - Cisco Unified Communications Policy" -Target "ou=Cisco Unified Communications SVR,ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - Federation Service Server Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - Federation Service Server Policy" -Target "ou=Federation Service SVR,ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - IP Address Management (IPAM) Server Policy" $unlinkit -eq "yes") {
   #Remove-GPLink -Name "SVR - IP Address Management (IPAM) Server Policy" -Target "ou=IPAM Servers SVR,ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - McAfee ePolicy Orchestrator Server Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - McAfee ePolicy Orchestrator Server Policy" -Target "ou=McAfee ePO SVR,ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - Remote Desktop Session Host Server Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - Remote Desktop Session Host Server Policy" -Target "ou=RD Session Host SVR,ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - SQL Database Server Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - SQL Database Server Policy" -Target "ou=SQL Database SVR,ou=Domain Servers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - Domain Controller (DC) Server Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - Domain Controller (DC) Server Policy" -Target "ou=Domain Controllers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - AppLocker Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - AppLocker Policy" -Target "ou=Domain Controllers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - Firewall Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - Firewall Policy" -Target "ou=Domain Controllers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - Google Chrome Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - Google Chrome Policy" -Target "ou=Domain Controllers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - IE11 Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - IE11 Policy" -Target "ou=Domain Controllers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "SVR - PDC NTP Time Source Common Services Network" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "SVR - PDC NTP Time Source Common Services Network" -Target "ou=Domain Controllers,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "USR - Domain User Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "USR - Domain User Policy" -Target "ou=Domain Users,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "USR - Google Chrome Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "USR - Google Chrome Policy" -Target "ou=Domain Users,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "USR - IE11 Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "USR - IE11 Policy" -Target "ou=Domain Users,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "USR - Office 2016 Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "USR - Office 2016 Policy" -Target "ou=Domain Users,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "WRK - AppLocker Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "WRK - AppLocker Policy" -Target "ou=Domain Workstations,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "WRK - Domain Workstation Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "WRK - Domain Workstation Policy" -Target "ou=Domain Workstations,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "WRK - Firewall Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "WRK - Firewall Policy" -Target "ou=Domain Workstations,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "WRK - Google Chrome Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "WRK - Google Chrome Policy" -Target "ou=Domain Workstations,dc=$domain,dc=cns" 
}

if ( $gpo_name -eq "WRK - IE11 Policy" -and $unlinkit -eq "yes") {
   Remove-GPLink -Name "WRK - IE11 Policy" -Target "ou=Domain Workstations,dc=$domain,dc=cns" 
}

