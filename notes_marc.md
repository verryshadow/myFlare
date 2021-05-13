# Notizen Flare Unittest Dev

Hier stehen Notizen zu Ereignissen oder anderen Dingen die während der
Entwicklung der Unittest aufgekommen sind

## Stufe 1

### Testdata

TestCases aus codex-testdata-to-sq sehen wie folgt aus 
``` json
{
    "exclusionCriteria": [],
    "inclusionCriteria": [
        {
            "termCode": {
                "code": "81839001",
                "display": "",
                "system": "http://snomed.info/sct"
            }
        },
        {
            "termCode": {
                "code": "B01AB13",
                "display": "",
                "system": "http://fhir.de/CodeSystem/dimdi/atc"
            }
        }
    ],
    "version": ""
}
```

Es fehlt jedoch eine geschweifte Klammer nach innerhalb der inclusionCriteria
und leere exclusionCriteria können nicht gemappt werden. Es müsste daher wie
folgt aussehen:

```json
{
  "version": "http://to_be_decided.com/draft-1/schema#",
  "display": "",
  "inclusionCriteria": [
    [
      {
        "termCode": {
                "code": "81839001",
                "display": "",
                "system": "http://snomed.info/sct"
            }
      },
      {
            "termCode": {
                "code": "B01AB13",
                "display": "",
                "system": "http://fhir.de/CodeSystem/dimdi/atc"
            }
        }
    ]
  ]
}
```


## Stufe 2



## Stufe 3


