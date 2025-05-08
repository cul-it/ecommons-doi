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
# run with the command 'python mint-datacite-api.py -f yourfilename'
# by default dois will be created in test. to create in prod do:
# 'python mint-datacite-api.py -f yourfilename -s prod'
# you'll get an output file with the name of your file appended with "_update" that will have
# the new dois in it.

parser = argparse.ArgumentParser(description='Select file and shoulder')

parser.add_argument("-s", "--shoulder", dest="shoulder",
					default="test",
					help="Uses test shoulder by default use prod to mint production DOIs")
parser.add_argument("-f", dest="file", help="file name in this directory")

# Retrieve credentials for FOLIO
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
	with open(in_file.split(".")[0] + "_update.csv", 'w') as updatefile:

		writer = csv.writer(updatefile)
		writer.writerow(["id", "collection", "dc.identifier.doi"])
		for record in reader:
			if record['dc.title[]']:
				title = record['dc.title[]']
			else:
				title = "None"
				with open('notitlesETDs.txt', 'a') as fother:
					fother.write(record['id'])
					fother.write('\n')

			if record['dc.date.issued[]']:
				pubdate = record['dc.date.issued[]'][:4]
			else:
				pubdate = "None"
				with open('noyearsETDs.txt', 'a') as fyrother:
					fyrother.write(record['id'])
					fyrother.write('\n')
			build_datacite = {
				"type": "dois",
				"attributes": {
					#"event": "publish",
					"prefix": shoulder,
					"titles": [{
						"title": title
					}],
					"publisher": "Cornell University Library",
					"publicationYear": pubdate,
					"types": {
						"resourceTypeGeneral": "Text"
					},
					"url": record["dc.identifier.uri"],
					"schemaVersion": "http://datacite.org/schema/kernel-4"
				}
			}

			if record["ORCID"]:
				build_datacite["attributes"]["creators"] = [
					{
						"nameType": "Personal",
						"name": record['dc.contributor.author[]'],
						"nameIdentifiers": [
							{
								"nameIdentifier": record["ORCID"],
								"nameIdentifierScheme": "ORCID",
								"schemeUri": "https://orcid.org",
							}],
						"affiliation": [
							{
								"name": "Cornell University",
								"schemeUri": "https://ror.org",
								"affiliationIdentifier": "https://ror.org/05bnh6r87",
								"affiliationIdentifierScheme": "ROR"
							}]
					}]
			else:
				build_datacite["attributes"]["creators"] = [
					{
						"name": record['dc.contributor.author[]'],

						"affiliation": [
							{
								"name": "Cornell University",
								"schemeUri": "https://ror.org",
								"affiliationIdentifier": "https://ror.org/05bnh6r87",
								"affiliationIdentifierScheme": "ROR"
							}
						]
					}
				]
			datacite = {}
			datacite["data"] = build_datacite
			new_doi = requests.post(url, headers=headers, data=(json.dumps(datacite))).json()
			record['dc.identifier.doi'] = "http://doi.org/" + \
				new_doi["data"]["id"]
			print(new_doi)
			writer.writerow(
				[record["dc.title[]"], record["collection"], record["dc.identifier.doi"]])
