# Steps to run the project

## 1. Copy the .env.example file to .env and edit the variables

`cp .env.example .env && rm .env.example`

## 2. Set up a venv with all the dependencies

`chmod +X startup.sh && . startup.sh`

## 3. Run the dedicated script with

`python3 <script.py>`

## 4. Close the session

``python3 close-session.py`

## 5. Deactivate and remove the venv

`chmod +X cleanup.sh && . cleanup.sh`

### Examples of use

#### Retrieve  distribution formats

```sh
python3 retrieve-record-xpath.py
Enter the UUID of the record: c885c51c-a7c3-4cf7-8cab-13281b8aca09
Enter the XPath to retrieve metadata: .//gmd:distributionFormat
```

#### Retrieve the digital transfer options

The command is the same as above but with the following xpath:

`.//gmd:MD_DigitalTransferOptions`

#### Retrieve the Keywords associated with the record

.//gmd:descriptiveKeywords

#### Retrieve the internal identifier of a record

Use the **retrieve_record_internal-Ref.py** script with a csv containing the list of uuids respecting the following structure:

```csv
geocat_uuid
<uuid>
<uuid>
```
#### Add WMS service information as Online Resources

1. Copy and modify the update the updates.yml.example file

`cp updates.yml.example updates.yml`

2. Run the script update-OnlineResources.py

`python3 update-OnlineResources.py`

#### Update the distribution format

1. Update the file updates.yml as follow (e.g. for a WMS) :

```yml
updates:
  - uuid: <record_uuid>
    distributionFormat: 
      - OGC Web Map Service (WMS)
```

2. Run the script Put-distributionFormat.py
