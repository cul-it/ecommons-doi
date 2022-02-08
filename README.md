# ecommons-doi
Goal: take metadata export from eCommons (a relatively standard csv), upload the appropriate parts to datacite, mint DOIs, and return DOIs in an appropriate format to upload back to eCommons.

## Set up the data:
### Credentials
1. Make a local copy of "datacite_creds_example.ini", rename as "datacite_creds.ini" (expected in script)
2. Get credentials from eCommons team or eCommons documentation in confluence, and populate datacite_creds.ini with both test and production credentials. 
***Don't put the credentials on github!***

### Update metadata


The eCommons metadata export has many fields. Mandatory fields are listed below, other fields will be ignored.

- dc.contributor.author[]
- dc.title[]
- dc.identifier.uri
- dc.date.issued[]
- ORCID

ORCID is not recorded in eCommons, ORCID ids should be added from the ProQuest metadata prior to generating DOIs.

## Run it!
Uses python3. 
- Put the metadata csv in the same local folder as the script. 
- Run from within the local directory where the script is stored.
- Run with the command 'python mint-datacite-api.py -f yourfilename'
- By default dois will be created in test. to create in prod do:
- 'python mint-datacite-api.py -f yourfilename -s prod'

Output is a .csv file with the name of your file appended with "_update" that will have the new dois in it.
