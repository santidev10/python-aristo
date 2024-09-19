import json
import requests

octopus_server_uri = 'http://10.196.80.68/api'
octopus_api_key = 'API-TJMD4RUEIXAS8PJ6WBBQREUFIX3YMM'
headers = {'X-Octopus-ApiKey': octopus_api_key}
space_name = "Spaces-1"
project_name = "Projects-22"
environment_name = 'Environments-41'
channel_name = 'Default'
release_version = "Releases-304"

def get_octopus_resource(uri):
    response = requests.get(uri, headers=headers)
    response.raise_for_status()
    return json.loads(response.content.decode('utf-8'))


def get_by_name(uri, name):
    resources = get_octopus_resource(uri)
    return next((x for x in resources if x['Id'] == name), None)

def get_all(uri):
    resources = get_octopus_resource(uri)
    # return next((x for x in resources), None)
    return resources

space = get_by_name('{0}/spaces/all'.format(octopus_server_uri), space_name)
print(space)
# space = get_all('{0}/spaces/all'.format(octopus_server_uri))
print(space['Name'])
print("================projects=================")
# project = get_by_name('{0}/{1}/projects/all'.format(octopus_server_uri, space['Id']), project_name)
project = get_all('{0}/{1}/projects/all'.format(octopus_server_uri, space['Id']))
for pro in project:
    print(pro)
# print(project[2]['Name'])
# print("=================================")
# releases = get_octopus_resource('{0}/{1}/projects/{2}/releases'.format(octopus_server_uri, space['Id'], project['Id']))
# print(releases)
# print("=================================")
# release = next((x for x in releases['Items'] if x['Id'] == release_version), None)
# print(release)
print("===============environment==================")
# environment = get_by_name('{0}/{1}/environments/all'.format(octopus_server_uri, space['Id']), environment_name)
environment = get_all('{0}/{1}/environments/all'.format(octopus_server_uri, space['Id']))
for env in environment:
    # print(env['Name'], env['Id'])
    print(env)

# deployment = {
#     'ReleaseId': release['Id'],
#     'EnvironmentId': environment['Id']
# }

# print("=================================")
# print(deployment)
# uri = '{0}/{1}/deployments'.format(octopus_server_uri, space['Id'])
# response = requests.post(uri, headers=headers, json=deployment)
# response.raise_for_status()

############# GET MACHINES ###################
print("========= MACHINES ========================")
machines = get_all('{0}/{1}/machines'.format(octopus_server_uri, space['Id']))
print(type(machines))
# print(machines)
machine = machines['Items']
print(machine)
# for machine in machines:
#     print(machine)

################ CHANNELS #################
print("========= CHANNELS  ========================")
channels = get_all('{0}/{1}/channels/all'.format(octopus_server_uri, space['Id']))
print(type(channels))
# print(channels)
for channel in channels:
    print(channel)


# 'Id': 'Projects-2'    'SpaceId': 'Spaces-1'   'Name': 'PC Submission'   'LifecycleId': 'Lifecycles-1'
# 'Id': 'Projects-22'   'SpaceId': 'Spaces-1'   'Name': 'ALC'             'LifecycleId': 'Lifecycles-3'
# 'Id': 'Projects-24'   'SpaceId': 'Spaces-1'   'Name': 'HHR'             'LifecycleId': 'Lifecycles-4'
# 'Id': 'Projects-27'   'SpaceId': 'Spaces-1'   'Name': 'WW'              'LifecycleId': 'Lifecycles-5'

# 'Id': 'Environments-1', 'SpaceId': 'Spaces-1', 'Slug': 'development', 'Name': 'Development'
# 'Id': 'Environments-41', 'SpaceId': 'Spaces-1', 'Slug': 'alc', 'Name': 'ALC'
# 'Id': 'Environments-42', 'SpaceId': 'Spaces-1', 'Slug': 'hhr', 'Name': 'HHR'
# 'Id': 'Environments-43', 'SpaceId': 'Spaces-1', 'Slug': 'ww', 'Name': 'WW'