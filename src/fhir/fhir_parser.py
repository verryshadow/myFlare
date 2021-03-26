import xml.etree.ElementTree as Etree
from typing import List, Set

from fhir.namespace import ns


def get_patient_ids_from_bundle(bundle: Etree.Element) -> Set[str]:
    """
    Extracts all patient ids from the entities contained in a bundle

    :param bundle: FHIR-bundle given in response to a search containing patients observations and encounters
    :return: list of patient ids
    """
    ids = set()
    entries = _split_bundle(bundle)
    for entry in entries:
        resource = _extract_resource_from_entry(entry)
        resource_type = _get_resource_type(resource)
        id_extractor = _resource_to_extractor_mapping[resource_type]
        extracted_id = id_extractor(resource)
        if extracted_id:
            ids = ids.union([extracted_id])

    return ids


def _get_resource_type(x_resource: Etree.Element) -> str:
    """
    Retrieves the entity type (patient, observation ...) from a resource

    :param x_resource: <resource></resource>
    :return: the type of entity contained in the resource
    """
    tag = x_resource.tag

    # Remove namespace for easier lookup
    ns_split = tag.split("}")
    if len(ns_split) > 1:
        tag = ns_split[1]

    return tag.lower()


def _extract_id_from_patient(patient: Etree.Element) -> str:
    x_id = patient.find("./ns0:id", ns)

    if x_id is None:
        x_identifier = patient.find("./ns0:identifier", ns)
        x_identifier_value = x_identifier.find("./ns0:value", ns)
        x_id_value = x_identifier_value.attrib["value"]
    else:
        x_id_value = x_id.attrib["value"]
    return x_id_value


def _extract_id_from_observation(observation: Etree.Element) -> str:
    # get reference https://www.hl7.org/fhir/references.html#Reference
    x_reference_element = observation.find(".ns0:subject", ns)

    # Extract all tags possibly containing values
    x_identifier = x_reference_element.find("./ns0:identifier", ns)
    x_reference = x_reference_element.find("./ns0:reference", ns)
    x_type = x_reference_element.find("./ns0:type", ns)

    patient_id = None
    if x_identifier is not None:
        x_value = x_identifier.find("./ns0:value", ns)
        patient_id = x_value.attrib["value"]
    # TODO: Proper reference handling by executing FHIR query
    elif x_reference is not None:
        patient_id = x_reference.attrib["value"].split("/")[-1]

    return patient_id

def _extract_id_from_condition(condition: Etree.Element) -> str:
    # get reference https://www.hl7.org/fhir/references.html#Reference
    x_reference_element = condition.find(".ns0:subject", ns)

    # Extract all tags possibly containing values
    x_identifier = x_reference_element.find("./ns0:identifier", ns)
    x_reference = x_reference_element.find("./ns0:reference", ns)
    x_type = x_reference_element.find("./ns0:type", ns)

    patient_id = None
    if x_identifier is not None:
        x_value = x_identifier.find("./ns0:value", ns)
        patient_id = x_value.attrib["value"]
    # TODO: Proper reference handling by executing FHIR query
    elif x_reference is not None:
        patient_id = x_reference.attrib["value"].split("/")[-1]

    return patient_id

def _extract_id_from_encounter(encounter: Etree.Element) -> str:
    # TODO implement
    pass


def _split_bundle(bundle: Etree.Element) -> List[Etree.Element]:
    """
    Split the bundle and return all entry tags in the bundle

    :param bundle: FHIR bundle
    :return: entries contained in the bundle
    """
    entries = bundle.findall("./ns0:entry", ns)
    return entries


def _extract_resource_from_entry(entry: Etree.Element) -> Etree.Element:
    """
    :param entry: <entry></entry>
    :return: the element found inside the <resource></resource> in the entry
    """
    resource = list(entry.find("./ns0:resource", ns))[0]
    return resource


_resource_to_extractor_mapping = {
    "patient": _extract_id_from_patient,
    "observation": _extract_id_from_observation,
    "encounter": _extract_id_from_encounter,
    "condition": _extract_id_from_condition
}


def build_result_set_from_query_results(fhir_query_results: List[List[List[Set[str]]]]) -> List[str]:
    """
    Resolves the CNF given to it in form of all the FHIR-queries belonging to a request

    :param fhir_query_results:
    All ids from the FHIR-query results given in the format of a CNF, where a single query consists of a List of Sets
    of ids, where each set represents a single page from the query result
    :return: The resolved CNF
    """
    panels = list()
    # Iterate over all panels from the request
    for fhir_cnf_results in fhir_query_results:
        items = list()
        # Iterate over all items from the panel
        for fhir_disjunction_results in fhir_cnf_results:
            # Items are translated into one FHIR-query, an executed FHIR-query consists of pages, build union of it
            items.append(set.union(*fhir_disjunction_results))
        if len(items) != 0:
            panels.append(set.union(*items))
    if len(panels) == 0:
        return []
    return list(set.intersection(*panels))
