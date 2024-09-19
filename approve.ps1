$ErrorActionPreference = "Stop";

# Define working variables
$octopusURL = "http://20.221.73.234/api"
$octopusAPIKey = "API-2EAQGLCO34TBDWNBGGG3EK6QALW9HT44"
$header = @{ "X-Octopus-ApiKey" = $octopusAPIKey }
$spaceName = "Default"

# Get space Id
$space = (Invoke-RestMethod -Method Get -Uri "$octopusURL/spaces/all" -Headers $header) | Where-Object {$_.Name -eq $spaceName}

# e.g. "Interruptions-204".
# You can get this ID from the deployment document like this -> /api/interruptions?regarding=[Deployment ID]
$InterruptionID = "Interruptions-28"

$header = @{ "X-Octopus-ApiKey" = $OctopusAPIKey }

$body = @{Instructions= $null
            Notes = "Proceed from PS script"
            # Set this property to "Abort" to abort the deployment.
            # Omit the property completely for a failure guidance interruption.
            Result = "Proceed"
            # If you wish to Exclude the machine from the deployment (in case of a rolling deploy), uncomment the line below.
            # Guidance = "Exclude"
        } | ConvertTo-Json

# Take responsibility for the Intervention
Invoke-RestMethod "$OctopusURL/$($space.Id)/interruptions/$InterruptionID/responsible" -Method Put -Headers $header

#Approve/abort the intervention
Invoke-RestMethod "$OctopusURL/$($space.Id)/interruptions/$InterruptionID/submit" -Body $body -Method Post -Headers $header

