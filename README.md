# About

The script searches for all sites created in the provided Juniper Mist Organization and gathers data about all devices assigned to them. It is preset to output:
- Site name
- Device name
- Device type (ap, switch, gateway)
- Device version (software)

The script can be adopted to gather any devices data available in a site.

## Requirements

- Authentication credentials, either _username and password_ or _token_ having rights to list sites in an organization and get devices statistics from each site in an org
- _Organization UUID_