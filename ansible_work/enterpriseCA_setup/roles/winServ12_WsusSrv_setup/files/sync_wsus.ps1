#Get WSUS Server Object
$wsus = Get-WSUSServer

#Connect to WSUS server configuration
$wsusConfig = $wsus.GetConfiguration()

#Set to download updates from Microsoft Updates
Set-WsusServerSynchronization –SyncFromMU

#Set Update Languages to English and save configuration settings
$wsusConfig.AllUpdateLanguagesEnabled = $false
$wsusConfig.SetEnabledUpdateLanguages("en")
$wsusConfig.Save()

#Get WSUS Subscription and perform initial synchronization to get latest categories
$subscription = $wsus.GetSubscription()
$subscription.StartSynchronizationForCategoryOnly()

While ($subscription.GetSynchronizationStatus() -ne 'NotProcessing') {
   Start-Sleep -Seconds 5
}

