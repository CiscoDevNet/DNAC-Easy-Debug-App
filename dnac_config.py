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
Sample Configuration
DNAC_IP = "1.1.1.1"
DNAC_PORT = 443
USERNAME = "username"
PASSWORD = "password"
VERSION = "v1"
DEVICE_IP = "2.2.2.2"
PRODUCT_FAMILY = "Routers"
TEMPLATE_NAME = "MyTemplate"
PROCESS_NAME = "dbm"
FTP_SERVER = "3.3.3.3"
FTP_USERNAME = "ftp-username"
FTP_PASSWORD = "ftp-password"
QUERY_INTERVAL = "1800"
"""
DNAC_IP = "Your DNA Center Cluster IP Address"
DNAC_PORT = 443
USERNAME = "Your DNA Center Username"
PASSWORD = "Your DNA Center Password"
VERSION = "v1"
DEVICE_IP = "Device IP Address"
PRODUCT_FAMILY = "Device Family - Any one from the list {Routers, Switches}"
TEMPLATE_NAME = "Any Name for the Template that you want to deploy"
PROCESS_NAME = "IOS process name - Any one from the list but not limited to {smand, dbm, wcm, pman, fman, hman, vman}"
FTP_SERVER = "Your FTP Server IP Address"
FTP_USERNAME = "Your FTP Server Username"
FTP_PASSWORD = "Your FTP Server Password"
QUERY_INTERVAL = "Time Interval in seconds for EEM run; min 300  to max 604800"
