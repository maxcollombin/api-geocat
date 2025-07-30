from lxml import etree
import yaml

NSMAP = {
    'gmd': "http://www.isotc211.org/2005/gmd",
    'gco': "http://www.isotc211.org/2005/gco",
    'che': "http://www.geocat.ch/2008/che",
    'xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'xlink': "http://www.w3.org/1999/xlink",
    'gml': "http://www.opengis.net/gml/3.2",
}

def el(tag, ns='gmd', **kwargs):
    return etree.Element(f"{{{NSMAP[ns]}}}{tag}", nsmap=NSMAP if ns == 'gmd' else None, **kwargs)

def text_el(tag, text, ns='gco'):
    e = el(tag, ns)
    e.text = str(text)
    return e

def Generate_distributionFormat_XML(params):
    """
    Génère une ou plusieurs balises <gmd:distributionFormat> à partir des paramètres YAML.
    Retourne une chaîne XML avec les nouvelles balises.
    """
    fragments = []

    for format_name in params['distributionFormat']:
        # Déterminer le xlink:href en fonction du format
        if format_name == "OGC Web Feature Service (WFS)":
            xlink_href = (
                "local://srv/api/registries/entries/80779add-0cf2-4c66-913b-0cf5ca7f645e"
                "?lang=fre,ger,ita,eng,roh&schema=iso19139.che"
            )
        elif format_name == "OGC Web Map Service (WMS)":
            xlink_href = (
                "local://srv/api/registries/entries/6c284fc7-fb99-4bb6-8e14-35466d8096d6"
                "?lang=fre,ger,ita,eng,roh&schema=iso19139.che"
            )
        else:
            raise ValueError(f"Format inconnu : {format_name}")

        # Création de la balise <gmd:distributionFormat>
        distribution_format = el("distributionFormat")
        distribution_format.attrib["{http://www.w3.org/1999/xlink}href"] = xlink_href

        md_format = el("MD_Format")
        name = el("name")
        name.append(text_el("CharacterString", format_name))
        md_format.append(name)

        version = el("version", ns="gco")
        version.attrib["{http://www.isotc211.org/2005/gco}nilReason"] = "unknown"
        md_format.append(version)

        distribution_format.append(md_format)
        fragments.append(distribution_format)

    return "\n".join([etree.tostring(frag, pretty_print=True, encoding="unicode") for frag in fragments])

# Test local
if __name__ == "__main__":
    with open("updates.yml", "r", encoding="utf-8") as f:
        params_yaml = yaml.safe_load(f)

    xml_fragment = Generate_distributionFormat_XML(params_yaml['updates'][0])
    print("=== Fragment XML généré ===")
    print(xml_fragment)