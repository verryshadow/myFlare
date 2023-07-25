# Manual Query Translate

## Note
- curate json was active


## Example and lookup
```bash
[[["Observation?code=http://loinc.org|76689-9&value-concept=http://hl7.org/fhir/administrative-gender|female"]], []]
```

```bash
[[inclusion],[exclusion]]
```

```bash
[[["ressource?searchTerm=systemURL|code&searchTerm=systemURL|code"]],[]]
```


--------


## 1-acehemmer_code.json

### script
```json
curl --location --request POST 'http://localhost:5111/query-translate' \
--header 'Content-Type: codex/json' \
--header 'Accept: internal/json' \
--data-raw '{
    "exclusionCriteria": [],
    "inclusionCriteria": [
        {
            "termCode": {
                "code": "41549009",
                "display": "",
                "system": "http://snomed.info/sct"
            }
        }
    ],
    "version": "http://to_be_decided.com/draft-1/schema#"
}'
```

### expected
```bash
[[["MedicationStatement?code=http://snomed.info/sct|41549009"]],[]]
```

### output
```bash
[[["MedicationStatement?code=http://snomed.info/sct|41549009"]],[]]
[[["MedicationStatement?code=http://snomed.info/sct|41549009,http://fhir.de/CodeSystem/dimdi/atc|C09A,http://fhir.de/CodeSystem/dimdi/atc|C09AA,http://fhir.de/CodeSystem/dimdi/atc|C09AA01,http://fhir.de/CodeSystem/dimdi/atc|C09AA02,http://fhir.de/CodeSystem/dimdi/atc|C09AA03,http://fhir.de/CodeSystem/dimdi/atc|C09AA04,http://fhir.de/CodeSystem/dimdi/atc|C09AA05,http://fhir.de/CodeSystem/dimdi/atc|C09AA06,http://fhir.de/CodeSystem/dimdi/atc|C09AA07,http://fhir.de/CodeSystem/dimdi/atc|C09AA08,http://fhir.de/CodeSystem/dimdi/atc|C09AA09,http://fhir.de/CodeSystem/dimdi/atc|C09AA10,http://fhir.de/CodeSystem/dimdi/atc|C09AA11,http://fhir.de/CodeSystem/dimdi/atc|C09AA12,http://fhir.de/CodeSystem/dimdi/atc|C09AA13,http://fhir.de/CodeSystem/dimdi/atc|C09AA14,http://fhir.de/CodeSystem/dimdi/atc|C09AA15,http://fhir.de/CodeSystem/dimdi/atc|C09AA16,http://fhir.de/CodeSystem/dimdi/atc|C09B,http://fhir.de/CodeSystem/dimdi/atc|C09BA,http://fhir.de/CodeSystem/dimdi/atc|C09BA01,http://fhir.de/CodeSystem/dimdi/atc|C09BA02,http://fhir.de/CodeSystem/dimdi/atc|C09BA03,http://fhir.de/CodeSystem/dimdi/atc|C09BA04,http://fhir.de/CodeSystem/dimdi/atc|C09BA05,http://fhir.de/CodeSystem/dimdi/atc|C09BA06,http://fhir.de/CodeSystem/dimdi/atc|C09BA07,http://fhir.de/CodeSystem/dimdi/atc|C09BA08,http://fhir.de/CodeSystem/dimdi/atc|C09BA09,http://fhir.de/CodeSystem/dimdi/atc|C09BA12,http://fhir.de/CodeSystem/dimdi/atc|C09BA13,http://fhir.de/CodeSystem/dimdi/atc|C09BA15,http://fhir.de/CodeSystem/dimdi/atc|C09BA21,http://fhir.de/CodeSystem/dimdi/atc|C09BA22,http://fhir.de/CodeSystem/dimdi/atc|C09BA23,http://fhir.de/CodeSystem/dimdi/atc|C09BA25,http://fhir.de/CodeSystem/dimdi/atc|C09BA26,http://fhir.de/CodeSystem/dimdi/atc|C09BA27,http://fhir.de/CodeSystem/dimdi/atc|C09BA28,http://fhir.de/CodeSystem/dimdi/atc|C09BA29,http://fhir.de/CodeSystem/dimdi/atc|C09BA33,http://fhir.de/CodeSystem/dimdi/atc|C09BA35,http://fhir.de/CodeSystem/dimdi/atc|C09BA54,http://fhir.de/CodeSystem/dimdi/atc|C09BA55,http://fhir.de/CodeSystem/dimdi/atc|C09BB,http://fhir.de/CodeSystem/dimdi/atc|C09BB02,http://fhir.de/CodeSystem/dimdi/atc|C09BB03,http://fhir.de/CodeSystem/dimdi/atc|C09BB04,http://fhir.de/CodeSystem/dimdi/atc|C09BB05,http://fhir.de/CodeSystem/dimdi/atc|C09BB06,http://fhir.de/CodeSystem/dimdi/atc|C09BB07,http://fhir.de/CodeSystem/dimdi/atc|C09BB10,http://fhir.de/CodeSystem/dimdi/atc|C09BB12,http://fhir.de/CodeSystem/dimdi/atc|C09BX,http://fhir.de/CodeSystem/dimdi/atc|C09BX01,http://fhir.de/CodeSystem/dimdi/atc|C09BX02,http://fhir.de/CodeSystem/dimdi/atc|C09BX03,http://fhir.de/CodeSystem/dimdi/atc|C09BX04&status=active,completed"]],
[]]
```

## 1-age.json

### script

```json
curl --location --request POST 'http://localhost:5111/query-translate' \
--header 'Content-Type: codex/json' \
--header 'Accept: internal/json' \
--data-raw '{
    "exclusionCriteria": [],
    "inclusionCriteria": [
        {
            "termCode": {
                "code": "424144002",
                "display": "Current chronological age (observable entity)",
                "system": "http://snomed.info/sct"
            },
            "valueFilter": {
                "comparator": "eq",
                "type": "quantity-comparator",
                "unit": {
                    "code": "a",
                    "display": "years"
                },
                "value": 46.6
            }
        }
    ],
    "version": "http://to_be_decided.com/draft-1/schema#"
}'
```

### expected

```bash
[[["Patient?code=http://snomed.info/sct|424144002&value=46.6"]],[]]
```

### output

```bash
[[[""]], []] 
```
