# Version 1.0
#Install Windows Features

param( [string] $safe_passwd, [string] $safe_domain_nm, [string] $domain, [string] $domain_name )

#This is for first server and forest to create and Domain
#values 2008R2 = 4, 2012 = 5

$pwd = ConvertTo-SecureString $safe_passwd -AsPlaintext -Force
$username =  $domain + "\" + $safe_domain_nm
$credential = New-Object -TypeName System.Management.Automation.PSCredential -Argumentlist $username, $pwd

try {
   Add-Computer `
   -Credential $credential `
   -DomainName $domain_name  `
   -Force:$true
}
catch {
   Throw "Failed to add computer to domain  $($_.Exception.Message)"
}
