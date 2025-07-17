import os
import requests
from lxml import etree
from authenticate import authenticate  # Importer la fonction authenticate

def retrieve_metadata_by_xpath(uuid, xpath):
    """
    Retrieve metadata elements from a GeoNetwork record based on the given XPath.

    Args:
        uuid (str): The UUID of the record.
        xpath (str): The XPath to locate metadata elements.

    Returns:
        list: A list of XML strings for the matching elements.
    """
    # Utiliser la session authentifiée et l'URL de base
    try:
        session, api_url = authenticate()
    except ValueError as e:
        print(f"❌ Erreur d'authentification : {e}")
        return []

    item_url = f"{api_url}/records/{uuid}"
    print(f"🔗 URL utilisée: {item_url}")

    try:
        response = session.get(item_url, headers={"Accept": "application/xml"})
        if response.status_code == 200:
            root = etree.fromstring(response.content)
            namespaces = {
                'gmd': 'http://www.isotc211.org/2005/gmd',
                'gco': 'http://www.isotc211.org/2005/gco',
                'che': 'http://www.geocat.ch/2008/che',
                'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                'xlink': 'http://www.w3.org/1999/xlink',
                'gml': 'http://www.opengis.net/gml/3.2',
            }
            elements = root.xpath(xpath, namespaces=namespaces)
            if elements:
                return [etree.tostring(el, pretty_print=True, encoding='unicode') for el in elements]
            else:
                print(f"⚠️ Aucun élément trouvé pour le XPath : {xpath}")
        else:
            print(f"❌ Requête échouée (status {response.status_code})")
            print("Réponse :", response.text)
    except requests.exceptions.RequestException as e:
        print("🔌 Erreur réseau :", e)
    except etree.XMLSyntaxError as e:
        print("🧩 Erreur XML :", e)

if __name__ == "__main__":
    record_uuid = input("UUID du record : ").strip()
    xpath = input("XPath à extraire : ").strip()
    elements = retrieve_metadata_by_xpath(record_uuid, xpath)
    if elements:
        output_dir = "responses"
        os.makedirs(output_dir, exist_ok=True)
        output_path = f"{output_dir}/metadata_{record_uuid}.xml"
        with open(output_path, "w", encoding="utf-8") as f:
            for el in elements:
                f.write(el + "\n")
        print(f"📄 Éléments sauvegardés dans {output_path}")