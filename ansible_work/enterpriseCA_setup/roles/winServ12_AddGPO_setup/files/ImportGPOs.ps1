param( [string] $domain )

Import-GPO -BackupGpoName "ADM - Domain Administrators Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "ADM - Domain Administrators Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "ADM - Google Chrome Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "ADM - Google Chrome Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "ADM - IE11 Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "ADM - IE11 Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "ADM - Office 2016 Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "ADM - Office 2016 Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "ALL - Domain Custom Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "ALL - Domain Custom Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SAC - Domain Service Account Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SAC - Domain Service Accounts Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SAC - IE11 Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SAC - IE11 Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SAC - Office 2016 Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SAC - Office 2016 Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SAC - Google Chrome Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SAC - Google Chrome Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - AppLocker Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - AppLocker Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - CA Server Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - CA Server Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - Domain Server Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Domain Server Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
#Import-GPO -BackupGpoName "SVR - Office 2016 Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Office 2016 Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - Firewall Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Firewall Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - Firefox Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Firefox Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - Google Chrome Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Google Chrome Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - IE11 Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - IE11 Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
#Import-GPO -BackupGpoName "SVR - Federation Services Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Federation Services Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
#Import-GPO -BackupGpoName "SVR - Remote Desktop Session Host Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Remote Desktop Session Host Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - SQL Server Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - SQL Server Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - Domain Controller (DC) Server Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Domain Controller (DC) Server Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
#Import-GPO -BackupGpoName "SVR - PDC NTP Time Source Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - PDC NTP Time Source Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
#Import-GPO -BackupGpoName "SVR - Solarwinds Onion Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Solarwinds Onion Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
#Import-GPO -BackupGpoName "SVR - Solarwinds SQL Server Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Solarwinds SQL Server Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
#Import-GPO -BackupGpoName "SVR - Solarwinds Web Help Desk Server Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Solarwinds Web Help Desk Server Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - Splunk Server Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - Splunk Server Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "SVR - WSUS Server Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "SVR - WSUS Server Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
#Import-GPO -BackupGpoName "USR - Domain User Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "USR - Domain User Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "USR - Google Chrome Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "USR - Google Chrome Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "USR - IE11 Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "USR - IE11 Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "USR - Office 2016 Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "USR - Office 2016 Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "WRK - AppLocker Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "WRK - AppLocker Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "WRK - Domain Workstation Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "WRK - Domain Workstation Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "WRK - Firewall Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "WRK - Firewall Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
#Import-GPO -BackupGpoName "WRK - Firefox Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "WRK - Firefox Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "WRK - Google Chrome Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "WRK - Google Chrome Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "WRK - IE11 Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "WRK - IE11 Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
Import-GPO -BackupGpoName "WRK - Office 2016 Policy" -Path 'C:\ITIS\BCP_GPO_STIG_CIS_05-29-2018\GPO Backup' -TargetName "WRK - Office 2016 Policy" -MigrationTable C:\ITIS\mig.migtable -CreateIfNeeded
