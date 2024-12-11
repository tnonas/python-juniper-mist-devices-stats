#!/usr/bin/env python3

from juniper_mist_auth import get_api_url, get_auth_data, get_user_pass, get_token
import requests, json, csv

# ------------------------------------------------
# Generate Mist Clouds menu used to choose API url
# ------------------------------------------------
api_url: str = get_api_url()

# ---------------------------------------------------
# Choose Mist authentication type and get credentials
# ---------------------------------------------------
auth_choice: str = 'z'  # Define initial choice for authentication option outside available choices

while auth_choice not in 'TtUu':  # Display Authentication menu until the correct character is selected
    # noinspection SpellCheckingInspection
    auth_choice = str(input("Do you want to use (T)oken or (U)sername / Password for Mist API authentication? "))

if auth_choice in 'Uu':  # Get username / pass credentials and Org ID
    username, password = get_user_pass()

else:  # Get token and Org ID
    token: str = str(get_token())

# -------------------
# Get Organization ID
# -------------------
org_id: str = str(input("Provide your Organization ID: "))

# -----------------------
# Set API request details
# -----------------------
## Common API request parameters
r_url: str = f'https://{api_url}/api/v1/orgs/{org_id}/sites'
params: dict = {}
r_payload: dict = {}

## Define API request parameters (headers and request) specific to authentication type
if auth_choice in ['U', 'u']:
    print('\n--> Using Username / Password authentication...')
    print('\n--> Getting a list of sites in the org...', end='')

    r_headers: dict = {  # Use basic authorization, hence no authentication info in the header
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response: object = requests.request('GET', r_url, headers=r_headers, params=params, data=json.dumps(r_payload),
                                        auth=(username, password))

else:
    print('\n--> Using Token authentication...')
    print('\n--> Getting a list of sites in the org...', end='')

    r_headers: dict = {  # Use token authorization
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Token {token}'
    }

    response: object = requests.request('GET', r_url, headers=r_headers, params=params, data=json.dumps(r_payload))

## Analyze the initial response
if response.status_code != 200:
    print(
        f'\n|-> Request unsuccessful, status code: {response.status_code} ({response.reason}). Cannot read the list of sites. Please check your authentication and Org ID details.')
else:
    list_sites_output: dict = json.loads(response.text)  # Convert JSON string response to dict()

    sites_list: dict = {}  # This is where Org's list of sites and their names will reside

    for site in list_sites_output:  # Build a list of sites in the org
        sites_list[site['name']] = site['id']

    # Get devices details in each site
    print(f'DONE')
    print(f'--> Getting information about devices in each site...')

    devices_data: list = []  # This is where all device data gather will reside

    for site_name, site_id in sites_list.items():  # Get each site from the list of sites and get devices stats

        print(f'|-> Analyzing {site_name}...', end='')

        # Set the second API request parameters. If the specific parameter is not set here the initial parameters wil be used
        r_url = f'https://{api_url}/api/v1/sites/{site_id}/stats/devices'
        params = {'type': 'all', 'status': 'connected'}

        # Generate request and get response based on authentication type
        if auth_choice in ['U', 'u']:  # For basic authentication
            response = requests.request('GET', r_url, headers=r_headers, params=params, data=json.dumps(r_payload),
                                        auth=(username, password))
        else:  # For token authentication
            response = requests.request('GET', r_url, headers=r_headers, params=params, data=json.dumps(r_payload))

        # Analyze response
        if response.status_code != 200:
            print(
                f'\n|-> Request unsuccessful, status code: {response.status_code} ({response.reason}). Cannot read devices stats in site ID {site_id}!')
        else:
            devices_stats_output: dict = json.loads(response.text)  # Convert JSON string response to dict()

            for device in devices_stats_output:
                devices_data.append(  # Define needed device stats here
                    {
                        'Site name': site_name,
                        'Device type': device['type'],
                        'Device name': device['name'],
                        'Device version': device['version']
                    }
                )
            print('DONE')

    # Write results to CSV file
    fieldnames: list = ['Site name', 'Device name', 'Device type',
                        'Device version']  # Define which dict keys will be written to CSV

    with open('output/devices_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(devices_data)

    print(
        f'\nAnalysis of devices stats in all sites in org ID: {org_id} was SUCCESSFUL. The results are found in file: "./output/devices_data.csv"')
