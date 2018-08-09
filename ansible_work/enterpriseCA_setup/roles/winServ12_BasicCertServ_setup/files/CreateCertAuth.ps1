# Version 1.0
# Install Windows Features

param( [string] $safe_passwd, [string] $safe_domain_nm, [string] $domain_name, [string] $common_name, [string] $dist_name_suffix )

$ConfirmPreference="none"

function Setup_CertServer {
  [CmdletBinding(
    ConfirmImpact = 'Medium')
  ]
  param($param)

  $pwd = ConvertTo-SecureString $safe_passwd -AsPlaintext -Force
  $username =  $domain_name + "\" + $safe_domain_nm
  $credential = New-Object -TypeName System.Management.Automation.PSCredential -Argumentlist $username, $pwd

  # StandaloneRootCa
  try {
     Install-AdcsCertificationAuthority `
     -CAType EnterpriseRootCA `
     -KeyLength 2048 `
     -HashAlgorithmName "SHA256" `
     -ValidityPeriod "Years" `
     -ValidityPeriodUnits 3  `
     -Credential $credential `
     -CACommonName $common_name `
     -CADistinguishedNameSuffix $dist_name_suffix `
     -CryptoProviderName "RSA#Microsoft Software Key Storage Provider" `
     -DatabaseDirectory "c:\CertDB" `
     -LogDirectory "c:\CertLog" `
     -Force:$true
  }
  catch {
      Throw "Failed to create Certificate Authority $($_.Exception.Message)"
  }
}

try {
   Import-Module ServerManager 
}
catch {
   Throw "Failed import of service manager $($_.Exception.Message)"
}

try {
    Add-WindowsFeature Adcs-Cert-Authority -IncludeManagementTools
}
catch {
    Throw "Failed to add Adcs-Cert-Authority $($_.Exception.Message)"
}

Setup_CertServer
