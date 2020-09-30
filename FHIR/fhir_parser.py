from typing import List
import xml.etree.ElementTree as ET

_ns = {"ns0": "http://hl7.org/fhir"}


def get_patient_ids_from_bundle(bundle: ET.Element) -> List[str]:
    ids = []
    entries = _split_bundle(bundle)
    for entry in entries:
        resource = _extract_resource_from_entry(entry)
        resource_type = _get_resource_type(resource)
        id_extractor = _resource_to_extractor_mapping[resource_type]
        ids.append(id_extractor(resource))

    return ids


def build_unions(fhir_query_ids_a: List[str], fhir_query_ids_b: List[str]) -> List[str]:
    # Ugly but I couldn't be bothered to change the signatures
    return list(set(fhir_query_ids_a).union(set(fhir_query_ids_b)))


def build_intersections(fhir_query_ids_a: List[str], fhir_query_ids_b: List[str]) -> List[str]:
    return list(set(fhir_query_ids_a).intersection(set(fhir_query_ids_b)))


def build_result_set_from_query_results(fhir_query_results: List[List[List[str]]]) -> List[str]:
    results = []
    for fhir_cnf_results in fhir_query_results:
        unions = []
        for fhir_disjunction_results in fhir_cnf_results:
            unions = build_unions(unions, fhir_disjunction_results)
        results = build_intersections(results, unions)
    return results


def _get_resource_type(resource):
    tag = resource.tag

    # Remove namespace for easier lookup
    ns_split = tag.split("}")
    if len(ns_split) > 1:
        tag = ns_split[1]
    return tag.lower()


def _extract_ids_from_patient(patient: ET.Element) -> str:
    x_identifier = patient.find("./ns0:identifier", _ns)
    x_identifier_value = x_identifier.find("./ns0:value", _ns)
    return x_identifier_value.attrib["value"]


def _extract_ids_from_observation(observation: ET.Element) -> str:
    x_identifier = observation.find(".ns0:subject/ns0:identifier", _ns)
    x_identifier_value = x_identifier.find("./ns0:value", _ns)
    return x_identifier_value.attrib["value"]


def _extract_ids_from_encounter(encounter: ET.Element) -> str:
    # TODO
    pass


def _split_bundle(bundle: ET.Element) -> List[ET.Element]:
    entries = bundle.findall("./ns0:entry", _ns)
    return entries


def _extract_resource_from_entry(entry: ET.Element) -> ET.Element:
    """
    :param entry: <entry></entry>
    :return: the element found inside the <resource></resource> in the entry
    """
    resource = list(entry.find("./ns0:resource", _ns))[0]
    return resource


_resource_to_extractor_mapping = {
    "patient": _extract_ids_from_patient,
    "observation": _extract_ids_from_observation,
    "encounter": _extract_ids_from_encounter,
}
