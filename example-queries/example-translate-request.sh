curl --location --request POST 'http://localhost:5111/query-translate' \
--header 'Content-Type: codex/json' \
--header 'Accept: internal/json' \
--data-raw '{
  "version": "http://to_be_decided.com/draft-1/schema#",
  "inclusionCriteria": [
    [
      {
        "termCode": {
          "code": "76689-9",
          "system": "http://loinc.org",
          "display": "Sex assigned at birth"
        },
        "valueFilter": {
          "type": "concept",
          "selectedConcepts": [
            {
              "code": "male",
              "system": "http://hl7.org/fhir/administrative-gender",
              "display": "Male"
            }
          ]
        }
      }
    ]
  ],
  "display": ""
}'
