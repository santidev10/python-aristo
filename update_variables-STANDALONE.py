# This script works alone just to update the variables per usage below:
# usage:
# python3 update_variables.py Build_Name <build-name>               For example:
# python3 update_variables.py Build_Name Monaco_WinnersWorldR25_270_FullBuild_Gdk35
# python3 update_variables.py Build_Version <build-version>         For example:
# python3 update_variables.py Build_Version 2.7.0.10
#

import json, sys
import requests
from requests.api import head

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

# Define Octopus server variables
octopus_server_uri = 'http://20.221.73.234/api'
octopus_api_key = 'API-2EAQGLCO34TBDWNBGGG3EK6QALW9HT44'
headers = {'X-Octopus-ApiKey': octopus_api_key}
project_name = "PC Submission"
space_name = "Default"
variable = {
    'Name': sys.argv[1],
    'Value': sys.argv[2],
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
