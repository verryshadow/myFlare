## Docker Development Environment
To run with docker-compose and fhir server included:

```
docker-compose up -d
```

## Loading GECCO Testdate into FHIR Server

To load testdata into the local HAPI FHIR testserver exexute the `init-testdata.sh` script.

If you would like to load your own testdata into the test FHIR server, add your own FHIR transaction bundles to the testdata folder and execute the init-testdata script.


## Running a test query

```bash
curl --location --request POST 'http://localhost:5000/query-sync' \
--header 'Content-Type: codex/json' \
--header 'Accept: internal/json' \
--header 'Cookie: JSESSIONID=node0v3dnl2dqawhlbymawm3cl7ib22.node0' \
--data-raw '{
  "queryMetadata": {
    "version": "http://to_be_decided.com/draft-1/schema#",
    "timestamp": "2021-02-08T13:21:57",
    "queryId": "531ffdae-c500-4e8e-a978-69ddf4682e83"
  },
  "query": {
    "version": "http://to_be_decided.com/draft-1/schema#",
    "display": "",
    "inclusionCriteria": [
      [
        {
          "termCode": {
            "code": "J45.9",
            "system": "http://fhir.de/CodeSystem/dimdi/icd-10-gm",
            "version": "v1",
            "display": "Asthma"
          }
        }
      ]
    ],
    "exclusionCriteria": [
    ]
  }
}'
```