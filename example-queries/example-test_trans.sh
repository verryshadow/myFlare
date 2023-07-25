curl --location --request POST 'http://localhost:5000/query-translate' \
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