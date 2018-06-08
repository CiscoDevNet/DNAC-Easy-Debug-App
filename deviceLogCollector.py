#!/usr/bin/env python
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
This script calls Template Programmer & Network Device APIs and deploy an EEM Script on the device to collect
BTTracelogs automatically and send them to FTP server whenever there is error seen in the tracelogs.
All simplify REST request functions and get authentication token function are in dnac-api-helper.py
Controller ip, username and password are defined in dnac_config.py
"""

from dnac_api_helper import *
from dnac_template_helper import *
import dnac_config
import json
import time
import re


def get_network_device_id(device_ip = dnac_config.DEVICE_IP):

    '''
    Get the Device UUID for a given IP address
    Get to network-device/ip-address/{device_ip}
    :param device_ip: Device IP address which has been added to the inventory
    :return: Returns device UUID
    '''

    try:
        # The request and response of GET network-device/ip-address/ API
        resp = get(api="network-device/ip-address/"+device_ip)
        status = resp.status_code
        device = resp.text

    except ValueError:
        print("Something wrong, cannot get network device information")
        sys.exit()

    if status != 200:
        print(resp.text)
        sys.exit()

    if device == []:  # Response is empty, no network-device is discovered.
        print("No network device found with IP {} !".format(device_ip))
        sys.exit()
    else:
        device_json = json.loads(device)
        print(json.dumps(device_json, indent=4, sort_keys=True))
        print(resp.json()["response"]["instanceUuid"])
        return resp.json()["response"]["instanceUuid"]


def create_eem_script(ios_process=dnac_config.PROCESS_NAME,ftp_server_ip=dnac_config.FTP_SERVER,
                      ftp_user=dnac_config.FTP_USERNAME, ftp_pass=dnac_config.FTP_PASSWORD,
                      query_interval=dnac_config.QUERY_INTERVAL):
    '''
    Method to Create a Event Manager Script that will be pushed to the device via Template Programmer.
    :param ios_process: IOS Process Name for which Logs need to be collected.Configured via dnac_config.PROCESS_NAME
    :param ftp_server_ip: FTP Server IP address where logs need to be copied. Configured via dnac_config.FTP_Server
    :param ftp_user: FTP Server username. Configured via dnac_config.FTP_USERNAME
    :param ftp_pass: FTP Server password. Configured via dnac_config.FTP_PASSWORD
    :param query_interval: EEM Run interval in seconds
    :return: Return EEM Script
    '''
    script = """event manager applet DNACGetLog
                event timer watchdog time """ + query_interval + """
                action 001 cli command \"file prompt quiet\"
                action 002 cli command \"enable\"
                action 003 cli command \"config terminal\"
                action 004 cli command \"ip ftp username """ + ftp_user + """\"
                action 005 cli command \"ip ftp password """ + ftp_pass + """\"
                action 006 cli command \"end\"
                action 100 cli command \"show plat soft trace filter-binary process """ + ios_process + """ level error\"
                action 110 regexp \"ERR\" \"$_cli_result\" result
                action 120 if $_regexp_result eq \"1\"
                action 125  cli command \"request platform soft trace rotate all\"
                action 130  cli command \"archive tar /create bootflash:""" + ios_process + """_error_$_event_pub_sec.tar bootflash:tracelogs """ + ios_process + """*\"
                action 140  cli command \"copy bootflash:""" + ios_process + """_error_$_event_pub_sec.tar ftp://""" + ftp_server_ip + """\"
                action 150  puts \"Copied Collected logs to FTP Server\"
                action 160 else
                action 170  puts \"No logs to collected\"
                action 180 end"""
    print("----------------- EEM Script that will be Deployed ------------------")
    print(script)
    return script


def get_templateID(template_name= dnac_config.TEMPLATE_NAME):
    try:
        # The request and response of GET template-programmer/template API
        resp = get(api="template-programmer/template")
        status = resp.status_code
        template = resp.text

    except ValueError:
        print("Something wrong, cannot get template information")
        sys.exit()

    if status != 200:
        print(resp.text)
        sys.exit()
    else:
        template_json = json.loads(template)
        print(json.dumps(template_json, indent=4, sort_keys=True))
        template_ID = get_filtered_templateID(template_json)
        return(template_ID)


def get_template_version(template_ID):
    try:
        # The request and response of GET template-programmer/template API
        resp = get(api="template-programmer/template/version/"+template_ID)
        status = resp.status_code
        template = resp.text

    except ValueError:
        print("Something wrong, cannot get latest template version information")
        sys.exit()

    if status != 200:
        print(resp.text)
        sys.exit()
    else:
        template_json = json.loads(template)
        print(json.dumps(template_json, indent=4, sort_keys=True))
        latest_version = get_filtered_version(template_json)
        print(latest_version)
        return(latest_version)


if __name__ == '__main__':
    # device_uuid = get_network_device_id()
    # print(device_uuid)
    print("----------------- Deploying EEM Script to collect tracelogs from devices automatically ---------------- ")
    print("----------------- Creating a new Template Project ----------------------")
    project_task_id = create_template_project()
    get_project_id = get_template_project_id()
    print("----------------- Creating the EEM Script that need to be deployed ----------------------")
    eemscript = create_eem_script()
    eemscript = re.sub('\n\s+', '\n', eemscript)

    print("----------------- Creating a new Template ---------------------")
    task_id = create_template(get_project_id, eemscript)

    parent_template_id = get_parent_template_id(get_project_id)

    commit_template(parent_template_id)

    template_id = get_templateid(parent_template_id)

    print("------------------ Fetching Latest version of a template --------------------")
    version_id = get_template_version(template_id)

    print("------------------ Fetching Device UUID --------------------")
    network_uuid = get_network_device_id()

    print(" --------------- Deploying Template ------------------- ")
    deploy_ID = deploy_template(version_id, network_uuid)
    status = check_status(deploy_ID)
    max_tries = 10
    while max_tries:
        if status["status"] != "SUCCESS":
            time.sleep(30)
            status = check_status(deploy_ID)
            max_tries -= 1
        else:
            print(" --------------- Template deployed Successfully ------------------- ")
            break
    if not max_tries:
        print(" --------------- Fail to deploy the template --------------------")



