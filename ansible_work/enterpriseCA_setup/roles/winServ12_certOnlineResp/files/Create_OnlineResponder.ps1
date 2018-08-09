# Version 1.0
# Install Windows Features

param( [string] $safe_passwd, [string] $safe_domain_nm, [string] $domain_name )

$ConfirmPreference="none"

function Setup_OnlineResponder {
  [CmdletBinding(
    ConfirmImpact = 'Medium')
  ]
  param($param)

$pwd = ConvertTo-SecureString $safe_passwd -AsPlaintext -Force
$username = $domain_name + "\" + $safe_domain_nm
$credential = New-Object -TypeName System.Management.Automation.PSCredential -Argumentlist $username, $pwd


  try {
     Install-AdcsOnlineResponder `
     -Credential $credential `
     -Force:$true
  }
  catch {
      Throw "Failed to install Certificate Online Responder $($_.Exception.Message)"
  }
}

try {
   Import-Module ServerManager
}
catch {
   Throw "Failed import of service manager $($_.Exception.Message)"
}

try {
    Add-WindowsFeature Adcs-Online-Cert 
}
catch {
    Throw "Failed to add AD Online Responder --  $($_.Exception.Message)"
}

Setup_OnlineResponder

