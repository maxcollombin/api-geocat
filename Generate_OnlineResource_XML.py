import yaml
from lxml import etree
from retrieve_record_xpath import retrieve_metadata_by_xpath
import difflib
import os

NSMAP = {
    'gmd': "http://www.isotc211.org/2005/gmd",
    'gco': "http://www.isotc211.org/2005/gco",
    'che': "http://www.geocat.ch/2008/che",
    'xsi': "http://www.w3.org/2001/XMLSchema-instance"
}

def el(tag, ns='gmd', **kwargs):
    return etree.Element(f"{{{NSMAP[ns]}}}{tag}", **kwargs)

def text_el(tag, text, ns='gco'):
    e = el(tag, ns)
    e.text = str(text)
    return e

def Generate_LocalisedElement(tag, default_text, translations):
    parent = el(tag)
    parent.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = "gmd:PT_FreeText_PropertyType"
    parent.append(text_el("CharacterString", default_text))
    pt_free_text = el("PT_FreeText")
    for locale, text in translations.items():
        text_group = el("textGroup")
        loc_el = el("LocalisedCharacterString", locale=locale)
        loc_el.text = str(text)
        text_group.append(loc_el)
        pt_free_text.append(text_group)
    parent.append(pt_free_text)
    return parent

def load_params_from_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def Generate_OnLineResource_XML(params, existing_elements):
    """
    Génère un élément <gmd:onLine> et l'ajoute dans un bloc MD_DigitalTransferOptions.
    """
    root = etree.fromstring(existing_elements[-1]) if existing_elements else el("MD_DigitalTransferOptions", ns="gmd", nsmap=NSMAP)

    online = el("onLine")
    ci_online = el("CI_OnlineResource")

    # linkage
    linkage = el("linkage")
    linkage.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = "che:PT_FreeURL_PropertyType"
    linkage.append(text_el("URL", params['URL']['fr'], ns="gmd"))

    pt_free_url = el("PT_FreeURL", ns="che")
    for locale, url in [("#FR", params['URL']['fr']), ("#DE", params['URL']['de'])]:
        group = el("URLGroup", ns="che")
        local_url = el("LocalisedURL", ns="che", locale=locale)
        local_url.text = url
        group.append(local_url)
        pt_free_url.append(group)
    linkage.append(pt_free_url)
    ci_online.append(linkage)

    # protocol
    protocol = el("protocol")
    service_type = params.get('type', 'WMS').upper()  # Par défaut, WMS
    protocol.append(text_el("CharacterString", f"OGC:{service_type}"))
    ci_online.append(protocol)

    # name
    name_elem = Generate_LocalisedElement("name", params['name']['fr'], {
        "#FR": params['name']['fr'],
        "#DE": params['name']['de']
    })
    ci_online.append(name_elem)

    # description
    desc_elem = Generate_LocalisedElement("description", params['description']['fr'], {
        "#FR": params['description']['fr'],
        "#DE": params['description']['de']
    })
    ci_online.append(desc_elem)

    # function
    function = el("function")
    function_code = el("CI_OnLineFunctionCode")
    function_code.attrib["codeList"] = "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/ML_gmxCodelists.xml#CI_OnLineFunctionCode"
    function_code.attrib["codeListValue"] = "download"
    function.append(function_code)
    ci_online.append(function)

    online.append(ci_online)
    root.append(online)

    return etree.tostring(root, pretty_print=True, encoding='unicode')

def test_xml_generation():
    params_yaml = load_params_from_yaml('updates.yml')
    update = params_yaml['updates'][0]
    uuid = update['uuid']
    xpath = ".//gmd:MD_DigitalTransferOptions"

    existing_elements = retrieve_metadata_by_xpath(uuid, xpath)
    generated_xml = Generate_OnLineResource_XML(update, existing_elements)

    print("=== XML généré ===")
    print(generated_xml)

if __name__ == "__main__":
    test_xml_generation()
