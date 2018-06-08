"""
Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
"""
@author Washim Bari
"""
"""
This script provides a function to get DNAC authentication token
and functions to make DNAC REST APIs request
All required modules are imported in this script so from other scripts just need to import this script
"""
import requests   # We use Python external "requests" module to do HTTP query
import json
import sys
from requests.auth import HTTPBasicAuth

# All DNAC configuration is in dnac_config.py
import dnac_config  # DNAC IP is assigned in dnac_config.py

# It's used to get rid of certificate warning messages when using Python 3.
# For more information please refer to: https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings() # Disable warning message

def get_X_auth_token(ip=dnac_config.DNAC_IP, ver=dnac_config.VERSION, uname=dnac_config.USERNAME, pword=dnac_config.PASSWORD):
    """
    This function returns a new JWT token.
    Passing ip, version,username and password when use as standalone function
    to overwrite the configuration above.

    Parameters
    ----------
    ip (str): dnac routable DNS address or ip
    ver (str): dnac version
    uname (str): user name to authenticate with
    pword (str): password to authenticate with

    Return:
    ----------
    str: DNAC authentication token
    """

    # The url for the post ticket API request
    post_url = "https://"+ip+"/api/system/"+ ver +"/auth/token"
    # All DNAC REST API query and response content type is JSON
    headers = {'content-type': 'application/json'}
    # POST request and response
    try:
        r = requests.post(post_url, auth=HTTPBasicAuth(username=uname, password=pword), headers=headers,verify=False)
        # Remove '#' if need to print out response
        #print (r.text)
        r.raise_for_status()
        # return service ticket
        return r.json()["Token"]
    except requests.exceptions.ConnectionError as e:
        # Something wrong, cannot get service ticket
        print ("Error: %s" % e)
        sys.exit ()

def get(ip=dnac_config.DNAC_IP, ver=dnac_config.VERSION, uname=dnac_config.USERNAME, pword=dnac_config.PASSWORD, api='', params=''):
    """
    To simplify requests.get with default configuration.Return is the same as requests.get

    Parameters
    ----------
    ip (str): dnac routable DNS address or ip
    ver (str): dnac version
    uname (str): user name to authenticate with
    pword (str): password to authenticate with
    api (str): dnac api without prefix
    params (str): optional parameter for GET request

    Return:
    -------
    object: an instance of the Response object(of requests module)
    """
    ticket = get_X_auth_token(ip,ver,uname,pword)
    headers = {"X-Auth-Token": ticket}
    url = "https://"+ip+"/api/"+ver+"/"+api
    print ("\nExecuting GET '%s'\n"%url)
    try:
    # The request and response of "GET" request
        resp= requests.get(url,headers=headers,params=params,verify = False)
        print ("GET '%s' Status: "%api,resp.status_code,'\n') # This is the http request status
        return(resp)
    except:
       print ("Something wrong with GET /",api)
       sys.exit()

def post(ip=dnac_config.DNAC_IP, ver=dnac_config.VERSION, uname=dnac_config.USERNAME, pword=dnac_config.PASSWORD, api='', data=''):
    """
    To simplify requests.post with default configuration. Return is the same as requests.post

    Parameters
    ----------
    ip (str): dnac routable DNS address or ip
    ver (str): dnac version
    uname (str): user name to authenticate with
    pword (str): password to authenticate with
    api (str): dnac api without prefix
    data (JSON): JSON object

    Return:
    -------
    object: an instance of the Response object(of requests module)
    """
    ticket = get_X_auth_token(ip,ver,uname,pword)
    headers = {"content-type" : "application/json","X-Auth-Token": ticket}
    url = "https://"+ip+"/api/"+ver+"/"+api
    print ("\nExecuting POST '%s'\n"%url)
    try:
    # The request and response of "POST" request
        resp= requests.post(url,json.dumps(data),headers=headers,verify = False)
        print ("POST '%s' Status: "%api,resp.status_code,'\n') # This is the http request status
        return(resp)
    except:
       print ("Something wrong with POST /",api)
       sys.exit()

