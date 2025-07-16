import yaml
from lxml import etree

def load_params_from_yaml(file_path):
    with open(file_path, mode='r', encoding='utf-8') as yamlfile:
        return yaml.safe_load(yamlfile)

def Generate_OnLineResource_XML(params):
    NSMAP = {
        'gmd': "http://www.isotc211.org/2005/gmd",
        'gco': "http://www.isotc211.org/2005/gco",
        'che': "http://www.geocat.ch/2008/che",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance"
    }

    def el(tag, ns='gmd', **kwargs):
        """
        Crée un élément XML avec le namespace spécifié.
        """
        return etree.Element(f"{{{NSMAP[ns]}}}{tag}", **kwargs)

    def text_el(tag, text, ns='gco'):
        """
        Crée un élément XML avec du texte.
        """
        e = el(tag, ns)
        e.text = str(text)
        return e

    def Generate_LocalisedElement(tag, default_text, translations):
        """
        Génère un élément XML localisé avec un CharacterString par défaut et des LocalisedCharacterString.
        """
        parent = el(tag)
        parent.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = "gmd:PT_FreeText_PropertyType"

        # Ajouter le CharacterString par défaut
        parent.append(text_el("CharacterString", default_text))

        # Ajouter les traductions localisées
        pt_free_text = el("PT_FreeText")
        for locale, text in translations.items():
            text_group = el("textGroup")
            loc_el = el("LocalisedCharacterString", locale=locale)
            loc_el.text = str(text)
            text_group.append(loc_el)
            pt_free_text.append(text_group)

        parent.append(pt_free_text)
        return parent

    # gmd:onLine
    online = el("onLine", ns="gmd", nsmap=NSMAP)
    ci_online = el("CI_OnlineResource")

    # linkage
    linkage = el("linkage")
    linkage.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = "che:PT_FreeURL_PropertyType"

    # gmd:URL
    url_elem = text_el("URL", params['URL']['fr'], ns="gmd")
    linkage.append(url_elem)

    # che:PT_FreeURL
    pt_free_url = el("PT_FreeURL", ns="che")
    for locale, url in [("#FR", params['URL']['fr']), ("#DE", params['URL']['de'])]:
        url_group = el("URLGroup", ns="che")
        local_url = el("LocalisedURL", ns="che", locale=locale)
        local_url.text = str(url)
        url_group.append(local_url)
        pt_free_url.append(url_group)

    linkage.append(pt_free_url)
    ci_online.append(linkage)

    # gmd:protocol
    protocol = el("protocol")
    protocol.append(text_el("CharacterString", "OGC:WMS"))
    ci_online.append(protocol)

    # gmd:name (localisé)
    name_translations = {
        "#FR": params['name']['fr'],
        "#DE": params['name']['de']
    }
    name_elem = Generate_LocalisedElement("name", params['name']['fr'], name_translations)
    ci_online.append(name_elem)

    # gmd:description (localisé)
    description_translations = {
        "#FR": params['description']['fr'],
        "#DE": params['description']['de']
    }
    desc_elem = Generate_LocalisedElement("description", params['description']['fr'], description_translations)
    ci_online.append(desc_elem)

    online.append(ci_online)
    return etree.tostring(online, pretty_print=False, encoding="unicode")

def test_xml_generation():
    params_yaml = load_params_from_yaml('params.yml')
    print("=== XML généré depuis YAML ===")
    print(Generate_OnLineResource_XML(params_yaml))

if __name__ == "__main__":
    test_xml_generation()
