#!/usr/bin/python2.7 

# File name: sendSMS.py
# Author: Daniel Gullin
# Date created: 2016-10-19
# Version: 0.1
# License: GPL

import requests
import argparse
import re

### Settings ###
# File with msisdn
file = "phoneNumbers.cfg"

# If no source msisdn we use xxx as default (max 11 car)
default = "xxx"

# Base64-encoded authorization (https://www.base64encode.org/) user:password
auth = "xxx"

# The URL to GenericSMS HTTP API
url = "https://api.genericmobile.se/SmsGateway/api/v1/Message"

###################
# DON'T TOUCH BELOW
###################

# Arguments
parser = argparse.ArgumentParser(description="Send SMS through GenericSMS, usually used by OP5")
parser.add_argument("-s", "--source", help="Source MSISDN, default is xxx")
parser.add_argument("-d", "--destination", type=str, help="Destination MSISDN, use international style +4670xxxxxxx format. If no destination is used file test.txt will be used")
parser.add_argument("-m", "--message", type=str, help="The Hot Message", required=True)
parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
args = parser.parse_args()

# If no source number we shall use xxx as default
if args.source == None: args.source = default

# The mighty send function!
def send_sms(msisdn):
        msisdn = re.sub(r'^0', "+46", msisdn)
        payload = '{\n    \"From\":\"%s\",\n    \"To\":["%s"],\n    \"Text\":\"%s"\n}' % (args.source, msisdn, args.message)
        if args.verbose: print "%s\n" % payload
        headers = {
                'authorization': "Basic %s" % (auth),
                'accept': "application/json",
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "c7577af4-733d-fe98-ba1b-1728df06d687"
                }
        response = requests.request("POST", url, data=payload, headers=headers)
        if args.verbose: 
                print(response.text)
                print "\n"
        return

# If no destination, use /var/www/html/sms/phoneNumbers.cfg 
if args.destination == None:
        f = open(file, "r")
        for line in f:
                #line = re.sub(r'^#.*', "", line)
                line = line.rstrip("\r\n")
                if line.isdigit(): send_sms(line)
else:
                send_sms(args.destination)
