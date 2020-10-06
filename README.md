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
Each item_key is then looked up in a userdefined mapping given in the ``I2B2/mapping.json`` where a list of corresponding FHIR-codes is returned.

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
    <summary>Our Example would look like this:</summary>

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
The generated FHIR-Queries from above are then executed one by one, the resulting Bundle is 