#! /usr/bin/env python

import requests
import json
import click
import os
import tabulate
import yaml
import urllib3
import getpass


urllib3.disable_warnings()    # Disables Non-Trusted Certificate warning as vManage WebServer is having self-signed Cert

vmanage_host = input("Enter vManage IP Address: ")
vmanage_port = input("Enter vManage port(Enter 8443, if default): ")
vmanage_username = input("Enter vManage Username: ")
vmanage_password = getpass.getpass(prompt='Enter Password: ')


# if vmanage_host is None or vmanage_port is None or vmanage_username is None or vmanage_password is None:
#     print("CISCO SDWAN details must be set via environment variables before running.")
#     print("export vManage_IP=10.10.20.90")
#     print("export vManage_PORT=8443")
#     print("export vManage_USERNAME=admin")
#     print("export vManage_PASSWORD=C1sco12345")
#     print("")
#     exit()


# Define class authentication with two functions.
# 1. get_jsessionid   - Get the jsessionid using credentials of vManage
# 2. get_token - Get token of session using jsessionid. Later this token will be used to make API call and credentials
#                will not be required.

class Authentication:

    @staticmethod
    def get_jsessionid(vmanage_host, vmanage_port, username, password):
        api = "/j_security_check"
        base_url = "https://%s:%s" % (vmanage_host, vmanage_port)
        url = base_url + api
        payload = {'j_username': username, 'j_password': password}

        response = requests.post(url=url, data=payload, verify=False)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            return (jsessionid[0])
        except:
            print("No J-Session-id found")
            exit()

    @staticmethod
    def get_token(vmanage_host, vmanage_port, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s:%s" % (vmanage_host, vmanage_port)
        api = "/dataservice/client/token"
        url = base_url + api
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return (response.text)
        else:
            return None


# Authenticate to vManage using credentials to get jsessionid and then get token using this jsessionid.

Auth = Authentication()
jsessionid = Auth.get_jsessionid(vmanage_host, vmanage_port, vmanage_username, vmanage_password)
token = Auth.get_token(vmanage_host, vmanage_port, jsessionid)


# Set the header content using received jsessionid & token.
# If no token received, then exclude token from header content.

if token is not None:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid}

# Base URL for API calls.
base_url = "https://%s:%s/dataservice" % (vmanage_host, vmanage_port)

# Append the API call to the base URL.
url = base_url + "/device"

# Execute API call using header value having jsessionid & token.
response = requests.get(url=url, headers=header, verify=False)
if response.status_code == 200:
    items = response.json()
    print("API call successful")
    print(items)
else:
    print("Failed to get list of devices " + str(response.text))
    exit()

url = base_url + "/admin/user/activeSessions"

response = requests.get(url=url, headers=header, verify=False)
if response.status_code == 200:
    items = response.text
    print("2nd API call successful")
    print(items)
else:
    print(response.status_code)
    print("Failed to get list of devices " + str(response.text))
    exit()
