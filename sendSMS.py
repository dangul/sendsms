#!/usr/bin/python2.7 

# File name: sendSMS.py
# Author: Daniel Gullin
# Date created: 2016-10-19
# Version: 0.2
# License: GPL

import logging
import requests
import argparse
import re

### Settings ###
# File with msisdn
file = "phoneNumbers.cfg"

# If no source msisdn we use xxx as default (max 11 car)
default = "xxx"

# Base64-encoded authorization (https://www.base64encode.org/)
# We use user:PASSWORD
auth = "dXNlcjpQQVNTV09SRA=="

# The URL to GenericSMS HTTP API
url = "https://api.genericmobile.se/SmsGateway/api/v1/Message"

# Log SMS (/var/log/sendSMS.log)
log = True

###################
# DON'T TOUCH BELOW
###################

if log:
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)-8s %(message)s',
                datefmt='%b %d %Y %H:%M:%S',
                filename='/var/log/sendSMS.log',
                filemode='a')

# Arguments
parser = argparse.ArgumentParser(description="Send SMS through GenericSMS, usually used by OP5")
parser.add_argument("-s", "--source", help="Source MSISDN, default is BallouDrift")
parser.add_argument("-d", "--destination", type=str, help="Destination MSISDN, use international style +4670xxxxxxx format. If no destination is used file test.txt will be used")
parser.add_argument("-m", "--message", type=str, help="The Hot Message", required=True)
parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
args = parser.parse_args()

# If no source number we shall use BallouDrift as default
if args.source == None: args.source = default

# The mighty send function!
def send_sms(msisdn):
        msisdn = re.sub(r'^0', "+46", msisdn)
        payload = '{\n    \"From\":\"%s\",\n    \"To\":["%s"],\n    \"Text\":\"%s"\n}' % (args.source, msisdn, args.message)
        headers = {
                'authorization': "Basic %s" % (auth),
                'accept': "application/json",
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "c7577af4-733d-fe98-ba1b-1728df06d687"
                }
        response = requests.request("POST", url, data=payload, headers=headers)
        if args.verbose: print "%s \n\n%s \n" % (payload, response.text)

        if log:
                logging.debug('From: %s', args.source)
                logging.debug('To: %s', msisdn )
                logging.debug("Text: %s", args.message )
                logging.debug("Response: %s", response.text )

# If no destination, use $phoneNumbers.cfg 
if args.destination == None:
        f = open(file, "r")
        for line in f:
                line = line.rstrip("\r\n")
                if line.isdigit(): send_sms(line)
else:
                send_sms(args.destination)
