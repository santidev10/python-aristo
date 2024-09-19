# final script for resuming the manual step after tech-admin uploads the xml file to flask-app/static/files

import json, sys
from textwrap import indent
import requests, subprocess

octopus_server_uri = 'http://10.196.80.68/api'
octopus_api_key = 'API-TJMD4RUEIXAS8PJ6WBBQREUFIX3YMM'
headers = {'X-Octopus-ApiKey': octopus_api_key}
project_name = "PC Submission"
space_name = "Default"
body = {
    'Instructions': None,
    'Notes': "Message",
    'Result': "Proceed"
}

# Get deploymentId
proc = subprocess.Popen('cat /mnt/octo-file-share/octo-deployment-id.txt', stdout=subprocess.PIPE, shell=True, text=True)
out, err = proc.communicate()
deploymentId = out.strip()
print(type(deploymentId))
print(deploymentId)
print("===========================")
# Get interruptionId
uri = '{0}/Spaces-1/interruptions?regarding={1}'.format(octopus_server_uri, deploymentId)
print(uri)
response = requests.get(uri, headers=headers)
dict = json.loads(response.text)
print(dict)
interruptionId = dict['Items'][0]['Id']
print(interruptionId)
print("===========================")
# Take responsibility for the Intervention
# Invoke-RestMethod "$OctopusURL/api/$($space.Id)/interruptions/$InterruptionID/responsible" -Method Put -Headers $header
uri = '{0}/Spaces-1/interruptions/{1}/responsible'.format(octopus_server_uri, interruptionId)
print(uri)
response = requests.put(uri, headers=headers)
print(response)
response.raise_for_status
print("===========================")
#Approve/abort the intervention
#Invoke-RestMethod "$OctopusURL/api/$($space.Id)/interruptions/$InterruptionID/submit" -Body $body -Method Post -Headers $header
uri = '{0}/Spaces-1/interruptions/{1}/submit'.format(octopus_server_uri, interruptionId)
print(uri)
response = requests.post(uri, headers=headers, json=body)
print(response)
response.raise_for_status

