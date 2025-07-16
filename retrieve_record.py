import requests
from dotenv import load_dotenv
import os
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

# Charger des informations d'environnement depuis le fichier .env
load_dotenv()

# Accéder aux variables
api_url = os.getenv("GEOCAT_URL")
user = os.getenv("GEOCAT_USERNAME")
pwd = os.getenv("GEOCAT_PASSWORD")

def retrieve_record(uuid):
    session = requests.Session()
    session.auth = (user, pwd)

    item_url = f"{api_url}/records/{uuid}"
    print(f"Generated URL: {item_url}")  # Affiche l'URL générée

    try:
        response = session.get(item_url, headers={"Accept": "application/json"})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response content:", response.text)
    except requests.exceptions.SSLError as e:
        print("SSL Error:", e)
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)

if __name__ == "__main__":
    record_uuid = input("Enter the UUID of the record: ")
    record_info = retrieve_record(record_uuid)
    if record_info:
        output_file = f"responses/record_{record_uuid}.xml"
        with open(output_file, "w", encoding="utf-8") as file:
            xml_data = dicttoxml(record_info, custom_root='record', attr_type=False)
            pretty_xml = parseString(xml_data).toprettyxml(indent="  ")
            file.write(pretty_xml)
        print(f"Record information saved to {output_file}")