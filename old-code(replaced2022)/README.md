# eCommons ETDs to DOIs

Built/tested/recommended to use with Python 2.7. EZID.py script which we wrap around requires work to function with Python 3.

## Goal

We want to take eCommons handles and metadata - in particular, for electronic dissertations and theses - once loaded, use the handles and basic eCommons metadata to generate DOIs using the [EZID DOI API](http://ezid.cdlib.org/doc/apidoc.html#python-example), then push those DOIs back into the dc.identifier.doi metadata field in eCommons.

Eventually, this will be migrated into the ETDs processing workflow as an automatic post-processing/post-ingest enhancement step.

## How to Use

### Preparation

*Run once if you don't have these scripts on your computer:*

1. Clone or download a copy of this code repository locally: `$ git clone https://github.com/cul-it/ecommons-doi.git`
2. Change into the directory where this is cloned, then install requirements using pip (run this command in a command line interface/shell and in the directory where you stored the code repository): `$ pip install -r requirements.txt`

*Run before each time you start the ETD to DOI process:*

2. Change into the directory where these scripts live on your computer: `$ cd ~/Tools/ecommons-doi` (change the last part to the path for your computer)
3. Pull latest changes from GitHub repository for this script: `$ git pull origin master`
4. Grab an unaltered copy of the eCommons CSV metadata/collection export that you wish to work off of. **The column names need to match the eCommons field names.** Fields and dates out of scope for this workflow will be removed as part of the script. It's easiest if you move the eCommons export CSV into the `data` directory in this repository (`data` is ignored by git, so will not be overwritten by `git pull origin master` and will not appear if you push anything back to GitHub).

### Run the ETD Generation Job in 1 Process:

5. Run the following script in the top level of the directory where these scripts live, with the appropriate options filled in:
`$ python etddoi.py -u 'EZID username' -p 'EZID password' -s 'DOI shoulder in for 11.1111/XX1' -d 'Date on or after to create DOIs for in form YYYY-MM' /path/to/the/eCommonsCSVexportFile.csv`
example:
`$ python etddoi.py -u 'username' -p 'password' -s '10.5072/FK2' -d '2016-04' 1813.47.csv`
6. Let the script run. It will create a directory called `data/YYYYMMDD_HHMMSS/` (named based off when the script was run). In that directory will be a file called `EC.csv` (the eCommons CSV with DOIs added, ready for reloading into eCommons) and the ANVL text files (with DOIs appended after generation). Wait for the script to complete before opening these files.
7. Once complete, review `data/YYYYMMDD_HHMMSS/EC.csv`, then send to Mira for loading/metadata batch update. There is also `data/YYYYMMDD_HHMMSS/EC_reviewOnly.csv` which has a fuller set of eCommons metadata and the new DOI for further review as needed.

Example of the full process for this option:

```bash
$ cd ~/Tools/ecommons-doi
$ git pull origin master
 From https://github.com/cul-it/ecommons-doi.git
  * branch            master     -> FETCH_HEAD
 Already up-to-date.
 # Metadata Export from https://ecommons.cornell.edu/handle/1813/47
 # Manually Downloaded as '1813-47.csv to ~/Downloads'
$ mv ~/Downloads/1813-47.csv data/
$ python etddoi.py -u 'username' -p 'password' -s '10.5072/FK2' -d '2017-01' data/1813-47.csv
... (DOI generation output)
```


### Run the ETD Generation Job in 2 Processes: 1. Generate ANVL files, then 2. Mint DOIs

5. Run the following script in the top level of the directory where these scripts live, with the appropriate options filled in: `python doiparse.py -d 'Date on or after to create DOIs for in form YYYY-MM' /path/to/the/eCommonsCSVexportFile.csv`
6. Let the script run. It will create a directory called `data/YYYYMMDD_HHMMSS/` (named based off when the script was run). In that directory will be a file called `EC.csv` (the eCommons CSV with DOIs added, _not yet ready_ for reloading into eCommons) and the ANVL text files (with DOIs appended after generation). Wait for the script to complete before opening these files. The script will tell you when it is complete.
7. Open the ANVL files and review all you like. When ready to generate DOIs, run this script (the path to ANVL files will be whatever is output in the last line of running the above script): `$ python mintdoi.py -u 'EZID username' -p 'EZID password' -s 'DOI shoulder in for 11.1111/XX1' path/to/directory/with/ANVLfiles/`
8. Once complete, review `data/YYYYMMDD_HHMMSS/EC.csv`, then send to Mira for loading/metadata batch update.

Example of the full process for this option:

```bash
$ cd ~/Tools/ecommons-doi
$ git pull origin master
 From https://github.com/cul-it/ecommons-doi.git
  * branch            master     -> FETCH_HEAD
 Already up-to-date.
 # Metadata Export from https://ecommons.cornell.edu/handle/1813/47
 # Manually Downloaded as '1813-47.csv to ~/Downloads'
$ mv ~/Downloads/1813-47.csv data/
$ python doiparse.py -d '2016-04' data/1813-47.csv
Records in the collection: 5570
Records to be updated with DOIs: 145
creating ANVL files in data/20160711_183606/
ANVL txt files created.
ANVL files available in: data/20160711_183606/
$ python mintdoi.py -u 'username' -p 'password' -s '10.5072/FK2' -d '2016-04' data/20160711_183606/
... (DOI generation output)
```

### Note on starting CSV file:

These scripts needs the eCommons CSV as exported. It is targeted right now to working with the Graduate School ETDs collection (fields in other collections may/may not be ignored). It will automatically check and not process eCommons records that already have a value in the dc.identifier.doi field. It will process all records in a collection CSV otherwise unless a date is given (i.e., the text script above processes all ETD records where the ETD was submitted on or after 2016-04). If a datacite required field isn't found for a record, it will use a default of 'Unknown' at the moment. This can be changed for validation purposes (right now, no ETDs should encounter this issue, but checks are in place to generate missing field text files upon running this script).


## Editing a set of DOIs

If you made a mistake on DOIs metadata that have already been created, you can use the following to batch update:

### Preparation

*Run once if you don't have these scripts on your computer:*

1. Clone or download a copy of this code repository locally: `$ git clone https://github.com/cul-it/ecommons-doi.git`
2. Change into the directory where this is cloned, then install requirements using pip (run this command in a command line interface/shell and in the directory where you stored the code repository): `$ pip install -r requirements.txt`

*Run before each time you start the ETD to DOI process:*

2. Change into the directory where these scripts live on your computer: `$ cd ~/Tools/ecommons-doi` (change the last part to the path for your computer)
3. Pull latest changes from GitHub repository for this script: `$ git pull origin master`
4. Grab a copy of the eCommons CSV metadata/collection export that you wish to work off of. **The column names need to match the eCommons field names.** Fields and dates out of scope for this workflow will be removed as part of the script. It's easiest if you move the eCommons export CSV into the `data` directory in this repository (`data` is ignored by git, so will not be overwritten by `git pull origin master` and will not appear if you push anything back to GitHub). Edit this CSV only where you need to make a change to the DOI metadata using the eCommons CSV headers - as one example, if you generated DOIs with the wrong handles, and the eCommons export with handles are correct, the new export handles will overwrite the old ones.

### Run the ETD Edit (Metadata or Target URL [handle]) Job:

5. Run the following script in the top level of the directory where these scripts live, with the appropriate options filled in (including a required -m to update metadata or -t to update the taret URL (i.e. the handle the DOI points to). To not overwhelm the EZID servers, we don't update both at the same time):
`$ python editdoi.py -m|t -u 'EZID username' -p 'EZID password' -d 'Issue Date on or after to edit record DOIs in form YYYY-MM' /path/to/the/eCommonsCSVexportFile.csv`
example to update the DOI metadata:
`$ python editdoi.py -m -u 'username' -p 'password' -d '2016-12' data/1813-47.csv`
example to update the DOI target URL:
`$ python editdoi.py -t -u 'username' -p 'password' -d '2016-12' data/1813-47.csv`
6. Let the script run. It will create a directory called `data/YYYYMMDD_HHMMSS/` (named based off when the script was run). In that directory will be a file called `EC.csv` (the eCommons CSV edited or with changes for pushing to DOI metadata) and the ANVL text files (updated for metadata changes). Wait for the script to complete before opening these files.
7. Once complete, review `data/YYYYMMDD_HHMMSS/` files for post-update further review as needed.

Example of the full process to edit DOI metadata:

```bash
$ cd ~/Tools/ecommons-doi
$ git pull origin master
 From https://github.com/cul-it/ecommons-doi.git
  * branch            master     -> FETCH_HEAD
 Already up-to-date.
 # Metadata Export from https://ecommons.cornell.edu/handle/1813/47
 # Manually Downloaded as '1813-47.csv to ~/Downloads'
$ mv ~/Downloads/1813-47.csv data/
$ python editdoi.py -m -u 'username' -p 'password' -d '2016-12' data/1813-47.csv
... (DOI update notification output)
```

Example of the full process to edit DOI target URLs:

```bash
$ cd ~/Tools/ecommons-doi
$ git pull origin master
 From https://github.com/cul-it/ecommons-doi.git
  * branch            master     -> FETCH_HEAD
 Already up-to-date.
 # Metadata Export from https://ecommons.cornell.edu/handle/1813/47
 # Manually Downloaded as '1813-47.csv to ~/Downloads'
$ mv ~/Downloads/1813-47.csv data/
$ python editdoi.py -t -u 'username' -p 'password' -d '2016-12' data/1813-47.csv
... (DOI update notification output)
```

## Further Scripts Workflow Docs (ignore if not wanting to understand the Python)

Currently expected to run locally. Will eventually move this to metasrv most likely for inclusion in the ETDs workflows.

### 1. Grab eCommons ETDs metadata for specific cycle (manual)

- Log into eCommons, export collection CSV from https://ecommons.cornell.edu/handle/1813/47
- Move CSV export into working directory.
- Manually review if/as needed.

To be done: automate this step.

### 2. Prepare/Queue CSV metadata for DOI generation (automated)

- Remove rows not in selected date range or conferral cycle.
- Verify DOIs do not already exist in CSV export selection.
- Remove fields not to be used in generation of DOI or eCommons update (see mapping)

### 3. DOI generation part 1: EZID Metadata Files Creation (automated)

- Create subdirectory for job to store EZID Metadata .txt files following example given
- Create new text file with ANVL metadata added for each row in eCommons CSV / each eCommons handle. Store in subdirectory

### 4. DOI generation part 2: EZID Creation and Capture (automated)

- Run ezid.py script for each eCommons handle to mint DOI and use metadata in related text ANVL file.
- If successful, capture handle and doi in ANVL file and EC.csv.
- If unsuccessful, stop script and write out error to CLI for review.

To be done: Error and exception handling for the ezid.py script.

### 5. Update eCommons (manual)

- Manually review (look over briefly) of the `EC.csv` in the appropriate working directory (`/data/DATE_TIME`)
- Should have handle (`dc.identifier.uri`) , DOI (`dc.identifier.doi`), mapped back to eCommons columns/fields
- Send `EC.csv` to eCommons staff for batch update.

To be done: Automate pushing updates?
