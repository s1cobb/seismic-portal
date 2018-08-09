# Version 1.0
# Install Windows Web Enrollment Features

param( [string] $safe_passwd, [string] $safe_domain_nm, [string] $domain_name )

$ConfirmPreference="none"

function Setup_WebEnrollment {
  [CmdletBinding(
    ConfirmImpact = 'Medium')
  ]
  param($param)

  $username = $domain_name + "\" + $safe_domain_nm
  $secure_pw = $safe_passwd | ConvertTo-SecureString -AsPlainText -Force
  $cred = New-Object System.Management.Automation.PSCredential -ArgumentList $username, $secure_pw 

  try {
     Install-AdcsWebEnrollment `
     -Credential $cred `
     -Force:$true
  }
  catch {
      Throw "Failed to install Enrollment Web Service $($_.Exception.Message)"
  }
}


try {
   Import-Module ServerManager 
   Add-WindowsFeature Adcs-Web-Enrollment -IncludeManagementTools
}
catch {
   Throw "Failed to add feature Adcs-Web-Enrollment"
}


Setup_WebEnrollment
