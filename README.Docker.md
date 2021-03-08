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
curl -X POST --data @src/query_parser/i2b2/i2b2_gecco_demo.xml -H "Content-type: i2b2/xml" -H "Accept: internal/xml" http://localhost:5000/query
```