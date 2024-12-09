# About

The script searches for all sites created in the provided Juniper Mist Organization and gathers data about all devices assigned to them. It is preset to output:
- Site name
- Device name
- Device type (ap, switch, gateway)
- Device version (software version)

The script can be adopted to gather any devices data available in a site.

## Requirements

- Authentication credentials, either _username and password_ or _token_ having rights to list sites in an organization and get devices statistics from each site in an org
  - Note: 2FA/MFA authentication for username and password is not supported
- _Organization UUID_

## Usage

- Install Python environment based on requirements contained in _requirements.txt_ file
- Start _get_devices_stats.py_ script
- Choose Juniper Mist cloud containing your Organization
- Provide authentication data, username and password or token
- Provide Organization ID (UUID) which will be searched for devices data in each site configured in it
- The results are written to CSV file in the _output_ directory

## Example

Based on Juniper Live Demo Organization and changed (non-existing) Organization ID.

```
./get_devices_stats.py

(1) Mist Global 01
(2) Mist Global 02
(3) Mist Global 03
(4) Mist Global 04
(5) Mist EMEA 01
(6) Mist EMEA 02
(7) Mist EMEA 03
(8) Mist APAC 01
Provide Mist Cloud number: 1

---> API target set to Mist Global 01 (api.mist.com)

Do you want to use (T)oken or (U)sername / Password for Mist API authentication? T

Provide your Token: 
Provide your Organization ID: 11111111-2222-3333-4444-555555555555

--> Using Token authentication...

--> Getting a list of sites in the org...DONE
--> Getting information about devices in each site...
|-> Analyzing GS-TN-Demo...DONE
|-> Analyzing sdwan_atlanta...DONE
|-> Analyzing _IoT Site...DONE
|-> Analyzing _LD-AI-Native...DONE
|-> Analyzing sdwan_newyork_hub...DONE
|-> Analyzing sdwan_sanfrancisco_hub...DONE
|-> Analyzing Primary Site...DONE
|-> Analyzing Mist WA Lab (EVE-NG)...DONE
|-> Analyzing sdwan_westford...DONE
|-> Analyzing wan-srx_hub...DONE
|-> Analyzing wan-srx_sunnyvale_spoke...DONE
|-> Analyzing sdwan_onboarding_site...DONE
|-> Analyzing sdwan_denver...DONE
|-> Analyzing Live-Demo...DONE
|-> Analyzing sdwan_phoenix...DONE
|-> Analyzing wan-demo_teleworker...DONE

Analysis of devices stats in all sites in org ID: 11111111-2222-3333-4444-555555555555 was SUCCESSFUL. The results are found in file: "./output/devices_data.csv"
```