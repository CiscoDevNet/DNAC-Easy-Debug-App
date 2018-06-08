# DNAC-Easy-Debug-App

### Description
Whenever there is are error/crash on the network device there is no immediate notification to the user.
When the administrator sees the issue on DNA, next steps is to collect logs/additional  info. This idea
is to deploy a python EEM that runs periodically within guest shell on the device and as soon as it
detects a problem condition immediately capture the logs/core files , turns on further debug etc and
uploads this to DNA-C.  Network Administrator doesn’t need to wait for end user to report this issue.
This enables proactive troubleshooting. when the issue is seen on Assurance UI already the required
debug files are available.

### Prerequisite
- Device should be added to inventory.
- Following python packages should be pre installed.
   - requests
   - json
   - time
   - re
   - sys

### Configuring the Script
Before running the script you must edit the 'dnac_config.py' file and update the following values
```
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
```

### Running Python script
```
python3 deviceLogCollector.py
```

### Embedded Event Manager Script that would be deployed
- For VMAN Process following EEM Script will be deployed.
- FTP Server, Username , Password will be fetch from dnac_config
```sh
    event manager applet DNACGetLog
    event timer watchdog time 1800
    action 001 cli command "file prompt quiet"
    action 002 cli command "enable"
    action 003 cli command "config terminal"
    action 004 cli command "ip ftp username <ftp-username>"
    action 005 cli command "ip ftp password <ftp-password>"
    action 006 cli command "end"
    action 100 cli command "show plat soft trace filter-binary process <process-name> level error"
    action 110 regexp "ERR" "$_cli_result" result
    action 120 if $_regexp_result eq "1"
    action 125  cli command "request platform soft trace rotate all"
    action 130  cli command "archive tar /create bootflash:smand_error_$_event_pub_sec.tar bootflash:tracelogs smand*"
    action 140  cli command "copy bootflash:smand_error_$_event_pub_sec.tar ftp://<ftp-ip-address>"
    action 160  puts "Copied Collected logs to FTP Server"
    action 160 else
    action 170  puts "No logs to collect"
    action 180 end