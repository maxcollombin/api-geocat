import os
import csv
import requests
from lxml import etree
from authenticate import authenticate  # Importer la fonction authenticate

def retrieve_character_string_values(uuid):
    """
    Retrieve the values of <gco:CharacterString> from a GeoNetwork record based on the hierarchical XPath.

    Args:
        uuid (str): The UUID of the record.

    Returns:
        list: A list of values for <gco:CharacterString>.
    """
    # XPath précis pour respecter la hiérarchie
    xpath = ".//gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString"

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
            # Extraire uniquement les valeurs de <gco:CharacterString> respectant la hiérarchie
            character_string_values = root.xpath(xpath, namespaces=namespaces)
            if character_string_values:
                return [value.text for value in character_string_values]
            else:
                print(f"⚠️ Aucun élément trouvé pour le XPath : {xpath}")
                return []
        else:
            print(f"❌ Requête échouée (status {response.status_code})")
            print("Réponse :", response.text)
            return []
    except requests.exceptions.RequestException as e:
        print("🔌 Erreur réseau :", e)
        return []
    except etree.XMLSyntaxError as e:
        print("🧩 Erreur XML :", e)
        return []

if __name__ == "__main__":
    input_file = input("Chemin du fichier CSV contenant les UUIDs : ").strip()
    output_file = os.path.join("responses", "references-internes.csv")

    # Vérifier si le fichier d'entrée existe
    if not os.path.exists(input_file):
        print(f"❌ Le fichier {input_file} n'existe pas.")
        exit(1)

    # Lire les UUIDs depuis le fichier CSV
    uuids = []
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Ignorer l'en-tête
        uuids = [row[0] for row in reader]

    # Extraire les valeurs et écrire dans le fichier de sortie
    os.makedirs("responses", exist_ok=True)
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["geocat_uuid", "ref_interne"])  # Écrire l'en-tête

        for uuid in uuids:
            values = retrieve_character_string_values(uuid)
            if values:
                for value in values:
                    writer.writerow([uuid, value])
            else:
                writer.writerow([uuid, ""])

    print(f"📄 Résultats sauvegardés dans {output_file}")