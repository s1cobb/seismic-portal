#Configure the Platforms that we want WSUS to receive updates
Get-WsusProduct | where-Object {
    $_.Product.Title -in (
    'CAPICOM',
    'Silverlight',
    'SQL Server 2012 R2',
    'Exchange Server 2010',
    'Windows Server 2012 R2')
} | Set-WsusProduct

#Configure the Classifications
Get-WsusClassification | Where-Object {
    $_.Classification.Title -in (
    'Update Rollups',
    'Security Updates',
    'Critical Updates',
    'Service Packs',
    'Updates')
} | Set-WsusClassification

#Configure Synchronizations
$subscription.SynchronizeAutomatically=$true

#Set synchronization scheduled for midnight each night
$subscription.SynchronizeAutomaticallyTimeOfDay= (New-TimeSpan -Hours 0)
$subscription.NumberOfSynchronizationsPerDay=1
$subscription.Save()

#Kick off a synchronization
$subscription.StartSynchronization()
