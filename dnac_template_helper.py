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
This file contains helper methods to
 -create a template project
 -create a template
 -commit the template
 -deploy the template
"""

from dnac_api_helper import *
import dnac_config
import json


def create_template_project(project_name="DNAC-Templates"):
    '''
    Method to create a Template Programmer Project on DNAC.
    :param project_name: Template Programmer Project Name. Default value is DNAC-Templates
    :return: Returns Task ID
    '''
    try:
        json_data = {
                  "name": project_name,
                  "description": "Collection of EEM Templates",
                  "tags": [
                    ""
                  ]
                }
        # The request and response of POST  template-programmer/project API
        resp = post(api="template-programmer/project", data=json_data)
        status = resp.status_code
        template = resp.text

    except ValueError:
        print("Something wrong, can't create template project")
        sys.exit()

    if status != 202:
        print(resp.text)
        sys.exit()
    else:
        template_json = json.loads(template)
        print(json.dumps(template_json, indent=4, sort_keys=True))
        print(resp.json()["response"]["taskId"])
        return resp.json()["response"]["taskId"]


def get_template_project_id(project_name="DNAC-Templates"):

    '''
    Method to get the project id for a given Template project
    Send a GET request to template-programmer/project/ API.
    :param project_name: Project Name , default DNAC-Templates
    :return: Returns Project ID
    '''

    try:
        # The request and response of GET  API template-programmer/ API
        resp = get(api="template-programmer/project?name=" + project_name)
        status = resp.status_code
        project = resp.text

    except ValueError:
        print("Something wrong, cannot get project ID")
        sys.exit()

    if status != 200:
        print(resp.text)
        sys.exit()
    else:
        project_json = json.loads(project)
        print(json.dumps(project_json, indent=4, sort_keys=True))
        print(resp.json()[0]["id"])
        return resp.json()[0]["id"]


def create_template(project_id, script , template_name=dnac_config.TEMPLATE_NAME,
                    product_family=dnac_config.PRODUCT_FAMILY):
    '''
    Method to create a template on DNAC.
    POST to template-programmer/project/{projectID}/template
    :param project_id: Project ID for Template Project under which template need to be created.
    :param script: EEM Script that need to be deployed.
    :param template_name: Template Name. Configured via dnac_config.TEMPLATE_NAME.
    :param product_family: Product Family of the device. Configured via dnac_config.PRODUCT_FAMILY.
    :return: Task ID
    '''
    try:
        json_data ={"name": template_name,
                    "description": "",
                    "tags": [],
                    "deviceTypes": [{
                        "productFamily": product_family,
                        "productSeries": "",
                        "productSeries": "",
                        "productType": "",
                    }],
                    "softwareType": "IOS-XE",
                    "containingTemplates": [],
                    "templateContent": script,
                    "templateParams": []
                    }
        # The request and response of POST template-programmer/project/{projectID}/template API
        resp = post(api="template-programmer/project/" + project_id + "/template", data=json_data)
        status = resp.status_code
        template = resp.text

    except ValueError:
        print("Something wrong, can't create template")
        sys.exit()

    if status != 202:
        print(resp.text)
        sys.exit()
    else:
        template_json = json.loads(template)
        print(json.dumps(template_json, indent=4, sort_keys=True))
        print(resp.json()["response"]["taskId"])
        return resp.json()["response"]["taskId"]


def get_parent_template_id(project_id, template_name=dnac_config.TEMPLATE_NAME):
    '''
    Method to get the Parent Template ID for a given Template.
    GET Method to template-programmer/project/{projectID}/template
    :param project_id: Project ID of the Template Programmer Project
    :param template_name: Template Name. Configured via dnac_config.TEMPLATE_NAME.
    :return: Returns Parent Template ID
    '''
    try:
        # The request and response of GET template-programmer/template API
        resp = get(api="template-programmer/project/" + project_id + "/template")
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
        for index in template_json:
            for key in index:
                if index[key] == template_name:
                    template_id = index["id"]
                    print(template_id)
                    return template_id


def commit_template(template_id):
    '''
    Method to commit a template in DNAC.
    Post to template-programmer/template/version
    :param template_id:  Template ID of the Template.
    :return: Returns None
    '''
    try:
        json_data = {
            "templateId": template_id,
            "comments": "Committing template"
        }
        # The request and response of Post template-programmer/template/version API
        resp = post(api="template-programmer/template/version", data=json_data)
        status = resp.status_code
        template = resp.text

    except ValueError:
        print("Something wrong, cannot commit template")
        sys.exit()

    if status != 202:
        print(resp.text)
        sys.exit()
    else:
        template_json = json.loads(template)
        print(json.dumps(template_json, indent=4, sort_keys=True))


def get_templateid(template_name= dnac_config.TEMPLATE_NAME):
    '''
    Method to get the Template ID
    :param template_name: Template Name. Configured via dnac_config.TEMPLATE_NAME.
    :return: Template ID
    '''
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
        template_id = get_filtered_templateID(template_json)
        return template_id


def get_template_version(template_ID):
    '''
    Method to get a particular Version ID for a template
    GET to template-programmer/template/version/{template_ID}
    :param template_ID: Template ID of the Template
    :return: Version ID.
    '''
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


def deploy_template(version_id, network_uuid):
    '''
    Method to deploy a Template to a device.
    :param version_id: Version ID of the Template.
    :param network_uuid: Device Network UUID.
    :return: Returns Task ID.
    '''
    jsondata = {"templateId": version_id,
                "targetInfo": [
                    {
                        "type":"MANAGED_DEVICE_UUID",
                        "id": network_uuid
                    }
                 ]}
    try:
        # The request and response of POST template-programmer/template/deploy API
        resp = post(api="template-programmer/template/deploy", data=jsondata)
        status = resp.status_code
        template = resp.text

    except ValueError:
        print("Something wrong, deployment failed")
        sys.exit()

    if status != 202:
        print(resp.text)
        sys.exit()
    else:
        template_json = json.loads(template)
        print(json.dumps(template_json, indent=4, sort_keys=True))
        print("deployment ID : {}".format(template_json["deploymentId"]))
        return template_json["deploymentId"]


def check_status(deploy_ID):
    '''
    This method check the status of the deployed template.
    GET request to template-programmer/template/deploy/status/{DeploymentID}
    :param deploy_ID: Deployment ID
    :return: JSON containing the status of the deployment.
    '''
    try:
        # The request and response of GET template-programmer/template/deploy/status/ API
        resp = get(api="template-programmer/template/deploy/status/"+deploy_ID)
        status = resp.status_code
        template = resp.text

    except ValueError:
        print("Something wrong, cannot get deployment status")
        sys.exit()

    if status != 202:
        print(resp.text)
        sys.exit()
    else:
        template_json = json.loads(template)
        print(json.dumps(template_json, indent=4, sort_keys=True))
        return(template_json)


def get_filtered_templateID(template_json, filter=dnac_config.TEMPLATE_NAME):
    for index in template_json:
        for key in index:
            if index[key] == filter:
                template_ID = index["templateId"]
                print(template_ID)
                return(template_ID)


def get_filtered_version(template_json):
    version = 0
    for index in template_json[0]["versionsInfo"]:
        for key in index:
            if key == "version" and int(index[key]) > version:
                version = int(index[key])
                # print(version)

    for index in template_json[0]["versionsInfo"]:
        for key in index:
            if index[key] == str(version):
                version_ID = index["id"]
                # print(version_ID)
                return(version_ID)
