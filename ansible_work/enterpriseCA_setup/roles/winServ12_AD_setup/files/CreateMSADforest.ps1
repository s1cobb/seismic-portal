# Version 1.0
# Install Windows Features

param( [string] $safe_passwd, [string] $domain_name, [string] $domain_netbios_name )

try {
   Install-windowsfeature AD-domain-services
   Import-Module ADDSDeployment
}
catch {
   Throw "Failed to add the AD domain services"
}

#This is for first server and forest to create and Domain
#values 2008R2 = 4, 2012 = 5
$pwd = ConvertTo-SecureString $safe_passwd -AsPlaintext -Force

try {
   Install-ADDSForest `
   -CreateDnsDelegation:$false `
   -DatabasePath "C:\Windows\NTDS" `
   -DomainMode 5 `
   -DomainName $domain_name `
   -DomainNetbiosName $domain_netbios_name `
   -ForestMode 5 `
   -SafeModeAdministratorPassword $pwd `
   -InstallDns:$true `
   -LogPath "C:\Windows\NTDS" `
   -NoRebootOnCompletion:$false `
   -SysvolPath "C:\Windows\SYSVOL" `
   -Force:$true
}
catch {
   Throw "Failed to create forest  $($_.Exception.Message)"
}

#Server will reboot after forest creation
