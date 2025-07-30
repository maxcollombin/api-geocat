import requests
import yaml
from authenticate import authenticate
from Generate_distributionFormat_XML import Generate_distributionFormat_XML

def put_distribution_format():
    with open("updates.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    session, server = authenticate()

    for entry in config["updates"]:
        uuid = entry["uuid"]

        # Générer les nouvelles balises <gmd:distributionFormat>
        try:
            # generated_fragment = Generate_distributionFormat_XML(entry)
            generated_fragment = f"<gn_add>{Generate_distributionFormat_XML(entry)}</gn_add>"
        except Exception as e:
            print(f"❌ UUID {uuid} : erreur lors de la génération du fragment XML - {e}")
            continue

        json_body = [
            {
                "xpath": ".//gmd:MD_Distribution",
                "value": generated_fragment,
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

if __name__ == "__main__":
    put_distribution_format()
