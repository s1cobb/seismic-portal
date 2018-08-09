# Version 1.0
# Install Windows adcs Enrollment Web Service Features

param( [string] $safe_passwd, [string] $safe_domain_nm, [string] $domain_name )
$ConfirmPreference="none"

function Setup_DomainProfile {
  [CmdletBinding(
    ConfirmImpact = 'Medium')
  ]
  param($param)

$domain_user = $domain_name + "\" + $safe_domain_nm
$SecurePassword = ConvertTo-SecureString $safe_passwd -AsPlaintext -Force
$uc = New-Object System.Management.Automation.PSCredential -ArgumentList $domain_user, $SecurePassword 
Start-Process -FilePath 'CMD.EXE' -ArgumentList '/C ECHO' -Credential $uc -LoadUserProfile

}

# Make sure we run as admin            
#$usercontext = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()            
#$IsAdmin = $usercontext.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")                               
#if (-not($IsAdmin))            
#{            
#   Throw "Must run powerShell as Administrator to perform these actions"     
#}

Setup_DomainProfile
