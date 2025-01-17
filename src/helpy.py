{
  "resourceType": "Bundle",
  "meta": {
    "profile": [ "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/gecco-bundle" ]
  },
  "type": "transaction",
  "entry": [ {
    "fullUrl": "Patient/0b84700cbb357068f7e8448dccf99ab4",
    "resource": {
      "resourceType": "Patient",
      "meta": {
        "profile": [ "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/Patient" ]
      },
      "extension": [ {
        "url": "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/age",
        "extension": [ {
          "url": "dateTimeOfDocumentation",
          "_valueDateTime": {
            "extension": [ {
              "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
              "valueCode": "unknown"
            } ]
          }
        }, {
          "url": "age",
          "valueAge": {
            "value": 55,
            "unit": "years",
            "system": "http://unitsofmeasure.org",
            "code": "a"
          }
        } ]
      }, {
        "url": "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/ethnic-group",
        "valueCoding": {
          "system": "http://snomed.info/sct",
          "code": "10117001"
        }
      }  ],
      "identifier": [ {
        "type": {
          "coding": [ {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "424144002"
          } ]
        },
        "system": "https://dein.krankenhaus.de/fhir/NamingSystem/patientId",
        "value": "testaufgabe-1-01",
        "assigner": {
          "reference": "Organization/7bf3ad593927360881a2fe7425317511"
        }
      } ],
      "birthDate": "2002-04-01"
    },
    "request": {
      "method": "POST",
      "url": "Patient",
      "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/patientId|0b84700cbb357068f7e8448dccf99ab4"
    }
  }, {
    "fullUrl": "Organization/7bf3ad593927360881a2fe7425317511",
    "resource": {
      "resourceType": "Organization",
      "name": "dein_Krankenhaus"
    },
    "request": {
      "method": "POST",
      "url": "Organization",
      "ifNoneExist": "identifier=null|7bf3ad593927360881a2fe7425317511"
    }
  }, {
    "fullUrl": "Encounter/c4ed5579f6d868a7fad4b60f7290af6d",
    "resource": {
      "resourceType": "Encounter",
      "identifier": [ {
        "system": "https://dein.krankenhaus.de/fhir/NamingSystem/encounterId",
        "value": "testaufgabe-1-01-Event.1_fall_arm_1.1",
        "assigner": {
          "reference": "Organization/7bf3ad593927360881a2fe7425317511"
        }
      } ],
      "status": "unknown",
      "class": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": "IMP",
        "display": "inpatient encounter"
      },
      "subject": {
        "reference": "Patient/0b84700cbb357068f7e8448dccf99ab4"
      }
    },
    "request": {
      "method": "POST",
      "url": "Encounter",
      "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/encounterId|c4ed5579f6d868a7fad4b60f7290af6d"
    }
  }, {
    "fullUrl": "Observation/5986ca781c2b22a946c9b6301cb91306",
    "resource": {
      "resourceType": "Observation",
      "meta": {
        "profile": [ "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/sex-assigned-at-birth" ]
      },
      "identifier": [ {
        "system": "https://dein.krankenhaus.de/fhir/NamingSystem/observationId",
        "value": "testaufgabe-1-01-Event.1_fall_arm_1.1-Form.demographie.1-demographie.biologisches_geschlecht_code.1-biologisches_geschlecht_code"
      } ],
      "status": "final",
      "category": [ {
        "coding": [ {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "social-history",
          "display": "Social History"
        } ]
      } ],
      "code": {
        "coding": [ {
          "system": "http://loinc.org",
          "code": "76689-9"
        } ]
      },
      "subject": {
        "reference": "Patient/0b84700cbb357068f7e8448dccf99ab4"
      },
      "encounter": {
        "reference": "Encounter/c4ed5579f6d868a7fad4b60f7290af6d"
      },
      "_effectiveDateTime": {
        "extension": [ {
          "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
          "valueCode": "unknown"
        } ]
      },
      "valueCodeableConcept": {
        "coding": [ {
          "system": "http://hl7.org/fhir/administrative-gender",
          "code": "female"
        } ]
      }
    },
    "request": {
      "method": "POST",
      "url": "Observation",
      "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/observationId|5986ca781c2b22a946c9b6301cb91306"
    }
  },{
    "fullUrl": "Observation/a7e0bafdb16b5208b621146591775bf2",
    "resource": {
      "resourceType": "Observation",
      "meta": {
        "profile": [ "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/pregnancy-status" ]
      },
      "identifier": [ {
        "type": {
          "coding": [ {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "OBI",
            "display": "Observation Instance Identifier"
          } ]
        },
        "system": "https://dein.krankenhaus.de/fhir/NamingSystem/observationId",
        "value": "1-Event.1_fall_arm_1.1-Form.demographie.1-demographie.schwangerschaft_code.1-schwangerschaft_code",
        "assigner": {
          "reference": "Organization/7bf3ad593927360881a2fe7425317511"
        }
      } ],
      "status": "final",
      "category": [ {
        "coding": [ {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "social-history",
          "display": "Social History"
        } ]
      } ],
      "code": {
        "coding": [ {
          "system": "http://loinc.org",
          "code": "82810-3"
        } ],
        "text": "Pregnancy status"
      },
      "subject": {
        "reference": "Patient/0b84700cbb357068f7e8448dccf99ab4"
      },
      "encounter": {
        "reference": "Encounter/c4ed5579f6d868a7fad4b60f7290af6d"
      },
      "_effectiveDateTime": {
        "extension": [ {
          "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
          "valueCode": "unknown"
        } ]
      },
      "valueCodeableConcept": {
        "coding": [ {
          "system": "http://loinc.org",
          "code": "LA15173-0"
        }, {
          "system": "http://snomed.info/sct",
          "code": "77386006"
        } ]
      }
    },
    "request": {
      "method": "POST",
      "url": "Observation",
      "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/observationId|a7e0bafdb16b5208b621146591775bf2"
    }
  }, {
    "fullUrl": "MedicationStatement/7dfd76ea99f32a37d4128c71629cec0e",
    "resource": {
      "resourceType": "MedicationStatement",
      "meta": {
        "profile": [ "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/pharmacological-therapy" ]
      },
      "identifier": [ {
        "system": "https://dein.krankenhaus.de/fhir/NamingSystem/medicationstatementId",
        "value": "testaufgabe-1-01-Event.1_fall_arm_1.1-Form.medikation.1-medikation.covid19therapie_antipyretika.1-covid19therapie_hydroxychloroquine"
      } ],
      "status": "active",
      "medicationCodeableConcept": {
        "coding": [ {
          "system": "http://fhir.de/CodeSystem/dimdi/atc",
          "code": "P01BA02"
        }, {
          "system": "http://snomed.info/sct",
          "code": "83490000"
        } ]
      },
      "subject": {
        "reference": "Patient/0b84700cbb357068f7e8448dccf99ab4"
      },
      "effectiveDateTime": "2021-01-01T14:15:00+00:00"
    },
    "request": {
      "method": "POST",
      "url": "MedicationStatement",
      "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/medicationstatementId|7dfd76ea99f32a37d4128c71629cec0e"
    }
  } ]
}