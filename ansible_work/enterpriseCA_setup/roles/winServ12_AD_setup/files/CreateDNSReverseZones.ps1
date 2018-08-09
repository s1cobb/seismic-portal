# Version 1.0
# Create DNS reverse lookup zone

#Extra Tools
try {
   Add-WindowsFeature -Name "ad-domain-services" -IncludeAllSubFeature -IncludeManagementTools
   
}
catch {
   Throw "Failed to install extra tools"

try {
   Add-DnsServerPrimaryZone -DynamicUpdate Secure -NetworkId "192.168.132.0//24" -ReplicationScope Domain
}
catch {
   Throw "Failed to create the DNS server primary zone"
}

