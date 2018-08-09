# Version 1.0
# Install Windows Features

param( [string] $safe_passwd, [string] $safe_domain_nm, [string] $domain, [string] $web_role_user, [string] $web_role_password )

$ConfirmPreference="none"

function Setup_NetworkDeviceEnrollSrv {
  [CmdletBinding(
    ConfirmImpact = 'Medium')
  ]
  param($param)

$serv_account_name = $domain + "\" + $web_role_user
$pwd = ConvertTo-SecureString $safe_passwd -AsPlaintext -Force
$sac_pw = ConvertTo-SecureString $web_role_password -AsPlaintext -Force

$username = $domain + "\" + $safe_domain_nm
$credential = New-Object -TypeName System.Management.Automation.PSCredential -Argumentlist $username, $pwd

  try {
     Install-AdcsNetworkDeviceEnrollmentService `
     -ServiceAccountName $serv_account_name `
     -ServiceAccountPassword $sac_pw `
     -Credential $credential `
     -Force:$true
  }
  catch {
      Throw "Failed to install Certificate Network Device Service $($_.Exception.Message)"
  }
}

try {
   Import-Module ServerManager
}
catch {
   Throw "Failed import of service manager $($_.Exception.Message)"
}

try {
    Add-WindowsFeature Adcs-Device-Enrollment
}
catch {
    Throw "Failed to add AD Network Device Enrollment --  $($_.Exception.Message)"
}

Setup_NetworkDeviceEnrollSrv

