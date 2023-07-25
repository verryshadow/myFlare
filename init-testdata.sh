#!/bin/bash

#docker-compose -f docker-compose-odm.yml up

FILES=./testdata3/*.json
for fhirBundle in $FILES
do
  echo "Sending Testdate bundle $fhirBundle ..."
  curl -X POST -H "Content-Type: application/json" -d @$fhirBundle http://localhost:8081/fhir
done
