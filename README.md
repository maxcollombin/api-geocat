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

`.//gmd:MD_DigitalTransferOptions//gmd:onLine//gmd:CI_OnlineResource`

[!NOTE]
> Extra paths such as `.//gmd:onLine//gmd:CI_OnlineResource` but are not really useful




url correcte


https://geocat-int.dev.bgdi.ch/geonetwork/srv/api/records/batchediting?uuids=c885c51c-a7c3-4cf7-8cab-13281b8aca09


json body

```json
[
    {
      "xpath": ".//gmd:MD_DigitalTransferOptions",
      "value": "<gmd:onLine xmlns:gmd=\"http://www.isotc211.org/2005/gmd\" xmlns:gco=\"http://www.isotc211.org/2005/gco\" xmlns:che=\"http://www.geocat.ch/2008/che\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n  <gmd:CI_OnlineResource>\n    <gmd:linkage xsi:type=\"che:PT_FreeURL_PropertyType\">\n      <gmd:URL>https://sit.vs.ch/arcgis/services/MO/MapServer/WMSServer?SERVICE=WMS&amp;VERSION=1.3.0&amp;REQUEST=GetCapabilities</gmd:URL>\n      <che:PT_FreeURL>\n        <che:URLGroup>\n          <che:LocalisedURL locale=\"#FR\">https://sit.vs.ch/arcgis/services/MO/MapServer/WMSServer?SERVICE=WMS&amp;VERSION=1.3.0&amp;REQUEST=GetCapabilities</che:LocalisedURL>\n        </che:URLGroup>\n        <che:URLGroup>\n          <che:LocalisedURL locale=\"#DE\">https://sit.vs.ch/arcgis/services/AV/MapServer/WMSServer?SERVICE=WMS&amp;VERSION=1.3.0&amp;REQUEST=GetCapabilities</che:LocalisedURL>\n        </che:URLGroup>\n      </che:PT_FreeURL>\n    </gmd:linkage>\n    <gmd:protocol>\n      <gco:CharacterString>OGC:WMS</gco:CharacterString>\n    </gmd:protocol>\n    <gmd:name xsi:type=\"gmd:PT_FreeText_PropertyType\">\n      <gco:CharacterString>0</gco:CharacterString>\n      <gmd:PT_FreeText>\n        <gmd:textGroup>\n          <gmd:LocalisedCharacterString locale=\"#FR\">0</gmd:LocalisedCharacterString>\n        </gmd:textGroup>\n        <gmd:textGroup>\n          <gmd:LocalisedCharacterString locale=\"#DE\">0</gmd:LocalisedCharacterString>\n        </gmd:textGroup>\n      </gmd:PT_FreeText>\n    </gmd:name>\n    <gmd:description xsi:type=\"gmd:PT_FreeText_PropertyType\">\n      <gco:CharacterString>Lots</gco:CharacterString>\n      <gmd:PT_FreeText>\n        <gmd:textGroup>\n          <gmd:LocalisedCharacterString locale=\"#FR\">Lots</gmd:LocalisedCharacterString>\n        </gmd:textGroup>\n        <gmd:textGroup>\n          <gmd:LocalisedCharacterString locale=\"#DE\">Los</gmd:LocalisedCharacterString>\n        </gmd:textGroup>\n      </gmd:PT_FreeText>\n    </gmd:description>\n  </gmd:CI_OnlineResource>\n</gmd:onLine>",
      "condition": ""
    }
  ]
  
```

**To do:**

1. Tester le multilangues
2. Tester patch ? pour éviter de remplacer tous les liens existants



[
  {
    "xpath": ".//gmd:MD_DigitalTransferOptions//gmd:onLine",
    "value": "<gmd:CI_OnlineResource xmlns:gmd=\"http://www.isotc211.org/2005/gmd\" xmlns:gco=\"http://www.isotc211.org/2005/gco\" xmlns:che=\"http://www.geocat.ch/2008/che\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n    <gmd:linkage xsi:type=\"che:PT_FreeURL_PropertyType\">\n      <gmd:URL>https://sit.vs.ch/arcgis/services/MO/MapServer/WMSServer?SERVICE=WMS&amp;VERSION=1.3.0&amp;REQUEST=GetCapabilities</gmd:URL>\n      <che:PT_FreeURL>\n        <che:URLGroup>\n          <che:LocalisedURL locale=\"#FR\">https://sit.vs.ch/arcgis/services/MO/MapServer/WMSServer?SERVICE=WMS&amp;VERSION=1.3.0&amp;REQUEST=GetCapabilities</che:LocalisedURL>\n        </che:URLGroup>\n        <che:URLGroup>\n          <che:LocalisedURL locale=\"#DE\">https://sit.vs.ch/arcgis/services/AV/MapServer/WMSServer?SERVICE=WMS&amp;VERSION=1.3.0&amp;REQUEST=GetCapabilities</che:LocalisedURL>\n        </che:URLGroup>\n        <che:URLGroup>\n          <che:LocalisedURL locale=\"#IT\">https://sit.vs.ch/arcgis/services/MO/MapServer/WMSServer?SERVICE=WMS&amp;VERSION=1.3.0&amp;REQUEST=GetCapabilities</che:LocalisedURL>\n        </che:URLGroup>\n        <che:URLGroup>\n          <che:LocalisedURL locale=\"#EN\">https://sit.vs.ch/arcgis/services/MO/MapServer/WMSServer?SERVICE=WMS&amp;VERSION=1.3.0&amp;REQUEST=GetCapabilities</che:LocalisedURL>\n        </che:URLGroup>\n        <che:URLGroup>\n          <che:LocalisedURL locale=\"#RM\">https://sit.vs.ch/arcgis/services/MO/MapServer/WMSServer?SERVICE=WMS&amp;VERSION=1.3.0&amp;REQUEST=GetCapabilities</che:LocalisedURL>\n        </che:URLGroup>\n      </che:PT_FreeURL>\n    </gmd:linkage>\n    <gmd:protocol>\n      <gco:CharacterString>OGC:WMS</gco:CharacterString>\n    </gmd:protocol>\n    <gmd:name xsi:type=\"gmd:PT_FreeText_PropertyType\">\n      <gco:CharacterString>0</gco:CharacterString>\n      <gmd:PT_FreeText>\n        <gmd:textGroup>\n          <gmd:LocalisedCharacterString locale=\"#FR\">0</gmd:LocalisedCharacterString>\n        </gmd:textGroup>\n        <gmd:textGroup>\n          <gmd:LocalisedCharacterString locale=\"#DE\">0</gmd:LocalisedCharacterString>\n        </gmd:textGroup>\n      </gmd:PT_FreeText>\n    </gmd:name>\n    <gmd:description xsi:type=\"gmd:PT_FreeText_PropertyType\">\n      <gco:CharacterString>Lots</gco:CharacterString>\n      <gmd:PT_FreeText>\n        <gmd:textGroup>\n          <gmd:LocalisedCharacterString locale=\"#FR\">Lots</gmd:LocalisedCharacterString>\n        </gmd:textGroup>\n        <gmd:textGroup>\n          <gmd:LocalisedCharacterString locale=\"#DE\">Los</gmd:LocalisedCharacterString>\n        </gmd:textGroup>\n      </gmd:PT_FreeText>\n    </gmd:description>\n  </gmd:CI_OnlineResource>",
    "condition": ""
  }
]