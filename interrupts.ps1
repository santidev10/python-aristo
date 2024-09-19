$ErrorActionPreference = "Stop";

# Define working variables
$octopusURL = "http://10.196.80.68/api"
$octopusAPIKey = "API-TJMD4RUEIXAS8PJ6WBBQREUFIX3YMM"
$header = @{ "X-Octopus-ApiKey" = $octopusAPIKey }
$spaceName = "Default"


# Get space Id
$space = (Invoke-RestMethod -Method Get -Uri "$octopusURL/spaces/all" -Headers $header) | Where-Object {$_.Name -eq $spaceName}

# (Invoke-RestMethod -Method Get -Uri "$octopusURL/spaces/all" -Headers $header) | Where-Object {$_.Name -eq $spaceName}
# $interruptions = (Invoke-RestMethod -Method Get -Uri "$octopusURL/interruptions" -Headers $header) | Where-Object {$_.IsPending -eq $false}
$interruptions = (Invoke-RestMethod -Method Get -Uri "$octopusURL/interruptions" -Headers $header) 

write-host $interruptions
