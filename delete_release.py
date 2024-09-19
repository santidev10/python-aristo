# deletes all releases. Usage:
# python3 delete_all_release.py 

import json, sys
import requests
from requests.api import get, head

release_name = sys.argv[1]

octopus_server_uri = 'http://20.221.73.234'
octopus_api_key = 'API-2EAQGLCO34TBDWNBGGG3EK6QALW9HT44'
headers = {'X-Octopus-ApiKey': octopus_api_key}
space_name = "Spaces-1"
project_name = "Projects-2"
environment_name = 'Development'
channel_name = 'Default'


print(release_name)
uri = '{0}/api/{1}/releases/{2}'.format(octopus_server_uri, space_name, release_name)
response = requests.delete(uri, headers=headers)
print(response)
# release = json.loads(response.content.decode('utf-8'))
# print(release)

