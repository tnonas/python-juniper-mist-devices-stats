#!/usr/bin/env python3

import requests, json
from getpass import getpass
import csv

# Get api_url, org ID, token or credentials
mist_clouds = dict({
    'Mist Global 01': {'position': '1', 'url': 'api.mist.com'},
    'Mist Global 02': {'position': '2', 'url': 'api.gc1.mist.com'},
    'Mist Global 03': {'position': '3', 'url': 'api.ac2.mist.com'},
    'Mist Global 04': {'position': '4', 'url': 'api.gc2.mist.com'},
    'Mist EMEA 01': {'position': '5', 'url': 'api.eu.mist.com'},
    'Mist EMEA 02': {'position': '6', 'url': 'api.gc3.mist.com'},
    'Mist EMEA 03': {'position': '7', 'url': 'api.ac6.mist.com'},
    'Mist APAC 01': {'position': '8', 'url': 'api.ac5.mist.com'}
})

api_choice = str('0')
api_url = str('')

while api_choice not in '12345678':
    api_choice = input('(1) Mist Global 01\n(2) Mist Global 02\n(3) Mist Global 03\n(4) Mist Global 04\n(5) Mist EMEA 01\n(6) Mist EMEA 02\n(7) Mist EMEA 03\n(8) Mist APAC 01\nProvide Mist Cloud number: ')
for k, v in mist_clouds.items():
    if v['position'] == api_choice:
        api_url = v['url']
        print(f'\n---> API target set to {k} ({api_url})\n')

auth_choice = str('')
while auth_choice not in ['T', 't', 'U', 'u']:
    auth_choice = str(input("Do you want to use (T)oken or (U)sername / Password for Mist API authentication? "))

if auth_choice in ['U', 'u']:
    username = str(input("\nProvide your Username: "))
    password = str(getpass("Provide your Password: "))
    org_id = str(input("Provide your Organization ID: "))

else:
    token = str(getpass("\nProvide your Token: "))
    org_id = str(input("Provide your Organization ID: "))


# Set request vars
r_url = f'https://{api_url}/api/v1/orgs/{org_id}/sites'
params = {}
r_payload = {}

sites_list = dict({}) # This is where org's list of sites and their names will reside

## Choose headers and request specific to authentication type
if auth_choice in ['U', 'u']:
    print('\n--> Using Username / Password authentication...')
    print('\n--> Getting a list of sites in the org...', end='')

    r_headers = { # use basic authorization
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    ## Generate request and get response
    response = requests.request('GET', r_url, headers=r_headers, params=params, data=json.dumps(r_payload), auth=(username, password))

else:
    print('\n--> Using Token authentication...')
    print('\n--> Getting a list of sites in the org...', end='')

    r_headers = { # use token authorization
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Token {token}'
    }

    ## Generate request and get response
    response = requests.request('GET', r_url, headers=r_headers, params=params, data=json.dumps(r_payload))

## Analyze initial response
if response.status_code != 200:
    print(f'\n|-> Request unsuccessful, status code: {response.status_code} ({response.reason}). Cannot read the list of sites. Please check your authentication and Org ID details.')
else:
    list_sites_output = json.loads(response.text) # Convert JSON string response to dict()
    for site in list_sites_output: # Build a list of sites in the org
        sites_list[site['name']] = site['id']


    # Get devices details in each site
    print(f'DONE')
    print(f'--> Getting information about devices in each site...')

    devices_data = [] # This is where all device data gather will reside

    for site_name, site_id in sites_list.items(): # Get each site from the list of sites and get devices stats

        print(f'|-> Analyzing {site_name}...', end='')

        ## Set request parameters. If not set here the initial parameters wil be used
        r_url = f'https://{api_url}/api/v1/sites/{site_id}/stats/devices'
        params = {'type': 'all', 'status': 'connected'}
        ## Generate request and get response based on authentication type
        if auth_choice in ['U', 'u']: # For basic authentication
            response = requests.request('GET', r_url, headers=r_headers, params=params, data=json.dumps(r_payload),
                                        auth=(username, password))
        else: # For token authentication
            response = requests.request('GET', r_url, headers=r_headers, params=params, data=json.dumps(r_payload))
        ## Analyze response
        if response.status_code != 200:
            print(
                f'\n|-> Request unsuccessful, status code: {response.status_code} ({response.reason}). Cannot read devices stats in site ID {site_id}!')
        else:
            devices_stats_output = json.loads(response.text) # Convert JSON string response to dict()
            for device in devices_stats_output:
                devices_data.append(
                    {
                        'Site name': site_name,
                        'Device type': device['type'],
                        'Device name': device['name'],
                        'Device version': device['version']
                    }
                )
            print('DONE')

    # Write results to CSV file
    fieldnames = ['Site name', 'Device name', 'Device type', 'Device version'] # Define which dict keys will be written to CSV

    with open('output/devices_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(devices_data)

    print(f'\nAnalysis of devices stats in all sites in org ID: {org_id} was SUCCESSFUL. The results are found in file: "./output/devices_data.csv"')