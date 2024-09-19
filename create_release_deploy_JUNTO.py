# usage:
# python3 create_release_deploy_JUNTO.py <Build_Name> <Build_Version>      
# python3 create_release_deploy_JUNTO.py Monaco_WinnersWorldR25_270_FullBuild_Gdk35 2.7.0.10
# python3 create_release_deploy_JUNTO.py Monaco_HistoricalHorseRacing_261_FullBuild_Gdk20 2.6.1.516
# python3 create_release_deploy_JUNTO.py Monaco_HistoricalHorseRacing_261_FullBuild_Gdk30 2.6.1.16


import json, sys
import requests
from requests.api import get, head

######## UPDATE VARIABLES ##############
def get_octopus_resource(uri, headers, skip_count = 0):
    items = []
    response = requests.get((uri + "?skip=" + str(skip_count)), headers=headers)
    response.raise_for_status()
    # Get results of API call
    results = json.loads(response.content.decode('utf-8'))
    # Store results
    if 'Items' in results.keys():
        items += results['Items']
        # Check to see if there are more results
        if (len(results['Items']) > 0) and (len(results['Items']) == results['ItemsPerPage']):
            skip_count += results['ItemsPerPage']
            items += get_octopus_resource(uri, headers, skip_count)
    else:
        return results
    # return results
    return items

def up_var(a, b):
    # Define Octopus server variables
    octopus_server_uri = 'http://10.196.10.68/api'
    octopus_api_key = 'API-TJMD4RUEIXAS8PJ6WBBQREUFIX3YMM'
    headers = {'X-Octopus-ApiKey': octopus_api_key}
    project_name = "PC Submission"
    space_name = "Default"
    variable = {
        'Name': a,
        'Value': b,
    # 'Name': 'Build_Name',
    # 'Value': 'Monaco_WinnersWorldR25_270_FullBuild_Gdk35',
    # 'Value': 'RIVER',
        'Type': 'String',
        'IsSensitive': False
    }

    uri = '{0}/spaces'.format(octopus_server_uri)
    spaces = get_octopus_resource(uri, headers)
    # print(spaces)
    # print("+++++++++++++++++")
    space = next((x for x in spaces if x['Name'] == space_name), None)
    # print(space)

    uri = '{0}/{1}/projects'.format(octopus_server_uri, space['Id'])
    projects = get_octopus_resource(uri, headers)
    project = next((x for x in projects if x['Name'] == project_name), None)
    if project != None:
        uri = '{0}/{1}/variables/{2}'.format(octopus_server_uri, space['Id'], project['VariableSetId'])
        projectVariables = get_octopus_resource(uri, headers)
        print(projectVariables)
        print("+++++++++++++++++")
        projectVariable = next((x for x in projectVariables['Variables'] if x['Name'] == variable['Name']), None)
        print(projectVariable)
        projectVariable['Value'] = variable['Value']
        response = requests.put(uri, headers=headers, json=projectVariables)
        response.raise_for_status

name = sys.argv[1]
version = sys.argv[2]
up_var("Build_Name", name)
up_var("Build_Version", version)


#########   RELEASE #############
octopus_server_uri = 'http://10.196.80.68'
octopus_api_key = 'API-TJMD4RUEIXAS8PJ6WBBQREUFIX3YMM'
headers = {'X-Octopus-ApiKey': octopus_api_key}
space_name = "Spaces-1"
project_name = "Projects-2"
# environment_name = 'Development'
# channel_name = 'Default'
release_version = name  + '_' + version  # this needs to be unique
environment_name = 'Environments-1'

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


# ############ DEPLOY ###############

def get_octopus_resource(uri):
    response = requests.get(uri, headers=headers)
    response.raise_for_status()
    return json.loads(response.content.decode('utf-8'))


def get_by_name(uri, name):
    resources = get_octopus_resource(uri)
    return next((x for x in resources if x['Id'] == name), None)

space = get_by_name('{0}/api/spaces/all'.format(octopus_server_uri), space_name)
project = get_by_name('{0}/api/{1}/projects/all'.format(octopus_server_uri, space['Id']), project_name)
# releases = get_octopus_resource('{0}/{1}/projects/{2}/releases'.format(octopus_server_uri, space['Id'], project['Id']))
# release = next((x for x in releases['Items'] if x['Id'] == release_version), None)
environment = get_by_name('{0}/api/{1}/environments/all'.format(octopus_server_uri, space['Id']), environment_name)
deployment = {
    'ReleaseId': release['Id'],
    'EnvironmentId': environment['Id']
}
uri = '{0}/api/{1}/deployments'.format(octopus_server_uri, space['Id'])
response = requests.post(uri, headers=headers, json=deployment)
response.raise_for_status()
