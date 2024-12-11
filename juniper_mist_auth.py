#!/usr/bin/env python3

from getpass import getpass


def get_api_url() -> str:
    mist_clouds: dict[str: dict[str: str]] = {  # Names and API URLs of the current Mist clouds
        'Mist Global 01': {'position': '1', 'url': 'api.mist.com'},
        'Mist Global 02': {'position': '2', 'url': 'api.gc1.mist.com'},
        'Mist Global 03': {'position': '3', 'url': 'api.ac2.mist.com'},
        'Mist Global 04': {'position': '4', 'url': 'api.gc2.mist.com'},
        'Mist EMEA 01': {'position': '5', 'url': 'api.eu.mist.com'},
        'Mist EMEA 02': {'position': '6', 'url': 'api.gc3.mist.com'},
        'Mist EMEA 03': {'position': '7', 'url': 'api.ac6.mist.com'},
        'Mist APAC 01': {'position': '8', 'url': 'api.ac5.mist.com'}
    }

    cloud_choice: str = '0'  # Define initial choice of menu item outside available options
    api_url: str = ''  # Define initial API URL to a blank string

    # Display Mist Clouds menu until the correct number is selected
    while cloud_choice not in [str(i) for i in range(1,
                                                     9)]:  # Loop until chosen number matches on of the numbers allowed in list comprehension
        cloud_choice = str(input(
            '(1) Mist Global 01\n(2) Mist Global 02\n(3) Mist Global 03\n(4) Mist Global 04\n(5) Mist EMEA 01\n(6) Mist EMEA 02\n(7) Mist EMEA 03\n(8) Mist APAC 01\nProvide Mist Cloud number: '))

    # Search for API URL based on the menu number chosen
    for k, v in mist_clouds.items():
        if v['position'] == cloud_choice:
            api_url = v['url']
            print(f'\n---> API target set to {k} ({api_url})\n')

    return api_url


def get_auth_data() -> str:
    auth_choice: str = 'z'  # Define initial choice for authentication option outside available choices to trigger loop

    while auth_choice not in 'TtUu':  # Display Authentication menu until the correct character is selected
        # noinspection SpellCheckingInspection
        auth_choice = str(input("Do you want to use (T)oken or (U)sername / Password for Mist API authentication? "))
    return auth_choice


def get_user_pass() -> tuple[str, str]:
    username: str = str(input("\nProvide your Username: "))
    password: str = str(getpass("Provide your Password: "))
    return username, password


def get_token() -> str:
    token: str = str(getpass("\nProvide your Token: "))
    return token
