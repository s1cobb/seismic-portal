# Version 1.0
# Install Windows adcs Enrollment Web Service Features

param( [string] $thumb_print, [string] $safe_passwd, [string] $safe_domain_nm, [string] $domain_name, [string] $ca_config, [string] $sacusr, [string] $sacpw )
$ConfirmPreference="none"

function Setup_EnrollWebService {
  [CmdletBinding(
    ConfirmImpact = 'Medium')
  ]
  param($param)


  $sac_pw = ConvertTo-SecureString $sacpw -AsPlainText -Force
  $sac_usr =  $domain_name + "\" + $sacusr

  $username = $domain_name + "\" + $safe_domain_nm
  $secure_pw = ConvertTo-SecureString $safe_passwd -AsPlainText -Force
  $cred = New-Object System.Management.Automation.PSCredential -ArgumentList $username, $secure_pw

  try {
     Install-AdcsEnrollmentWebService `
     -Credential $cred `
     -ServiceAccountName $sac_usr `
     -ServiceAccountPassword $sac_pw `
     -CAConfig $ca_config `
     -AuthenticationType UserName `
     -SSLCertThumbprint $thumb_print `
     -Force:$true
  }
  catch {
      Throw "Failed to configure Enrollment Web Service -- $($_.Exception.Message)"
  }
}

try {
   Import-Module ServerManager
   Add-WindowsFeature ADcs-Enroll-Web-Svc 
}
catch {
   Throw "Failed to add the AD CS Web Service -- $($_.Exception.Message)"
}

Setup_EnrollWebService
