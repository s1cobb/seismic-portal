# Version 1.0
# Install Windows Features

param( [string] $safe_passwd,[string] $safe_domain_nm, [string] $domain_name, [string] $domain, [string] $site_name, [string] $replication_source )

try {
   Install-windowsfeature AD-domain-services -IncludeManagementTools
   Import-Module ADDSDeployment
}
catch {
   Throw "Failed to add the AD domain services"
}


#values 2008R2 = 4, 2012 = 5
$pwd = ConvertTo-SecureString $safe_passwd -AsPlaintext -Force
$username = $domain + "\" + $safe_domain_nm
$credential = New-Object -TypeName System.Management.Automation.PSCredential -Argumentlist $username, $pwd
$securePassword = ConvertTo-SecureString -String $safe_passwd -AsPlaintext -Force

$replicator_src_name = $replication_source + "." + $domain_name

try {
   Install-ADDSDomainController `
   -DomainName $domain_name `
   -SafeModeAdministratorPassword $securePassword `
   -NoGlobalCatalog:$false `
   -CreateDnsDelegation:$false `
   -CriticalReplicationOnly:$false `
   -Credential $credential `
   -DatabasePath 'C:\Windows\NTDS' `
   -SiteName $site_name `
   -LogPath 'C:\Windows\NTDS' `
   -SysvolPath 'C:\Windows\SYSVOL' `
   -ReplicationSourceDC $replicator_src_name `
   -NoRebootOnCompletion:$true `
   -Force:$true 
}
catch {
   Throw "Failed to create additional Domain Controller $replicator_src_name  $($_.Exception.Message)"
}

