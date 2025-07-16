import requests
from dotenv import load_dotenv
import os
from lxml import etree

# Remove any existing environment variables
os.environ.clear()
# Load environment variables from the .env file
load_dotenv()

# Access environment variables
api_url = os.getenv("GEOCAT_URL")
user = os.getenv("GEOCAT_USERNAME")
pwd = os.getenv("GEOCAT_PASSWORD")

def retrieve_metadata_by_xpath(uuid, xpath):
    """
    Retrieve metadata elements from a GeoNetwork record based on the given XPath.

    Args:
        uuid (str): The UUID of the record.
        xpath (str): The XPath to locate metadata elements.

    Returns:
        list: A list of XML strings for the matching elements.
    """
    session = requests.Session()
    session.auth = (user, pwd)

    item_url = f"{api_url}/records/{uuid}"
    print(f"Generated URL: {item_url}")  # Display the generated URL

    try:
        response = session.get(item_url, headers={"Accept": "application/xml"})
        if response.status_code == 200:
            xml_content = response.text
            root = etree.fromstring(xml_content.encode('utf-8'))
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
                return [etree.tostring(element, pretty_print=True, encoding='unicode') for element in elements]
            else:
                print(f"No elements found for XPath: {xpath}")
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response content:", response.text)
    except requests.exceptions.SSLError as e:
        print("SSL Error:", e)
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
    except etree.XMLSyntaxError as e:
        print("XML Parsing Error:", e)

if __name__ == "__main__":
    record_uuid = input("Enter the UUID of the record: ").strip()
    xpath = input("Enter the XPath to retrieve metadata: ").strip()
    metadata_elements = retrieve_metadata_by_xpath(record_uuid, xpath)
    if metadata_elements:
        output_dir = "responses"
        os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
        output_file = f"{output_dir}/metadata_{record_uuid}.xml"
        with open(output_file, "w", encoding="utf-8") as file:
            for element in metadata_elements:
                file.write(element + "\n")
        print(f"Metadata information saved to {output_file}")