# i2b2 to FHIR pipeline

A tool to execute i2b2 requests in FHIR

## Goal
the goal of this project is to provide an API that allows execution of i2b2 queries on a FHIR-server

## Getting started
to start the server you first need to setup the python environment:
```bash
pip install -r requirements.txt
flask run_flask.py
```

## Algorithm
### Input
The Flask server receives a POST request to `http://localhost:5000/i2b2` with a body containing the i2b2 request.
<details>
    <summary>The request would look like this</summary>
    
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<request xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <query_definition>
        <query_name>Male-Admit D@12:58:34</query_name>
        <query_timing>ANY</query_timing>
        <specificity_scale>0</specificity_scale>
        <panel>
            <panel_number>1</panel_number>
            <panel_accuracy_scale>100</panel_accuracy_scale>
            <invert>0</invert>
            <panel_timing>ANY</panel_timing>
            <total_item_occurrences>1</total_item_occurrences>
            <item>
                <hlevel>3</hlevel>
                <item_name>Male</item_name>
                <item_key>\\i2b2_DEMO\i2b2\Demographics\Gender\Male\</item_key>
                <tooltip>Demographic \ Gender \ Male</tooltip>
                <class>ENC</class>
                <item_icon>LA</item_icon>
                <item_is_synonym>false</item_is_synonym>
            </item>
        </panel>
        <panel>
            <panel_number>2</panel_number>
            <panel_accuracy_scale>100</panel_accuracy_scale>
            <invert>0</invert>
            <panel_timing>ANY</panel_timing>
            <total_item_occurrences>1</total_item_occurrences>
            <item>
                <hlevel>2</hlevel>
                <item_key>\\i2b2_DIAG\i2b2\Measurements\Lymphozyten\</item_key>
                <item_name>Lymphozyten</item_name>
                <tooltip>tooltip</tooltip>
                <item_icon>FA</item_icon>
                <class>ENC</class>
                <constrain_by_value>
                    <value_type>NUMBER</value_type>
                    <value_unit_of_measure>%</value_unit_of_measure>
                    <value_operator>LT</value_operator>
                    <value_constraint>40</value_constraint>
                </constrain_by_value>
                <item_is_synonym>false</item_is_synonym>
            </item>
            <item>
                <hlevel>2</hlevel>
                <item_key>\\i2b2_DIAG\i2b2\Measurements\Lymphozyten_absolut\</item_key>
                <item_name>Lymphozyten - absolut</item_name>
                <tooltip>tooltip</tooltip>
                <item_icon>FA</item_icon>
                <class>ENC</class>
                <constrain_by_value>
                    <value_type>NUMBER</value_type>
                    <value_unit_of_measure>/nl</value_unit_of_measure>
                    <value_operator>LT</value_operator>
                    <value_constraint>3</value_constraint>
                </constrain_by_value>
                <item_is_synonym>false</item_is_synonym>
            </item>
        </panel>
        <panel>
            <panel_number>3</panel_number>
            <panel_accuracy_scale>100</panel_accuracy_scale>
            <invert>0</invert>
            <panel_timing>ANY</panel_timing>
            <total_item_occurrences>1</total_item_occurrences>
            <item>
                <hlevel>2</hlevel>
                <item_key>\\i2b2_DIAG\i2b2\Measurements\Bilirubin\</item_key>
                <item_name>Bilirubin (gesamt)</item_name>
                <tooltip>tooltip</tooltip>
                <item_icon>FA</item_icon>
                <class>ENC</class>
                <constrain_by_value>
                    <value_type>NUMBER</value_type>
                    <value_unit_of_measure>mg/dl</value_unit_of_measure>
                    <value_operator>LT</value_operator>
                    <value_constraint>8</value_constraint>
                </constrain_by_value>
                <item_is_synonym>false</item_is_synonym>
            </item>
            <item>
                <hlevel>2</hlevel>
                <item_key>\\i2b2_DIAG\i2b2\Measurements\Bilirubin_direkt\</item_key>
                <item_name>Bilirubin (direkt)</item_name>
                <tooltip>tooltip</tooltip>
                <item_icon>FA</item_icon>
                <class>ENC</class>
                <constrain_by_value>
                    <value_type>NUMBER</value_type>
                    <value_unit_of_measure>mg/dl</value_unit_of_measure>
                    <value_operator>LT</value_operator>
                    <value_constraint>6</value_constraint>
                </constrain_by_value>
                <item_is_synonym>false</item_is_synonym>
            </item>
        </panel>
    </query_definition>

    <result_output_list>
        <result_output priority_index="9" name="patient_count_xml"/>
    </result_output_list>

</request>
```
</details>


### Parsing the i2b2
In the first step the algorithm proceeds to extract the item_keys and constrains. 

For every Panel a list is created, into which a dictionary for every item from the given panel is inserted.

Each dictionary contains the item key and if given value constrains.

### Mapping the i2b2 keys
Each item_key is then looked up in a user-defined mapping given in the ``I2B2/mapping.json`` where a list of 
corresponding FHIR-codes is returned.

<details>
    <summary>A single entry in the mapping looks like this</summary>
    
```json
"\\\\i2b2_DEMO\\i2b2\\Demographics\\Gender\\": [
    {
      "res": "Patient",
      "param": "gender",
      "sys": "",
      "code": "male"
    },
    {
      "res": "Patient",
      "param": "gender",
      "sys": "",
      "code": "female"
    },
    {
      "res": "Patient",
      "param": "gender",
      "sys": "",
      "code": "unknown"
    }
]
```
</details>

This step leaves us with this data structure: ```List[List[List[Dict]]]```

<details>
    <summary>The above example after completing this stage:</summary>

```json
[
  [
    {
      "res": "Patient",
      "param": "gender",
      "sys": "",
      "code": "male"
    }
  ],
  [
    {
      "res": "Observation",
      "param": "code",
      "sys": "",
      "code": "I_COVAS_COV_M030_LAB_PARA_Q040",
      "valueParam": "value-quantity",
      "constrain_by_value": {
        "value_type": "NUMBER",
        "value_operator": "LT",
        "value_constraint": "40",
        "value_unit_of_measure": "%"
      }
    },
    {
      "res": "Observation",
      "param": "code",
      "sys": "",
      "code": "I_COVAS_COV_M030_LAB_PARA_Q050",
      "valueParam": "value-quantity",
      "constrain_by_value": {
        "value_type": "NUMBER",
        "value_operator": "LT",
        "value_constraint": "3",
        "value_unit_of_measure": "/nl"
      }
    }
  ],
  [
    {
      "res": "Observation",
      "param": "code",
      "sys": "",
      "code": "I_COVAS_COV_M030_LAB_PARA_Q190",
      "valueParam": "value-quantity",
      "constrain_by_value": {
        "value_type": "NUMBER",
        "value_operator": "LT",
        "value_constraint": "8",
        "value_unit_of_measure": "mg/dl"
      }
    },
    {
      "res": "Observation",
      "param": "code",
      "sys": "",
      "code": "I_COVAS_COV_M030_LAB_PARA_Q200",
      "valueParam": "value-quantity",
      "constrain_by_value": {
        "value_type": "NUMBER",
        "value_operator": "LT",
        "value_constraint": "6",
        "value_unit_of_measure": "mg/dl"
      }
    }
  ]
]
```
</details>

### Building the FHIR-Queries
In the next step, for each item of every panel a FHIR Query is generated

<details>
    <summary>forming the executable CNF</summary>
    
```json
[
  [
    "https://server_address/fhir-server/api/v4/Patient?gender=male&_format=application/fhir+xml"
  ],
  [
    "https://server_address/fhir-server/api/v4/Observation?code=I_COVAS_COV_M030_LAB_PARA_Q040&value-quantity=lt40&_format=application/fhir+xml",
    "https://server_address/fhir-server/api/v4/Observation?code=I_COVAS_COV_M030_LAB_PARA_Q050&value-quantity=lt3&_format=application/fhir+xml"
  ],
  [
    "https://server_address/fhir-server/api/v4/Observation?code=I_COVAS_COV_M030_LAB_PARA_Q190&value-quantity=lt8&_format=application/fhir+xml",
    "https://server_address/fhir-server/api/v4/Observation?code=I_COVAS_COV_M030_LAB_PARA_Q200&value-quantity=lt6&_format=application/fhir+xml"
  ]
]
```
</details>

### Executing the FHIR-Queries
The generated FHIR-Queries from above are then executed, and the resulting bundles are collected.

<details>
    <summary>and the resulting Bundles replace the corresponding queries in the above data structure.</summary>
    
```json
[
  [
    "<ns0:Bundle xmlns:ns0=\"http://hl7.org/fhir\"><ns0:id value=\"79542ba5-b238-44e5-80fb-2f4fdb45016f\" /><ns0:type value=\"searchset\" /><ns0:total value=\"15\" /><ns0:link><ns0:relation value=\"self\" /><ns0:url value=\"https://localhost:9443/fhir-server/api/v4/Patient?_count=10&amp;gender=male&amp;_page=1\" /></ns0:link><ns0:link><ns0:relation value=\"next\" /><ns0:url value=\"https://localhost:9443/fhir-server/api/v4/Patient?_count=10&amp;gender=male&amp;_page=2\" /></ns0:link><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Patient/174e86d4a4f-31b8377e-9f6a-4f91-b230-25149127191b\" /><ns0:resource><ns0:Patient><ns0:id value=\"174e86d4a4f-31b8377e-9f6a-4f91-b230-25149127191b\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:28:30.671Z\" /></ns0:meta><ns0:identifier><ns0:use value=\"usual\" /><ns0:system value=\"urn:oid:0.1.2.3.4.5.6.7\" /><ns0:value value=\"1001\" /></ns0:identifier><ns0:active value=\"true\" /><ns0:gender value=\"male\" /><ns0:birthDate value=\"1992-09-16\" /></ns0:Patient></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Patient/174e86d4e9a-efaf107b-f3f1-48f2-9960-848f4e33ec57\" /><ns0:resource><ns0:Patient><ns0:id value=\"174e86d4e9a-efaf107b-f3f1-48f2-9960-848f4e33ec57\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:28:31.77Z\" /></ns0:meta><ns0:identifier><ns0:use value=\"usual\" /><ns0:system value=\"urn:oid:0.1.2.3.4.5.6.7\" /><ns0:value value=\"1002\" /></ns0:identifier><ns0:active value=\"true\" /><ns0:gender value=\"male\" /><ns0:birthDate value=\"1942-10-24\" /></ns0:Patient></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Patient/174e86d5bd7-b4d0bee1-c7f5-44ad-b87c-df9b06aa4a0a\" /><ns0:resource><ns0:Patient><ns0:id value=\"174e86d5bd7-b4d0bee1-c7f5-44ad-b87c-df9b06aa4a0a\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:28:35.159Z\" /></ns0:meta><ns0:identifier><ns0:use value=\"usual\" /><ns0:system value=\"urn:oid:0.1.2.3.4.5.6.7\" /><ns0:value value=\"1005\" /></ns0:identifier><ns0:active value=\"true\" /><ns0:gender value=\"male\" /><ns0:birthDate value=\"1987-05-01\" /></ns0:Patient></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Patient/174e86d601f-a203378a-247c-4e22-abcb-28817458fc49\" /><ns0:resource><ns0:Patient><ns0:id value=\"174e86d601f-a203378a-247c-4e22-abcb-28817458fc49\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:28:36.255Z\" /></ns0:meta><ns0:identifier><ns0:use value=\"usual\" /><ns0:system value=\"urn:oid:0.1.2.3.4.5.6.7\" /><ns0:value value=\"1006\" /></ns0:identifier><ns0:active value=\"true\" /><ns0:gender value=\"male\" /><ns0:birthDate value=\"2007-10-06\" /></ns0:Patient></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Patient/174e86d6d30-53a35210-4ad1-47b6-a483-dc6d9b37b416\" /><ns0:resource><ns0:Patient><ns0:id value=\"174e86d6d30-53a35210-4ad1-47b6-a483-dc6d9b37b416\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:28:39.6Z\" /></ns0:meta><ns0:identifier><ns0:use value=\"usual\" /><ns0:system value=\"urn:oid:0.1.2.3.4.5.6.7\" /><ns0:value value=\"1009\" /></ns0:identifier><ns0:active value=\"true\" /><ns0:gender value=\"male\" /><ns0:birthDate value=\"1940-02-12\" /></ns0:Patient></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Patient/174e86d7181-946d8332-912d-425e-b144-1c425ef1b52a\" /><ns0:resource><ns0:Patient><ns0:id value=\"174e86d7181-946d8332-912d-425e-b144-1c425ef1b52a\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:28:40.705Z\" /></ns0:meta><ns0:identifier><ns0:use value=\"usual\" /><ns0:system value=\"urn:oid:0.1.2.3.4.5.6.7\" /><ns0:value value=\"1010\" /></ns0:identifier><ns0:active value=\"true\" /><ns0:gender value=\"male\" /><ns0:birthDate value=\"1955-05-31\" /></ns0:Patient></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Patient/174e86d7ebb-07e5f6f2-e5c3-43e0-8606-6299685fa4b0\" /><ns0:resource><ns0:Patient><ns0:id value=\"174e86d7ebb-07e5f6f2-e5c3-43e0-8606-6299685fa4b0\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:28:44.091Z\" /></ns0:meta><ns0:identifier><ns0:use value=\"usual\" /><ns0:system value=\"urn:oid:0.1.2.3.4.5.6.7\" /><ns0:value value=\"1013\" /></ns0:identifier><ns0:active value=\"true\" /><ns0:gender value=\"male\" /><ns0:birthDate value=\"1946-09-01\" /></ns0:Patient></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Patient/174e86d8bc4-80bd9c33-e324-4ff1-964e-fd98235ddb15\" /><ns0:resource><ns0:Patient><ns0:id value=\"174e86d8bc4-80bd9c33-e324-4ff1-964e-fd98235ddb15\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:28:47.428Z\" /></ns0:meta><ns0:identifier><ns0:use value=\"usual\" /><ns0:system value=\"urn:oid:0.1.2.3.4.5.6.7\" /><ns0:value value=\"1016\" /></ns0:identifier><ns0:active value=\"true\" /><ns0:gender value=\"male\" /><ns0:birthDate value=\"1947-03-24\" /></ns0:Patient></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Patient/174e86d902b-f1b80a68-bd78-4a63-b19d-30c8691ed037\" /><ns0:resource><ns0:Patient><ns0:id value=\"174e86d902b-f1b80a68-bd78-4a63-b19d-30c8691ed037\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:28:48.555Z\" /></ns0:meta><ns0:identifier><ns0:use value=\"usual\" /><ns0:system value=\"urn:oid:0.1.2.3.4.5.6.7\" /><ns0:value value=\"1017\" /></ns0:identifier><ns0:active value=\"true\" /><ns0:gender value=\"male\" /><ns0:birthDate value=\"1966-04-29\" /></ns0:Patient></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Patient/174e86d946b-959c6bcd-6381-4735-9b07-a718196a25a6\" /><ns0:resource><ns0:Patient><ns0:id value=\"174e86d946b-959c6bcd-6381-4735-9b07-a718196a25a6\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:28:49.643Z\" /></ns0:meta><ns0:identifier><ns0:use value=\"usual\" /><ns0:system value=\"urn:oid:0.1.2.3.4.5.6.7\" /><ns0:value value=\"1018\" /></ns0:identifier><ns0:active value=\"true\" /><ns0:gender value=\"male\" /><ns0:birthDate value=\"1940-08-01\" /></ns0:Patient></ns0:resource></ns0:entry></ns0:Bundle>"
  ],
  [
    "<ns0:Bundle xmlns:ns0=\"http://hl7.org/fhir\"><ns0:id value=\"650e6365-1acb-4ab0-a4e5-940300270362\" /><ns0:type value=\"searchset\" /><ns0:total value=\"2\" /><ns0:link><ns0:relation value=\"self\" /><ns0:url value=\"https://localhost:9443/fhir-server/api/v4/Observation?_count=10&amp;code=I_COVAS_COV_M030_LAB_PARA_Q040&amp;value-quantity=lt40&amp;_page=1\" /></ns0:link><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Observation/174e86ef0b1-aa9903cb-0b50-45c9-8066-38d68fb0db3a\" /><ns0:resource><ns0:Observation><ns0:id value=\"174e86ef0b1-aa9903cb-0b50-45c9-8066-38d68fb0db3a\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:30:18.801Z\" /></ns0:meta><ns0:identifier><ns0:value value=\"M-1065\" /></ns0:identifier><ns0:status value=\"final\" /><ns0:code><ns0:coding><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"I_COVAS_COV_M030_LAB_PARA_Q040\" /></ns0:coding></ns0:code><ns0:subject><ns0:type value=\"Patient\" /><ns0:identifier><ns0:value value=\"1002\" /></ns0:identifier></ns0:subject><ns0:effectiveDateTime value=\"2020-05-29T11:26:45Z\" /><ns0:valueQuantity><ns0:value value=\"30\" /><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"%\" /></ns0:valueQuantity></ns0:Observation></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Observation/174e86fe7e1-6431edc8-dbf3-4a31-a3ea-3e5cc1ff2eff\" /><ns0:resource><ns0:Observation><ns0:id value=\"174e86fe7e1-6431edc8-dbf3-4a31-a3ea-3e5cc1ff2eff\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:31:22.081Z\" /></ns0:meta><ns0:identifier><ns0:value value=\"M-1121\" /></ns0:identifier><ns0:status value=\"final\" /><ns0:code><ns0:coding><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"I_COVAS_COV_M030_LAB_PARA_Q040\" /></ns0:coding></ns0:code><ns0:subject><ns0:type value=\"Patient\" /><ns0:identifier><ns0:value value=\"1009\" /></ns0:identifier></ns0:subject><ns0:effectiveDateTime value=\"2020-06-02T15:31:35Z\" /><ns0:valueQuantity><ns0:value value=\"30\" /><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"%\" /></ns0:valueQuantity></ns0:Observation></ns0:resource></ns0:entry></ns0:Bundle>",
    "<ns0:Bundle xmlns:ns0=\"http://hl7.org/fhir\"><ns0:id value=\"759b8e2e-1006-42f4-a697-b53af9d9a6bd\" /><ns0:type value=\"searchset\" /><ns0:total value=\"2\" /><ns0:link><ns0:relation value=\"self\" /><ns0:url value=\"https://localhost:9443/fhir-server/api/v4/Observation?_count=10&amp;code=I_COVAS_COV_M030_LAB_PARA_Q050&amp;value-quantity=lt3&amp;_page=1\" /></ns0:link><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Observation/174e86ef4ef-7ffaa0ad-fa81-4d87-8b5f-4e71de4c9b66\" /><ns0:resource><ns0:Observation><ns0:id value=\"174e86ef4ef-7ffaa0ad-fa81-4d87-8b5f-4e71de4c9b66\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:30:19.887Z\" /></ns0:meta><ns0:identifier><ns0:value value=\"M-1066\" /></ns0:identifier><ns0:status value=\"final\" /><ns0:code><ns0:coding><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"I_COVAS_COV_M030_LAB_PARA_Q050\" /></ns0:coding></ns0:code><ns0:subject><ns0:type value=\"Patient\" /><ns0:identifier><ns0:value value=\"1002\" /></ns0:identifier></ns0:subject><ns0:effectiveDateTime value=\"2020-05-29T11:26:45Z\" /><ns0:valueQuantity><ns0:value value=\"2\" /><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"/nl\" /></ns0:valueQuantity></ns0:Observation></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Observation/174e86fec1f-0023b790-bf60-49d9-b615-7d2ccb41d017\" /><ns0:resource><ns0:Observation><ns0:id value=\"174e86fec1f-0023b790-bf60-49d9-b615-7d2ccb41d017\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:31:23.167Z\" /></ns0:meta><ns0:identifier><ns0:value value=\"M-1122\" /></ns0:identifier><ns0:status value=\"final\" /><ns0:code><ns0:coding><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"I_COVAS_COV_M030_LAB_PARA_Q050\" /></ns0:coding></ns0:code><ns0:subject><ns0:type value=\"Patient\" /><ns0:identifier><ns0:value value=\"1009\" /></ns0:identifier></ns0:subject><ns0:effectiveDateTime value=\"2020-06-02T15:31:35Z\" /><ns0:valueQuantity><ns0:value value=\"2\" /><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"/nl\" /></ns0:valueQuantity></ns0:Observation></ns0:resource></ns0:entry></ns0:Bundle>"
  ],
  [
    "<ns0:Bundle xmlns:ns0=\"http://hl7.org/fhir\"><ns0:id value=\"39ddd63c-ad6b-47c8-b4aa-4c71219bd866\" /><ns0:type value=\"searchset\" /><ns0:total value=\"2\" /><ns0:link><ns0:relation value=\"self\" /><ns0:url value=\"https://localhost:9443/fhir-server/api/v4/Observation?_count=10&amp;code=I_COVAS_COV_M030_LAB_PARA_Q190&amp;value-quantity=lt8&amp;_page=1\" /></ns0:link><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Observation/174e86f30c9-67cc8da3-b503-405f-bcf3-d64b93b6e127\" /><ns0:resource><ns0:Observation><ns0:id value=\"174e86f30c9-67cc8da3-b503-405f-bcf3-d64b93b6e127\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:30:35.209Z\" /></ns0:meta><ns0:identifier><ns0:value value=\"M-1080\" /></ns0:identifier><ns0:status value=\"final\" /><ns0:code><ns0:coding><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"I_COVAS_COV_M030_LAB_PARA_Q190\" /></ns0:coding></ns0:code><ns0:subject><ns0:type value=\"Patient\" /><ns0:identifier><ns0:value value=\"1002\" /></ns0:identifier></ns0:subject><ns0:effectiveDateTime value=\"2020-05-29T11:26:46Z\" /><ns0:valueQuantity><ns0:value value=\"7\" /><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"mg/dL\" /></ns0:valueQuantity></ns0:Observation></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Observation/174e8702709-7924c71e-2715-4741-baee-78984435180e\" /><ns0:resource><ns0:Observation><ns0:id value=\"174e8702709-7924c71e-2715-4741-baee-78984435180e\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:31:38.249Z\" /></ns0:meta><ns0:identifier><ns0:value value=\"M-1136\" /></ns0:identifier><ns0:status value=\"final\" /><ns0:code><ns0:coding><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"I_COVAS_COV_M030_LAB_PARA_Q190\" /></ns0:coding></ns0:code><ns0:subject><ns0:type value=\"Patient\" /><ns0:identifier><ns0:value value=\"1009\" /></ns0:identifier></ns0:subject><ns0:effectiveDateTime value=\"2020-06-02T15:31:35Z\" /><ns0:valueQuantity><ns0:value value=\"7\" /><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"mg/dL\" /></ns0:valueQuantity></ns0:Observation></ns0:resource></ns0:entry></ns0:Bundle>",
    "<ns0:Bundle xmlns:ns0=\"http://hl7.org/fhir\"><ns0:id value=\"159b02a4-c64e-428c-b540-62d397d11a0c\" /><ns0:type value=\"searchset\" /><ns0:total value=\"2\" /><ns0:link><ns0:relation value=\"self\" /><ns0:url value=\"https://localhost:9443/fhir-server/api/v4/Observation?_count=10&amp;code=I_COVAS_COV_M030_LAB_PARA_Q200&amp;value-quantity=lt6&amp;_page=1\" /></ns0:link><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Observation/174e86f3508-d6f8d611-62c9-4811-881c-d6bb79fdb940\" /><ns0:resource><ns0:Observation><ns0:id value=\"174e86f3508-d6f8d611-62c9-4811-881c-d6bb79fdb940\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:30:36.296Z\" /></ns0:meta><ns0:identifier><ns0:value value=\"M-1081\" /></ns0:identifier><ns0:status value=\"final\" /><ns0:code><ns0:coding><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"I_COVAS_COV_M030_LAB_PARA_Q200\" /></ns0:coding></ns0:code><ns0:subject><ns0:type value=\"Patient\" /><ns0:identifier><ns0:value value=\"1002\" /></ns0:identifier></ns0:subject><ns0:effectiveDateTime value=\"2020-05-29T11:26:46Z\" /><ns0:valueQuantity><ns0:value value=\"5\" /><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"mg/dL\" /></ns0:valueQuantity></ns0:Observation></ns0:resource></ns0:entry><ns0:entry><ns0:fullUrl value=\"https://localhost:9443/fhir-server/api/v4/Observation/174e8702b3a-74db713c-5dea-4c87-b280-32fec22be28e\" /><ns0:resource><ns0:Observation><ns0:id value=\"174e8702b3a-74db713c-5dea-4c87-b280-32fec22be28e\" /><ns0:meta><ns0:versionId value=\"1\" /><ns0:lastUpdated value=\"2020-10-02T08:31:39.322Z\" /></ns0:meta><ns0:identifier><ns0:value value=\"M-1137\" /></ns0:identifier><ns0:status value=\"final\" /><ns0:code><ns0:coding><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"I_COVAS_COV_M030_LAB_PARA_Q200\" /></ns0:coding></ns0:code><ns0:subject><ns0:type value=\"Patient\" /><ns0:identifier><ns0:value value=\"1009\" /></ns0:identifier></ns0:subject><ns0:effectiveDateTime value=\"2020-06-02T15:31:35Z\" /><ns0:valueQuantity><ns0:value value=\"5\" /><ns0:system value=\"http://aurora.regenstrief.org/~ucum/ucum.html#section-Alphabetic-Index\" /><ns0:code value=\"mg/dL\" /></ns0:valueQuantity></ns0:Observation></ns0:resource></ns0:entry></ns0:Bundle>"
  ]
]
```

</details>

### Patient-id extraction
For each returned FHIR bundle the set of IDs either associated with or identifying the Resources is extracted and 
collected in a list, such that every response string is replaced by a list:

<details>

````json
[
  [
    [
      "1001",
      "1002",
      "1005",
      "1006",
      "1009",
      "1010",
      "1013",
      "1016",
      "1017",
      "1018"
    ]
  ],
  [
    [
      "1002",
      "1009"
    ],
    [
      "1002",
      "1009"
    ]
  ],
  [
    [
      "1002",
      "1009"
    ],
    [
      "1002",
      "1009"
    ]
  ]
]
````
</details>


### Building the result set
The result set is then built by calculating the intersection of all panel-result unions.

<details>

````json
["1009", "1002"]
````

</details>


### Building the server response
In the last step the server response is crafted as a simple xml-string containing some more meta information:

<details>

````xml
<resultSet>
	<delta value="6.354444265365601" />
	<start_time value="1602157960.1216936" />
	<end_time value="1602157966.4761379" />
	<result value="1002" />
	<result value="1009" />
</resultSet>
````

</details> 