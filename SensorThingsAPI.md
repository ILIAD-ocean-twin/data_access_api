# SensorThings APIs

[SensorThings API](https://ogcapi.ogc.org/sensorthings/) is the OGC standard endorsed as the INSPIRE good practice to share observations data. It is compliant with the ISO 19156/OGC Observations & Measurements standards.
Entry level descriptions of the API are available on the [Wikipedia](https://en.wikipedia.org/wiki/SensorThings_API)

## Use cases

STA is flexible standard useful in particular for:
 - exposing observations with all the Sensor, Observed Properties, Location in a flexible way so that client can build the query to access observations in the light way and get the whole related data though simple queries (like joins in SQL). Example STA demo is available on the [PSNC infrastruture](https://grlc-dpi-enabler-demeter.apps.paas-dev.psnc.pl/api-git/ILIAD-ocean-twin/JF-API/)
 - providing observation as the data stream. STA was designed to support both request/response model on HTTP and pub/sub on MQTT
 - providing observation context definition as the supplement for the aggregated data e.g. linking aggregated in NetCDF/Zarr/EDR API to the Sensor and Location.
 - use of ODATA clients

 ## How to implement

As the API is open one can choose to:
 - use hosted environment like the [PSNC implementation with data hosting](https://grlc-dpi-enabler-demeter.apps.paas-dev.psnc.pl/api-git/ILIAD-ocean-twin/JF-API/#/json/get_Observations) that can consume file based data like CSV. The advantage is this service provides integration with the Ocean Information Model given.
 - setup the known implementations from the [STA website](https://ogcapi.ogc.org/sensorthings/), it requires integration with Ocean Information Model in own way. The simplest one is to add JSON-LD context definition as the reference
 - implement the service based on the [OpenAPI definition - work in progress](https://app.swaggerhub.com/apis/PZB/Iliad-simplified-SensorThings-API/). OpenAPI tools can generate server stub for number of languages. Stub needs to be filled with logic querying data from the back-end.
 - implement hybrid solution that can be
  - reference implementation with the default endpoint replaced by own database



Extensions of the API shall be defined using the [OGC Building Block for STA](https://github.com/ogcincubator/bblocks-sta) template to ensure OIM integration.

## Iliad API compliance

Iliad proposes following extensions to the STA API:
- [mandatory] OIM alignment with context definition or inline alignment
- Capabilities declaration based on the OGC API Commons
- extensions for the STA payload formalised based on the [OGC Building Block for STA](https://github.com/ogcincubator/bblocks-sta)

### OIM alignment

Ocean Information Model alignment means terms used in the payload has definitions explicitly referred so that various APIs use the sam definitions for the common entities supporting both human and machine readability.
Example alignment through context:
```
{
  "@iot.id": 1,
  "@iot.selfLink": "http://example.org/v1.1/Observations(1)",
  "FeatureOfInterest@iot.navigationLink": "Observations(1)/FeatureOfInterest",
  "Datastream@iot.navigationLink": "Observations(1)/Datastream",
  "phenomenonTime": "2014-12-31T11:59:59.00+08:00",
  "resultTime": "2014-12-31T11:59:59.00+08:00",
  "result": 70.4,
  "@context": "https://ogcincubator.github.io/bblocks-sta/build/annotated/bbr/template/Observation/context.jsonld"
}
```
In this example, the only change in the payload is the context link that explain all the data. This way, data can be interpreted unambiguously based on known ontologies in [RDF](https://ogcincubator.github.io/bblocks-sta/build/tests/bbr/template/Observation/example_1_1.ttl)

```
@prefix sosa1: <https://www.w3.org/TR/vocab-ssn/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] sosa1:hasSimpleResult 7.04e+01 ;
    sosa1:phenomenonTime "2014-12-31T11:59:59.00+08:00" ;
    sosa1:resultTime "2014-12-31T11:59:59.00+08:00" .

```

Alignment can be done by:
- [context](https://ogcincubator.github.io/bblocks-sta/bblock/ogc.bbr.template.Observation/json-ld) defined as linked resource, it makes payload limited and benefit fully from JSON simplicity
- inline contextualisation [PSNC implementation](https://grlc-dpi-enabler-demeter.apps.paas-dev.psnc.pl/api-git/ILIAD-ocean-twin/JF-API/#/json/get_Observations)


Base building blocks from OGC provide the context files for the core standard. Extensions of the context shall inherit these definitions but can extend it according to the use case. Building Blocks register provide functionality to build the context based on the provided ontologies and is recommended tool for own context definitions.

### Data model profiled

Usual case is that observation DataStream, Sensor, Observations for the individual use case provide additional information. Example extended Observation:
```
{
  "@iot.id": 1,
  "@iot.selfLink": "http://example.org/v1.1/Observations(1)",
  "FeatureOfInterest@iot.navigationLink": "Observations(1)/FeatureOfInterest",
  "Datastream@iot.navigationLink":"Observations(1)/Datastream",

  "phenomenonTime": "2014-12-31T11:59:59.00+08:00",
  "resultTime": "2014-12-31T11:59:59.00+08:00",
  "result": 70.4
  "approved": true
}
```
To make API OIM compliant:
- one SHALL define extended context definition inheriting from [base one](https://github.com/ogcincubator/bblocks-sta/tree/master).
 - one MAY refer to the new schema from the API definition, for example openAPI YAML schema for HTTP code 200

 OGC Building blocks register toolset helps to define the whole profile including: schema, context, examples, description.

 ### Capabilities declaration

 Following recent practices in the OGC APIs that is not yet adopted in the OGC STA, proposed extension include coherent:
 -  [conformance declaration](https://app.swaggerhub.com/apis/PZB/Iliad-simplified-SensorThings-API/1.0.0#/Capabilities/getRequirementsClasses),
 - [landing page](https://app.swaggerhub.com/apis/PZB/Iliad-simplified-SensorThings-API/1.0.0#/Capabilities/getLandingPage) with all the relevant consequent links,
 - api definition link.

 ```
 \ - landing page
 \conformance - conformance declaration, it is potentially redundant with the STA conformance declaration but inline with OGC Commons.
 \api - api definition

 ```

Simplified API defined under [SwaggerHub](https://app.swaggerhub.com/apis/PZB/Iliad-simplified-SensorThings-API/1.0.0#/) is conformant to following classes:
All the main entities:
http://www.opengis.net/spec/iot_sensing/1.1/conf/datamodel/thing
http://www.opengis.net/spec/iot_sensing/1.1/conf/datamodel/location
http://www.opengis.net/spec/iot_sensing/1.1/conf/datamodel/datastream
http://www.opengis.net/spec/iot_sensing/1.1/conf/datamodel/sensor
http://www.opengis.net/spec/iot_sensing/1.1/conf/datamodel/observed-property
http://www.opengis.net/spec/iot_sensing/1.1/conf/datamodel/observation
http://www.opengis.net/spec/iot_sensing/1.1/conf/datamodel/feature-of-interest
http://www.opengis.net/spec/iot_sensing/1.1/conf/datamodel/entity-control-information
http://www.opengis.net/spec/iot_sensing/1.1/conf/resource-path
http://www.opengis.net/spec/iot_sensing/1.1/conf/resource-path/resource-path-to-entities

Selected request operations:
http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data
http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/order

http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/select

http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/status-code

http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/query-status-code

http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/orderby

http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/top

http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/skip

http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/count

http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/filter

http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/pagination


Simplified API does not have to be conformant to following, while it depends on the use case:
For reference implementations deployment following will be included:
http://www.opengis.net/spec/iot_sensing/1.1/conf/datamodel/historical-location
http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/expand
http://www.opengis.net/spec/iot_sensing/1.1/conf/data-array
http://www.opengis.net/spec/iot_sensing/1.1/conf/data-array/data-array
http://www.opengis.net/spec/iot_sensing/1.1/conf/multi-datastream
http://www.opengis.net/spec/iot_sensing/1.1/conf/multi-datastream/properties
http://www.opengis.net/spec/iot_sensing/1.1/conf/multi-datastream/relations
http://www.opengis.net/spec/iot_sensing/1.1/conf/multi-datastream/constraints
http://www.opengis.net/spec/iot_sensing/1.1/conf/batch-request
http://www.opengis.net/spec/iot_sensing/1.1/conf/batch-request/batch-request
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-update-delete
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-update-delete/create-entity
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-update-delete/link-to-existing-entities
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-update-delete/deep-insert
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-update-delete/deep-insert-status-code
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-update-delete/update-entity
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-update-delete/delete-entity
http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/built-in-filter-operations
http://www.opengis.net/spec/iot_sensing/1.1/conf/request-data/built-in-query-functions
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-update-delete/historical-location-auto-creation
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-update-delete/update-entity-put
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-update-delete/update-entity-jsonpatch

For streaming data interface following shall be implemented
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-observations-via-mqtt
http://www.opengis.net/spec/iot_sensing/1.1/conf/create-observations-via-mqtt/observations-creation
http://www.opengis.net/spec/iot_sensing/1.1/conf/receive-updates-via-mqtt
http://www.opengis.net/spec/iot_sensing/1.1/conf/receive-updates-via-mqtt/receive-updates
