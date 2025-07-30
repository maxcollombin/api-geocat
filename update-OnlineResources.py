import requests
import yaml
from lxml import etree
from authenticate import authenticate
from Generate_OnlineResource_XML import Generate_OnLineResource_XML
from retrieve_record_xpath import retrieve_metadata_by_xpath

# Charger les configurations YAML
with open("updates.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Authentification
session, server = authenticate()

# Itérer sur chaque mise à jour
for entry in config["updates"]:
    uuid = entry["uuid"]

    # ✅ Charger les éléments existants
    xpath = ".//gmd:MD_DigitalTransferOptions"
    existing_elements = retrieve_metadata_by_xpath(uuid, xpath)

    # ✅ Appel correct avec deux arguments
    xml_snippet = Generate_OnLineResource_XML(entry, existing_elements)

    json_body = [
        {
            "xpath": xpath,
            "value": xml_snippet,
            "condition": ""
        }
    ]

    params = {
        'uuids': uuid,
        'updateDateStamp': 'true',
        'rejectIfInvalid': 'true'
    }

    try:
        response = session.put(
            f"{server}/records/batchediting",
            params=params,
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'X-XSRF-TOKEN': session.cookies.get('XSRF-TOKEN')
            },
            json=json_body
        )

        if response.ok:
            print(f"✅ UUID {uuid} : mise à jour réussie")
        else:
            print(f"❌ UUID {uuid} : erreur HTTP {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        print(f"❌ UUID {uuid} : erreur de connexion - {e}")
