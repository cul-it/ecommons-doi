#!/usr/bin/env python

import requests
import json
import csv
from dateutil import parser
import configparser
import argparse
import base64

#update the file datacite_creds.ini with the correct passwords before running
# to run put the file you are loading into this directory
# run with the command 'python updateDOI-datacite-api.py -f yourfilename'
# by default dois will be updated in test. to create in prod do:
# 'python updateDOI-datacite-api.py -f yourfilename -s prod'
# expects a 2 column CSV with only the handles and the draft DOIs 
# (in columns dc.identifier.uri and dc.identifier.doi)
# Use this script to update Draft DOIs by adding the target URL & publishing

parser = argparse.ArgumentParser(description='Select file and shoulder')

parser.add_argument("-s", "--shoulder", dest="shoulder",
					default="test",
					help="Uses test shoulder by default use prod to mint production DOIs")
parser.add_argument("-f", dest="file", help="file name in this directory")

# Retrieve credentials for datacite
config = configparser.ConfigParser()
config.read('datacite_creds.ini')
prod_pass = config.get('datacite', 'prod')
test_pass = config.get('datacite', 'test')
prod_shoulder = "10.7298"
test_shoulder = "10.23655"
un = "CORNELL.LIBRARY"

args = parser.parse_args()
shoulder = args.shoulder
in_file = args.file

if shoulder == "test":
	shoulder = test_shoulder
	pw = test_pass
	url = "https://api.test.datacite.org/dois"

if shoulder == "prod":
	shoulder = prod_shoulder
	pw = prod_pass
	url = "https://api.datacite.org/dois"

userpass = un + ':' + pw
encoded_u = base64.b64encode(userpass.encode()).decode()
headers = {
	'Authorization': "Basic %s" % encoded_u,
	'Content-type': "application/json"
}

with open(in_file) as csvfile:
	reader = csv.DictReader(csvfile, delimiter=",")
	for record in reader:
		if record['dc.identifier.doi']:
			DOIbase = str(record["dc.identifier.doi"]).removeprefix("https://doi.org/")
			print("DOIBase = " + DOIbase)

		build_datacite = {
			"type": "dois",
			"attributes": {
				"event": "publish",
				"prefix": shoulder,
				"url": record["dc.identifier.uri"],
				"schemaVersion": "http://datacite.org/schema/kernel-4"
				}
			}
		print ("build_datacite complete")
		datacite = {}
		datacite["data"] = build_datacite
		putURL = url + "/" + DOIbase
		print(putURL)
		update_doi = requests.put(putURL, headers=headers, data=(json.dumps(datacite))).json()
		# record['dc.identifier.doi'] = "http://doi.org/" + \
			# new_doi["data"]["id"]
		print(update_doi)
		print("doi updated " + DOIbase)
		# writer.writerow(
			# [record["id"], record["collection"], record["dc.identifier.doi"]])
