#Install Windows Features

param( [string] $safe_passwd, [string] $safe_domain_nm )

try {
   Install-windowsfeature File-Services -IncludeManagementTools
}
catch {
   Throw "Failed to add the File Server services"
}


try {
   Install-windowsfeature FS-DFS-Namespace -IncludeManagementTools
}
catch {
   Throw "Failed to add the DFS-Namespace services"
}


try {
   Install-windowsfeature FS-DFS-Replication -IncludeManagementTools
}
catch {
   Throw "Failed to add the DFS Replication services"
}


try {
   Install-windowsfeature FS-NFS-Service -IncludeManagementTools
}
catch {
   Throw "Failed to add the File NFS  services"
}


try {
   Install-windowsfeature FS-Resource-Manager, RSAT-FSRM-Mgmt -IncludeManagementTools
}
catch {
   Throw "Failed to add the File Server Resource Manager services"
}

$app_path = "C:\FileShare"
if( !(test-path $app_path) ) {
     try {
        New-Item -Path $app_path -ItemType Container
     }
     catch {
        Throw "Failed to create the fileshare directory"
     } 
  }

try {
     New-SmbShare -Name Groupdata -Path C:\FileShare -FolderEnumerationMode AccessBased -CachingMode Documents -EncryptData $True -FullAccess Everyone 
}
catch {
  Throw "Failed to create a new SmbShare named GroupData"
}
