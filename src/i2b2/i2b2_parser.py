import xml.etree.ElementTree as ET
from typing import List
import json

with open("I2B2/mapping.json") as mapping:
    config = json.load(mapping)


def lookup(item_key: str) -> List[dict]:
    try:
        return config[item_key]
    except KeyError as e:
        # TODO: Properly handle errors
        return []


def parse_i2b2_query_xml_string(xml: str) -> List[List[dict]]:
    root = ET.fromstring(xml)
    panels = []

    # Iterate over panels
    ns = {'ns6': 'http://www.i2b2.org/xsd/hive/msg/1.1/', 'ns4': 'http://www.i2b2.org/xsd/cell/crc/psm/1.1/'}
    for x_panel in root.findall('./query_definition/panel', ns):
        panel = []

        # Iterate over all items in the panel
        for x_item in x_panel.findall('./item'):
            # Process item key
            x_item_key = x_item.find("item_key")
            if x_item_key is None:
                continue
            equivalents = lookup(x_item_key.text)

            for equivalent in equivalents:
                if "valueParam" in equivalent:
                    x_constrain_by_value = x_item.find("constrain_by_value")
                    if x_constrain_by_value is None:
                        continue

                    # Parse value constraints
                    x_value_type = x_constrain_by_value.find("value_type")
                    x_value_operator = x_constrain_by_value.find("value_operator")
                    x_value_constraint = x_constrain_by_value.find("value_constraint")
                    x_value_unit_of_measure = x_constrain_by_value.find("value_unit_of_measure")
                    constrain_by_value = {}
                    if x_value_type is not None:
                        constrain_by_value["value_type"] = x_value_type.text
                    if x_value_operator is not None:
                        constrain_by_value["value_operator"] = x_value_operator.text
                    if x_value_constraint is not None:
                        constrain_by_value["value_constraint"] = x_value_constraint.text
                    if x_value_unit_of_measure is not None:
                        constrain_by_value["value_unit_of_measure"] = x_value_unit_of_measure.text

                    equivalent["constrain_by_value"] = constrain_by_value

            panel = panel + equivalents

        if not panel == []:
            panels.append(panel)

    return panels


def main():
    with open('i2b2_example.xml', 'r') as file:
        i2b2_example = parse_i2b2_query_xml_string(file.read())
    print(i2b2_example)


if __name__ == "__main__":
    main()
