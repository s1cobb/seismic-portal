# Version 1.0
# Install Windows adcs Enrollment Policy Web Service Features

param( [string] $thumbprint, [string] $safe_passwd, [string] $safe_domain_nm, [string] $domain )

$ConfirmPreference="none"

function Setup_PolicyWebService {
  [CmdletBinding(
    ConfirmImpact = 'Medium')
  ]
  param($param)

  $username = $domain + "\" + $safe_domain_nm
  $secure_pw = $safe_passwd | ConvertTo-SecureString -AsPlainText -Force
  $cred = New-Object System.Management.Automation.PSCredential -ArgumentList $username, $secure_pw

  try {
     Install-AdcsEnrollmentPolicyWebService `
     -Credential $cred `
     -AuthenticationType UserName `
     -SSLCertThumbprint $thumbprint `
     -Force:$true 
  }
  catch {
      Throw "Failed to install WebPolicyService -- $($_.Exception.Message)"
  }
}

try {
   Import-Module ServerManager
   Add-WindowsFeature Adcs-Enroll-Web-Pol 
}
catch {
   Throw "Failed to add the AD CS Policy Web Service"
}

Setup_PolicyWebService 
