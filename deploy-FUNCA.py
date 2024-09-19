import json
import requests

octopus_server_uri = 'http://20.221.73.234/api'
octopus_api_key = 'API-2EAQGLCO34TBDWNBGGG3EK6QALW9HT44'
headers = {'X-Octopus-ApiKey': octopus_api_key}
space_name = "Spaces-1"
project_name = "Projects-2"
environment_name = 'Environments-1'
channel_name = 'Default'
release_version = "Releases-304"

def get_octopus_resource(uri):
    response = requests.get(uri, headers=headers)
    response.raise_for_status()
    return json.loads(response.content.decode('utf-8'))


def get_by_name(uri, name):
    resources = get_octopus_resource(uri)
    return next((x for x in resources if x['Id'] == name), None)

space = get_by_name('{0}/spaces/all'.format(octopus_server_uri), space_name)
print(space)
print("=================================")
project = get_by_name('{0}/{1}/projects/all'.format(octopus_server_uri, space['Id']), project_name)
print(project)
print("=================================")
releases = get_octopus_resource('{0}/{1}/projects/{2}/releases'.format(octopus_server_uri, space['Id'], project['Id']))
print(releases)
print("=================================")
release = next((x for x in releases['Items'] if x['Id'] == release_version), None)
print(release)
print("=================================")
environment = get_by_name('{0}/{1}/environments/all'.format(octopus_server_uri, space['Id']), environment_name)
print(environment)

deployment = {
    'ReleaseId': release['Id'],
    'EnvironmentId': environment['Id']
}

print("=================================")
print(deployment)
uri = '{0}/{1}/deployments'.format(octopus_server_uri, space['Id'])
response = requests.post(uri, headers=headers, json=deployment)
response.raise_for_status()