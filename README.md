# Flare

**F**easibi**l**ity **A**nalysis **R**equest **E**xecutor

## Goal
the goal of this project is to provide an API that allows for execution of i2b2 queries on a FHIR-server

## Quick Start
To quickly start a FLARE instance with a FHIR server and import sample data into it, execute the following steps:

```bash
docker-compose up -d
```

```bash
./init-testdata.sh
```

after starting the FLARE instance you can test if it is up with
```bash
curl -vX POST --data @src/query_parser/i2b2/i2b2_gecco_demo.xml -H "Content-type: i2b2/xml" -H "Accept: internal/xml" http://localhost:5000/query
```
this command submits a test query to the server, and renders the response with their headers:
```
*   Trying ::1:5000...
* TCP_NODELAY set
*   Trying 127.0.0.1:5000...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /query HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.65.3
> Content-type: i2b2/xml
> Accept: internal/xml
> Content-Length: 1321
> Expect: 100-continue
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 100 Continue
* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 202 ACCEPTED
< Content-Type: text/html; charset=utf-8
< Content-Length: 0
< Location: http://localhost:5000/query/ea6cd7ff-fbb4-4824-9147-81681b9f73e2
< Server: Werkzeug/1.0.1 Python/3.8.8
< Date: Wed, 03 Mar 2021 09:33:02 GMT
<
* Closing connection 0

```

The query result can be retrieved by appending ```/results``` to the  URL in the Location-header
```bash
curl http://localhost:5000/query/ea6cd7ff-fbb4-4824-9147-81681b9f73e2/results
```

## API documentation

The API essentially consists of the query resource, which can be manipulated as follows:

### Submit Query
a query can be submitted, with a POST operation to 
```/query```

Since FLARE can handle multiple query formats, and different query outputs, Metadata is required for the execution.
This metadata is supplied through the two HTTP-headers ```Content-Type``` and ```Accept```

* **Content-Type** determines the format of the query, and accepts the following values

|Value            |Meaning                                  |
|-----------------|-----------------------------------------|
|codex/json       |Codex structured query                   |
|i2b2/xml         |I2B2 query definition                    |
|internal/json    |The internal representation of the query |

* **Accept** determines the resulting output, and accepts the following values:

| Value        |Meaning                                 |
|--------------|----------------------------------------|
|result/xml    |The fully processed result              |
|internal/json |The internal representation of the query|


On success, the query response contains a code 202, and a Location header linking to the created query resource

<details>
<summary>Example query</summary>

####Query
```bash
curl -vX POST --data @src/query_parser/i2b2/i2b2_gecco_demo.xml -H "Content-type: i2b2/xml" -H "Accept: internal/xml" http://localhost:5000/query
```

####Response

```
*   Trying ::1:5000...
* TCP_NODELAY set
*   Trying 127.0.0.1:5000...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /query HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.65.3
> Content-type: i2b2/xml
> Accept: internal/xml
> Content-Length: 1321
> Expect: 100-continue
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 100 Continue
* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 202 ACCEPTED
< Content-Type: text/html; charset=utf-8
< Content-Length: 0
< Location: http://localhost:5000/query/ea6cd7ff-fbb4-4824-9147-81681b9f73e2
< Server: Werkzeug/1.0.1 Python/3.8.8
< Date: Wed, 03 Mar 2021 09:33:02 GMT
<
* Closing connection 0
```
</details>

### The query resource
The URL in the Location header when creating a query, looks like this: ```<server>/query/<query-id>/```, and allows you to:

* **DELETE** the query
* **GET** the original query

<details>
<summary>Example query</summary>

####Query
```bash
curl http://localhost:5000/query/ea6cd7ff-fbb4-4824-9147-81681b9f73e2
```

####Response
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<request>
    <query_definition>
        <query_name>Male-Admit D@12:58:34</query_name>
        <query_timing>ANY</query_timing>
        <specificity_scale>
            0
        </specificity_scale>
        <panel>
            <panel_number>2</panel_number>
            <panel_accuracy_scale>100</panel_accuracy_scale>
            <invert>0</invert>
            <panel_timing>ANY
            </panel_timing>
            <total_item_occurrences>1</total_item_occurrences>
            <item>
                <hlevel>2</hlevel>
                <item_key>\\GECCO_DEMO\Observation\BloodOxygen</item_key>
                <item_name>Blood Oxygen</item_name>
                <tooltip>tooltip</tooltip>
                <item_icon>FA</item_icon>
                <class>ENC</class>
                <constrain_by_value>
                    <value_type>NUMBER</value_type>
                    <value_unit_of_measure>%</value_unit_of_measure>
                    <value_operator>LT</value_operator>
                    <value_constraint>90
                    </value_constraint>
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

### The query state
Since the execution of the query runs asynchronously, you can poll the current state of the query by calling ```<server>/query/<query-id>/status```

<details>
<summary>Example query</summary>

####Query
```bash
curl http://localhost:5000/query/ea6cd7ff-fbb4-4824-9147-81681b9f73e2/status
```

####Response
```
DONE
```
</details>

### The query result
Once the query state API returns "DONE" the result can be retrieved by calling GET on ```<server>/query/<query-id>/results```

<details>
<summary>Example query</summary>

####Query
```bash
curl http://localhost:5000/query/ea6cd7ff-fbb4-4824-9147-81681b9f73e2/results
```

####Response
```json
[["Observation?code=3150-0&_format=application/fhir+xml"]]
```
</details>

##Running the server from scratch

*This section is not complete yet*

```bash
pip install -r requirements.txt

FHIR_BASE_URL=http://localhost:5555/fhir python src/run_server.py

```

When the server is running, you can run queries:
```bash
curl -X POST --data @query/i2b2/i2b2_demo.xml "Content-type: i2b2/xml" -H "Accept: internal/xml" http://localhost:5000/query
```
which will return with the relative location to the request status in the location header

