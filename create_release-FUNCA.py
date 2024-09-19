# usage:
# python3 create_release.py <Build_Name> <Build_Version>      
# python3 create_release.py Monaco_WinnersWorldR25_270_FullBuild_Gdk35 2.7.0.10
# python3 create_release.py Monaco_HistoricalHorseRacing_261_FullBuild_Gdk20 2.6.1.516
# python3 create_release.py Monaco_HistoricalHorseRacing_261_FullBuild_Gdk30 2.6.1.16

import update_variables
import json, sys
import requests
from requests.api import get, head

name = sys.argv[1]
version = sys.argv[2]

update_variables.up_var("Build_Name", name)
update_variables.up_var("Build_Version", version)

octopus_server_uri = 'http://10.196.80.68'
octopus_api_key = 'API-2EAQGLCO34TBDWNBGGG3EK6QALW9HT44'
headers = {'X-Octopus-ApiKey': octopus_api_key}
space_name = "Spaces-1"
project_name = "Projects-2"
# environment_name = 'Development'
# channel_name = 'Default'
release_version = name  + '_' + version  # this needs to be unique

# Create release JSON
releaseJson = {
  #  'ChannelId': channel_name,
    'ProjectId': project_name,
    'Version': release_version,
    'SelectedPackages': []
}

# Create release
uri = '{0}/api/{1}/releases'.format(octopus_server_uri, space_name)
response = requests.post(uri, headers=headers, json=releaseJson)
# response = requests.get(uri, headers=headers, json=releaseJson)
response.raise_for_status()

# Get results of API call
release = json.loads(response.content.decode('utf-8'))
print(release)

# Falta DEPLOY !!!
