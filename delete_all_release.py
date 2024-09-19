# deletes all releases. Usage:
# python3 delete_all_release.py 

import json
import requests
from requests.api import get, head

octopus_server_uri = 'http://10.196.80.68'
octopus_api_key = 'API-2EAQGLCO34TBDWNBGGG3EK6QALW9HT44'
headers = {'X-Octopus-ApiKey': octopus_api_key}
space_name = "Spaces-1"
project_name = "Projects-2"
environment_name = 'Development'
channel_name = 'Default'

for i in range(500):
    release_version = 'Releases-' + str(i)
    # print(release_version)
    uri = '{0}/api/{1}/releases/{2}'.format(octopus_server_uri, space_name, release_version)
    response = requests.delete(uri, headers=headers)
   # print(response.text)

