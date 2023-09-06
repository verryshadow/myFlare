# #########################################################################################
#
# Creates random patients data with age, birthdate, therapy, gender, ethnics, pregnant
#   + adds a new termcode called "Tobacco Use Status" & "warfarin-dose" for testing reasons
# all patients are ether not pregnant or the pregnancy status is unknown
#
# #########################################################################################

import secrets
import json
import random
from datetime import datetime, timedelta

# some ethnics
ethnics = ['10008004', '10117001', '10292001', '10432001', '108342005', '113169009', '113170005', '113171009',
           '11794009', '12556008', '13233008', '1340002', '13440006', '14045001', '14176005', '14470009', '1451003',
           '14999008', '15086000', '15801006', '160531006', '17095009', '17789004', '18167009', '18575005', '18583004',
           '185984009', '185988007', '185990008', '185995003', '186001005', '186002003', '186003008', '186019001',
           '186035008', '186036009', '186039002', '186040000', '186041001', '186042008', '186044009', '18664001',
           '19085009', '1919006', '19434008', '20140003', '20291009', '20449009', '21047009', '2135-2', '21868006',
           '21993009', '22007004', '23517005', '23534002', '23922002', '24812003', '25750005', '25804004', '26215007',
           '2688009', '270460000', '270461001', '270462008', '2720008', '27301002', '275586009', '275587000',
           '275588005', '275589002', '275590006', '27683006', '27700004', '28409002', '2852001', '28562006', '286009',
           '28796001', '28821007', '29343004', '309643000', '309644006', '312859007', '315236000', '315237009',
           '315240009', '315280000', '315283003', '315634007', '315635008', '31637002', '32045009', '32513008',
           '32873005', '33182009', '3353005', '33897005', '34334001', '35007000', '36329002', '3698008', '37474002',
           '37843006', '38144004', '3818007', '38361009', '38750003', '39007007', '39764005', '401213008', '40165009',
           '40182006', '4073004', '41076003', '413465009', '413466005', '414152003', '414551003', '414661004',
           '414978006', '41798002', '42632009', '4299001', '43056000', '43608005', '43890005', '44460002', '445343003',
           '45465003', '46110004', '46723002', '47250000', '47327008', '48118002', '48294008', '48375000', '48679001',
           '49202008', '50405005', '51827000', '52075006', '521000220104', '53195006', '53460002', '55990000',
           '56056003', '57405008', '57539009', '58047002', '59366001', '59487007', '59597001', '60157000', '62598008',
           '63457007', '6373008', '63732001', '63736003', '64483007', '64693008', '65776006', '66406004', '66920001',
           '67165000', '67439005', '67931002', '68486007', '69865008', '69983001', '704385002', '704386001',
           '704387005', '704388000', '704389008', '704390004', '704391000', '704392007', '71176007', '718958002',
           '718959005', '718960000', '718961001', '718962008', '718963003', '718964009', '71949006', '72201005',
           '72248007', '72337002', '72809004', '733078003', '733446001', '735001008', '73524008', '73736004',
           '74159009', '74302004', '75301003', '75326007', '75704009', '76253004', '76460008', '76574004', '76768002',
           '76775001', '76883002', '7695005', '77502007', '77686000', '79434006', '80208004', '80528001', '81035008',
           '8124001', '81283004', '81403004', '81560001', '81653003', '81846005', '82174001', '83365001', '83584002',
           '83939006', '85163001', '85371009', '85515006', '86275006', '870448005', '87323008', '88790004', '88839008',
           '88934004', '89026003', '90027003', '90348007', '90822005', '91066000', '91191002', '91488008', '9158000',
           '9533000']

# some genders
gender = ['female', 'male', 'unknown']

# pregnancy status is unknown or not pregnant
pregnant = ['LA4489-6', 'LA26683-5']

# codes for covid 19 therapies
covid19therapy = ['A11CC06', 'A12CB', 'A12CB01', 'A12CB02', 'A12CB03', 'A12CB05', 'A12CB06', 'B02AB04', 'D01AC20',
                  'D11AH01', 'D11AX22', 'G01B', 'G01BA', 'G01BA01', 'G01BC', 'G01BD', 'G01BD01', 'G01BE', 'G01BE50',
                  'G01BF', 'H02', 'H02A', 'H02AA', 'H02AA01', 'H02AA02', 'H02AA03', 'H02AB', 'H02AB01', 'H02AB02',
                  'H02AB03', 'H02AB04', 'H02AB05', 'H02AB06', 'H02AB07', 'H02AB08', 'H02AB09', 'H02AB10', 'H02AB11',
                  'H02AB12', 'H02AB13', 'H02AB14', 'H02AB15', 'H02AB17', 'H02AB51', 'H02AB54', 'H02AB56', 'H02AB58',
                  'H02B', 'H02BX', 'H02BX01', 'H02BX02', 'H02BX06', 'H02BX08', 'H02BX09', 'H02BX20', 'H02BX21', 'H02C',
                  'H02CA', 'H02CA01', 'H02CA02', 'J05AB06', 'J05AE08', 'J05AE10', 'J05AH02', 'J05AP01', 'J05AR10',
                  'J05AR14', 'J05AR15', 'J05AR22', 'J05AR23', 'J05AX27', 'L01XE10', 'L01XE18', 'L03AB', 'L03AB01',
                  'L03AB02', 'L03AB03', 'L03AB04', 'L03AB05', 'L03AB06', 'L03AB07', 'L03AB08', 'L03AB09', 'L03AB10',
                  'L03AB11', 'L03AB12', 'L03AB13', 'L03AB14', 'L03AB15', 'L03AB18', 'L03AB60', 'L03AB61', 'L04AA10',
                  'L04AA18', 'L04AB', 'L04AB01', 'L04AB02', 'L04AB03', 'L04AB04', 'L04AB05', 'L04AB06', 'L04AB07',
                  'L04AC', 'L04AC01', 'L04AC02', 'L04AC03', 'L04AC04', 'L04AC05', 'L04AC07', 'L04AC08', 'L04AC09',
                  'L04AC10', 'L04AC11', 'L04AC12', 'L04AC13', 'L04AC14', 'L04AC15', 'L04AC16', 'L04AC17', 'L04AC18',
                  'L04AD', 'L04AD01', 'L04AD02', 'L04AD03', 'M01BA', 'M01BA01', 'M01BA02', 'M01BA03', 'M01BA04',
                  'M01BA05', 'M01BA06', 'M01BA07', 'M01BA08', 'M04AC01', 'N02B', 'N02BA', 'N02BA01', 'N02BA02',
                  'N02BA03', 'N02BA04', 'N02BA05', 'N02BA06', 'N02BA07', 'N02BA08', 'N02BA09', 'N02BA10', 'N02BA11',
                  'N02BA12', 'N02BA13', 'N02BA14', 'N02BA15', 'N02BA16', 'N02BA19', 'N02BA20', 'N02BA51', 'N02BA55',
                  'N02BA57', 'N02BA59', 'N02BA65', 'N02BA71', 'N02BA75', 'N02BA77', 'N02BA79', 'N02BB', 'N02BB01',
                  'N02BB02', 'N02BB03', 'N02BB04', 'N02BB05', 'N02BB06', 'N02BB51', 'N02BB52', 'N02BB53', 'N02BB54',
                  'N02BB56', 'N02BB71', 'N02BB72', 'N02BB73', 'N02BB74', 'N02BB76', 'N02BE', 'N02BE01', 'N02BE03',
                  'N02BE04', 'N02BE05', 'N02BE51', 'N02BE53', 'N02BE54', 'N02BE61', 'N02BE71', 'N02BE73', 'N02BE74',
                  'N02BG', 'N02BG02', 'N02BG03', 'N02BG04', 'N02BG05', 'N02BG06', 'N02BG07', 'N02BG08', 'N02BG09',
                  'N02BG10', 'N02BH', 'N02BH01', 'N02BH10', 'N02BH20', 'N02BP', 'N02BP01', 'N02BP02', 'P01BA01',
                  'P01BA02', 'P02CF01', 'R03AK', 'R03AK01', 'R03AK02', 'R03AK03', 'R03AK04', 'R03AK05', 'R03AK06',
                  'R03AK07', 'R03AK08', 'R03AK09', 'R03AK10', 'R03AK11', 'R03AK12', 'R03AK13', 'R03AL', 'R03AL01',
                  'R03AL02', 'R03AL03', 'R03AL04', 'R03AL05', 'R03AL06', 'R03AL07', 'R03AL08', 'R03AL09', 'S01AD05',
                  'S01AD09', 'S01XA18', 'S02B', 'S02BA', 'S02BA01', 'S02BA03', 'S02BA06', 'S02BA07', 'S02BA08',
                  'S02BA56', 'C09A', 'C09AA', 'C09AA01', 'C09AA02', 'C09AA03', 'C09AA04', 'C09AA05', 'C09AA06',
                  'C09AA07', 'C09AA08', 'C09AA09', 'C09AA10', 'C09AA11', 'C09AA12', 'C09AA13', 'C09AA14', 'C09AA15',
                  'C09AA16', 'C09B', 'C09BA', 'C09BA01', 'C09BA02', 'C09BA03', 'C09BA04', 'C09BA05', 'C09BA06',
                  'C09BA07', 'C09BA08', 'C09BA09', 'C09BA12', 'C09BA13', 'C09BA15', 'C09BA21', 'C09BA22', 'C09BA23',
                  'C09BA25', 'C09BA26', 'C09BA27', 'C09BA28', 'C09BA29', 'C09BA33', 'C09BA35', 'C09BA54', 'C09BA55',
                  'C09BB', 'C09BB02', 'C09BB03', 'C09BB04', 'C09BB05', 'C09BB06', 'C09BB07', 'C09BB10', 'C09BB12',
                  'C09BX', 'C09BX01', 'C09BX02', 'C09BX03', 'C09BX04', 'B01AA04', 'B01AB', 'B01AB01', 'B01AB02',
                  'B01AB04', 'B01AB05', 'B01AB06', 'B01AB07', 'B01AB08', 'B01AB09', 'B01AB10', 'B01AB11', 'B01AB12',
                  'B01AB13', 'B01AB51', 'B01AB63', 'B01AC', 'B01AC01', 'B01AC02', 'B01AC03', 'B01AC04', 'B01AC05',
                  'B01AC06', 'B01AC07', 'B01AC08', 'B01AC09', 'B01AC10', 'B01AC11', 'B01AC12', 'B01AC13', 'B01AC15',
                  'B01AC16', 'B01AC17', 'B01AC18', 'B01AC19', 'B01AC21', 'B01AC22', 'B01AC23', 'B01AC24', 'B01AC25',
                  'B01AC26', 'B01AC27', 'B01AC30', 'B01AC34', 'B01AC36', 'B01AC56', 'B01AC86', 'B01AE', 'B01AE01',
                  'B01AE02', 'B01AE03', 'B01AE04', 'B01AE05', 'B01AE06', 'B01AE07', 'B01AF', 'B01AF01', 'B01AF02',
                  'B01AF03', 'B01AF04', 'J06B', 'J06BA', 'J06BA01', 'J06BA02', 'J06BB', 'J06BB01', 'J06BB02', 'J06BB03',
                  'J06BB04', 'J06BB05', 'J06BB06', 'J06BB07', 'J06BB08', 'J06BB09', 'J06BB10', 'J06BB11', 'J06BB12',
                  'J06BB13', 'J06BB14', 'J06BB15', 'J06BB16', 'J06BB17', 'J06BB18', 'J06BB19', 'J06BB21', 'J06BB22',
                  'J06BB30', 'J06BC', 'J06BC01', 'J06BC10']

# new codes for "Tobacco Use Status":
tobacco_use_status_values = ['yes', 'no', 'unknown']

file_path = "../"

# id, age, birthdate, therapy, gender, ethnics
for i in range(20):
    # Generate a random hex number with 16 digits
    random_hex = secrets.token_hex(16)

    # Generate a random number between 0 and 100 with one decimal point
    age = round(random.uniform(0, 100), 1)

    # get the birthdate
    birthdate = datetime.now().date() - timedelta(days=int(age * 365))

    # new codes for "Warfarin Dose":
    warfarin_dose = round(random.uniform(2, 5), 2)
    print(warfarin_dose)

    mydict = {
        "resourceType": "Bundle",
        "meta": {
            "profile": ["https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/gecco-bundle"]
        },
        "type": "transaction",
        "entry": [{
            "fullUrl": "Patient/" + random_hex,
            "resource": {
                "resourceType": "Patient",
                "meta": {
                    "profile": ["https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/Patient"]
                },
                "extension": [{
                    "url": "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/age",
                    "extension": [{
                        "url": "dateTimeOfDocumentation",
                        "_valueDateTime": {
                            "extension": [{
                                "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                                "valueCode": "unknown"
                            }]
                        }
                    }, {
                        "url": "age",
                        "valueAge": {
                            "value": age,
                            "unit": "years",
                            "system": "http://unitsofmeasure.org",
                            "code": "a"
                        }
                    }]
                }, {
                    "url": "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/ethnic-group",
                    "valueCoding": {
                        "system": "http://snomed.info/sct",
                        "code": random.choice(ethnics)
                    }
                }],
                "identifier": [{
                    "type": {
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "424144002"
                        }]
                    },
                    "system": "https://dein.krankenhaus.de/fhir/NamingSystem/patientId",
                    "value": "testaufgabe-1-01",
                    "assigner": {
                        "reference": "Organization/7bf3ad593927360881a2fe7425317511"
                    }
                }],
                "birthDate": str(birthdate)
            },
            "request": {
                "method": "POST",
                "url": "Patient",
                "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/patientId|" + random_hex
            }
        }, {
            "fullUrl": "Observation/a7e0bafdb16b5208b621146591775bf2",
            "resource": {
                "resourceType": "Observation",
                "meta": {
                    "profile": [
                        "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/pregnancy-status"]
                },
                "identifier": [{
                    "type": {
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "OBI",
                            "display": "Observation Instance Identifier"
                        }]
                    },
                    "system": "https://dein.krankenhaus.de/fhir/NamingSystem/observationId",
                    "value": "1-Event.1_fall_arm_1.1-Form.demographie.1-demographie.schwangerschaft_code.1-schwangerschaft_code",
                    "assigner": {
                        "reference": "Organization/7bf3ad593927360881a2fe7425317511"
                    }
                }],
                "status": "final",
                "category": [{
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "social-history",
                        "display": "Social History"
                    }]
                }],
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "82810-3"
                    }],
                    "text": "Pregnancy status"
                },
                "subject": {
                    "reference": "Patient/" + random_hex
                },
                "_effectiveDateTime": {
                    "extension": [{
                        "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                        "valueCode": "unknown"
                    }]
                },
                "valueCodeableConcept": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": random.choice(pregnant)
                    }]
                }
            },
            "request": {
                "method": "POST",
                "url": "Observation",
                "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/observationId|a7e0bafdb16b5208b621146591775bf2"
            }
        }, {
            "fullUrl": "Observation/540a48c942408b04a753b7a9f05987f0",
            "resource": {
                "resourceType": "Observation",
                "meta": {
                    "profile": ["https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/body-weight"]
                },
                "identifier": [{
                    "type": {
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "OBI",
                            "display": "Observation Instance Identifier"
                        }]
                    },
                    "system": "https://dein.krankenhaus.de/fhir/NamingSystem/observationId",
                    "value": "1-Event.1_fall_arm_1.1-Form.demographie.1-demographie.gewicht_code.1-gewicht_code",
                    "assigner": {
                        "reference": "Organization/7bf3ad593927360881a2fe7425317511"
                    }
                }],
                "status": "final",
                "category": [{
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }]
                }],
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "29463-7"
                    }, {
                        "system": "http://snomed.info/sct",
                        "code": "27113001"
                    }],
                    "text": "Body Weight"
                },
                "subject": {
                    "reference": "Patient/" + random_hex
                },
                "_effectiveDateTime": {
                    "extension": [{
                        "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                        "valueCode": "unknown"
                    }]
                },
                "valueQuantity": {
                    "value": round(random.uniform(0.0,200.0),1),
                    "unit": "kilogram",
                    "system": "http://unitsofmeasure.org",
                    "code": "kg"
                }
            },
            "request": {
                "method": "POST",
                "url": "Observation",
                "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/observationId|540a48c942408b04a753b7a9f05987f0"
            }
        },

            {
                "fullUrl": "Observation/a7e0bafdb16b5208b721146591775bf2",
                "resource": {
                    "resourceType": "Observation",
                    "meta": {
                        "profile": [
                            "https://needed-to-be-decided-link/tobacco-use-status"]
                    },
                    "identifier": [{
                        "type": {
                            "coding": [{
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                "code": "OBI",
                                "display": "Observation Instance Identifier"
                            }]
                        },
                        "system": "https://dein.krankenhaus.de/fhir/NamingSystem/observationId",
                        "value": "tobacco use status",
                        "assigner": {
                            "reference": "Organization/7bf3ad593927360881a2fe7425317511"
                        }
                    }],
                    "status": "final",
                    "category": [{
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "social-history",
                            "display": "Social History"
                        }]
                    }],
                    "code": {
                        "coding": [{
                            "system": "http://verenas-example.at",
                            "code": "77777-0"
                        }],
                        "text": "Tobacco Use Status"
                    },
                    "subject": {
                        "reference": "Patient/" + random_hex
                    },
                    "_effectiveDateTime": {
                        "extension": [{
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unknown"
                        }]
                    },
                    "valueCodeableConcept": {
                        "coding": [{
                            "system": "http://verenas-example.at",
                            "code": random.choice(tobacco_use_status_values)
                            # e.g. call http://localhost:8081/fhir/Observation?code=http://verenas-example.at|77777-0&value-concept=http://loinc.org|yes
                        }]
                    }
                },
                "request": {
                    "method": "POST",
                    "url": "Observation",
                    "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/observationId|a7e0bafdb16b5208b721146591775bf2"
                }
            },

            {
                "fullUrl": "Observation/a7e0bafdb16b5208b621146591775bf2",
                "resource": {
                    "resourceType": "Observation",
                    "meta": {
                        "profile": ["https://needed-to-be-decided-link/warfarin-dose"]
                    },
                    "identifier": [{
                        "type": {
                            "coding": [{
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                "code": "OBI",
                                "display": "Observation Instance Identifier"
                            }]
                        },
                        "system": "https://dein.krankenhaus.de/fhir/NamingSystem/observationId",
                        "value": "warfarin-dose",
                        "assigner": {
                            "reference": "Organization/7bf3ad593927360881a2fe7425317511"
                        }
                    }],
                    "status": "final",
                    "category": [{
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "vital-signs",
                            "display": "Vital Signs"
                        }]
                    }],
                    "code": {
                        "coding": [{
                            "system": "http://verenas-example.at",
                            "code": "33333-0"
                        }, {
                            "system": "http://verenas-new-example.at",
                            "code": "03-330"
                        }],
                        "text": "Warfarin Dose"
                    },
                    "subject": {
                        "reference": "Patient/" + random_hex
                    },
                    "_effectiveDateTime": {
                        "extension": [{
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unknown"
                        }]
                    },
                    "valueQuantity": {
                        "value": warfarin_dose,
                        "unit": "mg",
                        "system": "http://unitsofmeasure.org",
                        "code": "mg"
                    }
                },
                "request": {
                    "method": "POST",
                    "url": "Observation",
                    "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/observationId|b1e6c82a81da9cc7c53da1742adc0ac6"
                }
            },

            {
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
                "fullUrl": "Observation/5986ca781c2b22a946c9b6301cb91306",
                "resource": {
                    "resourceType": "Observation",
                    "meta": {
                        "profile": [
                            "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/sex-assigned-at-birth"]
                    },
                    "identifier": [{
                        "system": "https://dein.krankenhaus.de/fhir/NamingSystem/observationId",
                        "value": "testaufgabe-1-01-Event.1_fall_arm_1.1-Form.demographie.1-demographie.biologisches_geschlecht_code.1-biologisches_geschlecht_code"
                    }],
                    "status": "final",
                    "category": [{
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "social-history",
                            "display": "Social History"
                        }]
                    }],
                    "code": {
                        "coding": [{
                            "system": "http://loinc.org",
                            "code": "76689-9"
                        }]
                    },
                    "subject": {
                        "reference": "Patient/" + random_hex
                    },
                    "_effectiveDateTime": {
                        "extension": [{
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unknown"
                        }]
                    },
                    "valueCodeableConcept": {
                        "coding": [{
                            "system": "http://hl7.org/fhir/administrative-gender",
                            "code": random.choice(gender)
                        }]
                    }
                },
                "request": {
                    "method": "POST",
                    "url": "Observation",
                    "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/observationId|5986ca781c2b22a946c9b6301cb91306"
                }
            }, {
                "fullUrl": "MedicationStatement/7dfd76ea99f32a37d4128c71629cec0e",
                "resource": {
                    "resourceType": "MedicationStatement",
                    "meta": {
                        "profile": [
                            "https://www.netzwerk-universitaetsmedizin.de/fhir/StructureDefinition/pharmacological-therapy"]
                    },
                    "identifier": [{
                        "system": "https://dein.krankenhaus.de/fhir/NamingSystem/medicationstatementId",
                        "value": "testaufgabe-1-01-Event.1_fall_arm_1.1-Form.medikation.1-medikation.covid19therapie_antipyretika.1-covid19therapie_hydroxychloroquine"
                    }],
                    "status": "active",
                    "medicationCodeableConcept": {
                        "coding": [{
                            "system": "http://fhir.de/CodeSystem/dimdi/atc",
                            "code": "" + random.choice(covid19therapy)
                        }]
                    },
                    "subject": {
                        "reference": "Patient/" + random_hex
                    },
                    "effectiveDateTime": "2021-01-01T14:15:00+00:00"
                },
                "request": {
                    "method": "POST",
                    "url": "MedicationStatement",
                    "ifNoneExist": "identifier=https://dein.krankenhaus.de/fhir/NamingSystem/medicationstatementId|7dfd76ea99f32a37d4128c71629cec0e"
                }
            }]
    }
    print(file_path + "data" + str(i) + ".json")
    with open((file_path + "data" + str(i) + ".json"), "w") as file:
        json.dump(mydict, file)

print(type(mydict))
