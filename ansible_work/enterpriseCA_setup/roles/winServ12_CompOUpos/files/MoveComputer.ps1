# Version 1.0
# Install Windows Features

param( [string] $comp_name, [string] $domain_name )


try {
   if ( $comp_name -match "FG") {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Federation Proxy SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "SF" -OR $comp_name -match "NI" -OR $comp_name -match "SH" -OR $comp_name -match "SK" -OR $comp_name -match "SN" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Splunk SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "NF" -OR $comp_name -match "NO" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=SolarWinds SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "US" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=WSUS SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "CA" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=CA SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "EP" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=McAfee ePO SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "AS" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Cisco ASA Firewall SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "FD" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Federation Service SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "FL" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=File SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "IP" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=IPAM Servers SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "RS" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=RD Session Host SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "ON" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Solarwinds Orion SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "TK" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Solarwinds Ticket SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "SQ" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Solarwinds SQL Database SVR,ou=SQL Database SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "TMSSQL" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=TMS SQL Database SVR,ou=SQL Database SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "TMS" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=TMS SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "ZN" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Zenoss SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "WD" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Thin Clients Normal WrkStn WRK,ou=Thin Clients WRK,ou=domain workstations,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "WK" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Thin Clients Normal WrkStn WRK,ou=Thin Clients WRK,ou=,ou=domain workstations,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "WX" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=Thin Clients Normal WrkStn WRK,ou=Thin Clients WRK,ou=domain workstations,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "ES" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=VMware ESXi SVR,ou=Non-Windows Server Accounts,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "ISE" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=ISE SVR,ou=Non-Windows Server Accounts,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "NCL" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=NetApp SVR,ou=Non-Windows Server Accounts,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "SC" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=vCenter SVR,ou=Non-Windows Server Accounts,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "CE" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=CA SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "CP" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=CA SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "CW" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=CA SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "CN" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=CA SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   elseif ( $comp_name -match "OR" ) {
      Get-ADComputer $comp_name | Move-ADObject -TargetPath "ou=CA SVR,ou=domain servers,dc=$domain_name,dc=cns"
   }
   
}
catch {
   Throw "Failed to move $comp_name to correct OU ---  $($_.Exception.Message)"
} 
