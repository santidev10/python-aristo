import json, sys
import requests

octopus_server_uri = 'http://20.221.73.234/api'
octopus_api_key = 'API-2EAQGLCO34TBDWNBGGG3EK6QALW9HT44'
headers = {'X-Octopus-ApiKey': octopus_api_key}
project_name = "PC Submission"
space_name = "Default"
body = {
    'Instructions': None,
    'Notes': "Message",
    'Result': "Proceed"
}

interruptionId = "Interruptions-33"

# Take responsibility for the Intervention
# Invoke-RestMethod "$OctopusURL/api/$($space.Id)/interruptions/$InterruptionID/responsible" -Method Put -Headers $header
uri = '{0}/Spaces-1/interruptions/{1}/responsible'.format(octopus_server_uri, interruptionId)
print(uri)
response = requests.put(uri, headers=headers)
print(response)
response.raise_for_status

#Approve/abort the intervention
#Invoke-RestMethod "$OctopusURL/api/$($space.Id)/interruptions/$InterruptionID/submit" -Body $body -Method Post -Headers $header
uri = '{0}/Spaces-1/interruptions/{1}/submit'.format(octopus_server_uri, interruptionId)
response = requests.post(uri, headers=headers, json=body)
print(response)
response.raise_for_status

