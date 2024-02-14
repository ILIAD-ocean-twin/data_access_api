# Iliad Data Access API

Iliad Data Access API is based on the OGC EDR API, that is designed to access MetOcean data through convenient API that supports coverage and vector data, Iliad profile will be defined. The profile consist of the schema profile, sample configurations of the reference implementations and persistent playground hosted.

Federated architecture of the Digital Twin can require several types of the interfaces:
* data and services discovery: allows to browse and filter resources useful for the twin or being its products and navigate to access services; it is usually realised by the interfaces allowing for metadata browsing, that is realised by the catalogue services (T4.1 and T4.3). To ensure harmonised twin use, it is important to align metadata on the catalogue and access levels.
* data access: twin data embraces source data from project sensors, 3rd party data exposed by intermediary hubs and data generated from models,
* services access: access to applications executing Twin models like forecasts and simulations, but also analytical tools generating compositions of the data; in the project it is covered by the WP5. Alignment with DTO API concerns input and output metadata alignment and potentially mechanism that generated data can be exposed via DTO data access APIs.
* geospatial user feedback (GUF): allows users to report not only generic comments and ratings about a specific dataset, but it allows them to document several aspects related to the purpose of that feedback, to share publications connected with that data or describe specific usages. In this last case, users can also provide documentation of their usage of the target resource(s) as well as report issues or share specific codes or execution sentences. All this information can be referred to a whole dataset/product or to a specific geographical area that can be also documented. GUF standard documentation and schemas have been updated to [version 2](https://github.com/opengeospatial/Geospatial-User-Feedback/tree/main), which extends GUF 1.0 to allow storing reproducible usage. Moreover, an OPEN OGC API based on OGC API records and its implementation in the NiMMbus system (nimmbus.cat) as well as a new standard for GUF JSON codification are being developed.

This repository focuses on the data access APIs that is not covered by other tasks but shall be semantically integrated with these. At the same time, data models and querying shall be adoptable to the various protocols like event streaming and catalogs.

## Groundwork

Based on the discussions identified ILIAD data includes various types:
* Observations: include both in-situ measurements and citizen science observations
* vector data: like Protected Areas, simplified time series measurements data, windfarms infrastructure,
* Coverages: both numerical data grids in NetCDF/HDF formats and raster files in GeoTiff , also trajectories data in NetCDF[reference] files are close to the CIS model [reference]

Some of the pilots already provide data through legacy APIs like OGC WCS, WMS, WFS, OpenDAP, ERRDAP API. Variety of APIs can express variety of needs and applications that uses these accesses.

The approach taken is to define core suite of standard elements that can express the data in the alignment with the Ocean Information Model. OGC Environmental Data Retrieval API was selected as the starting point being modern interface developed few years ago in line with the ICT de-facto industry standards of APIs definition (Swagger/OpenAPI), allowing for semantic ‘uplift’ through JSON-LD extension of the poorly structured JSON, support of the raster and vector data, support of the Met Ocean and Marine Working groups and agencies behind.

## Data Access APIs SUITE

Considering all the recognised scenarios, the API suite can contain:
* fine grained access to observations based on the OGC Sensor Things API, optionally with STA+ extension for the Citizen Science
* aggregated representation like coverages  of the observations and models outcomes based on the Environmental Data Retrieval API in the CoverageJSON/NetCDF/Zarr formats
* vector features representation based on OGC API Features that could represent locations, physical installations but also be an alternative observations representation consumable by wider range of client applications
* catalog based on Records API/STAC with relevant extensions for metadata Description
* services API based on the OGC API Processes and Application Package

All the APIs shall follow several requirements for the alignments:
* be integrated with OIM based on the generic templates.
* follow Geospatial Data on the Web Best Practices, in particular: unique URIs that are refereable between various data Sources

## SensorThings APIs

[SensorThings API](https://ogcapi.ogc.org/sensorthings/) is the OGC standard endorsed as the INSPIRE good practice to share observations data. It is compliant with the ISO 19156/OGC Observations & Measurements standards.
Entry level descriptions of the API are available on the [Wikipedia](https://en.wikipedia.org/wiki/SensorThings_API)

### Use cases

STA is flexible standard useful in particular for:
 - exposing observations with all the Sensor, Observed Properties, Location in a flexible way so that client can build the query to access observations in the light way and get the whole related data though simple queries (like joins in SQL). Example STA demo is available on the [PSNC infrastruture](https://grlc-dpi-enabler-demeter.apps.paas-dev.psnc.pl/api-git/ILIAD-ocean-twin/JF-API/)
 - providing observation as the data stream as STA was design to support both request/response model on HTTP and pub/sub on MQTT
 - providing observation context definition as the supplement for the aggregated data e.g. linking aggregated in NetCDF/Zarr/EDR API to the Sensor and Location.
 - use of ODATA clients

 ### How to implement

As the API is open one can choose to:
 - use hosted environment like the [PSNC implementation with data hosting](https://grlc-dpi-enabler-demeter.apps.paas-dev.psnc.pl/api-git/ILIAD-ocean-twin/JF-API/#/json/get_Observations) that can consume file based data like CSV. The advantage is this service provides integration with the Ocean Information Model given.
 - setup the known implementations from the [STA website](https://ogcapi.ogc.org/sensorthings/), it requires integration with Ocean Information Model in own way. The simplest one is to add JSON-LD context definition as the reference
 - implement the service based on the [OpenAPI definition - work in progress](https://app.swaggerhub.com/apis/PZB/Iliad-simplified-SensorThings-API/). OpenAPI tools can generate server stub for number of languages. Stub needs to be filled with logic querying data from the back-end.
 - implement hybrid solution that can be
  - reference implementation with the default endpoint replaced by own database



Extensions of the API shall be defined using the [OGC Building Block for STA](https://github.com/ogcincubator/bblocks-sta) template to ensure OIM integration.

### Iliad API compliance

Iliad proposes following extensions to the STA API:
- Capabilities declaration based on the OGC API Commons
- OIM alignment with context definition or inline alignment
- extensions for the STA payload formalised based on the [OGC Building Block for STA](https://github.com/ogcincubator/bblocks-sta)


#### Capabilities declaration

Following recent practices in the OGC APIs that is not yet adopted in the OGC STA, proposed extension include coherent:
-  [conformance declaration](https://app.swaggerhub.com/apis/PZB/Iliad-simplified-SensorThings-API/1.0.0#/Capabilities/getRequirementsClasses),
- [landing page](https://app.swaggerhub.com/apis/PZB/Iliad-simplified-SensorThings-API/1.0.0#/Capabilities/getLandingPage) with all the relevant consequent links,
- api definition link.

```
\ - landing page
\conformance - conformance declaration
\api - api definition

```
#### OIM alignment

Ocean Information Model alignment means definitions used in the payload has definitions explicitly defined so that various APIs use the sam definitions for the common entities.
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

#### Data model profiled

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

## Coverage Data Access APIs Technical description

Base EDR is built on top of the OpenAPI specification and OGC APIs practice to support hierarchical, filterable and queryable discovery. Default encoding of the OGC APIs is JSON for M2M with HTML for human-machine interfaces (HMI) support. EDR supports binary data in NetCDF as well.
EDR API reference documentation is:
 - [EDR landing page with specification](https://ogcapi.ogc.org/edr/)
 - [GitHub repository with API introduction](https://github.com/opengeospatial/ogcapi-environmental-data-retrieval)

Additional learning materials
 - [Video FOSS4G introduction to EDR and other OGC APIs](https://youtu.be/ctoyVX2C07U?t=712)

In addition, OGC API Records is proposed in Iliad for metadata repository of datasets and data, and Sensor Things API for the sensor data and measurements.

Iliad APIs contains:
 - behavioural data exchange model reference to the core Standards
 - extensions proposed for the marine environment including data models and semantic uplift for the ocean Information Model support
 - alignment proposed for the selected legacy marine standards
 - example configurations of the API based on the reference implementations with proposed extensions
 - [TODO] schemas and validation guidelines and tools


 ### How to implement

 https://app.swaggerhub.com/apis/PZB/iliad-dto-test-bblocks/1.0.1#/

### Potential further time_steps

 - Catalog profiles aligned with the OIM. most probably based on the OGC API Records draft standards (as for end of 2023). the benefit would be to have STAC support given with STAC 1.0.0 version and option to define metadata of the STAC




### Main functions

Like other OGC APIs, EDR provides entry point landing page with:
 - `/` self-description of the interface and data in the metadata form
 - `/collections` - links to the data and collections
 - `/conformance` - conformance declaration defining which functionalities from the specifications are implemented in particular endpoint

Description of the endpoints is provided in the [API overview](https://ogcapi.ogc.org/edr/overview.html)

Main resources that are exposed in the Iliad EDR are:
 - coverages - each coverage file exposed as one collection, variables available as properties within collection. Data can be queried (trimmed) according to query parameter like cube or point
 - locations - fixed points or areas that defines details of the localisation related to the data gathered for given area. E.g. measurement/sensor localisation with the detailed information about the sensor inline or as link.
 - vector observations - point measurements, camera images and videos that are exposed by the APIs

 As the extension for non localised data, alignment with sensor description can be considered in the future.

EDR APIs supports filtering collections with bounding box, time extent. for more advanced queries, OGC API Records is recommended. As the extension of the OGC API Features, it can supports multiple properties including free text search and CQL queries.

EDR API supports querying data in [multiple ways] (https://docs.ogc.org/is/19-086r5/19-086r5.html#toc44)

### Multiple APIs

If multiple endpoints needs to be combined, reasonable approach is to organise them in the self-describing hierarchy. In this case root level landing page provides all the underlying links and conformance classes, while each of the sub-APIs referred has detailed information about the resources it exposes.

```
─/ <landing page>
 ├─ conformance <conformance classes listing both Features, Coverages/EDR and high-level STA conformance classes
 ├─ edr <combined OpenAPI definition for everything for data access>
 ├─ collections <OGC-API Records, with use-case specific views on the data>
 ├─ sta/v1.1 <STA interface, with detailed STA conformance classes on the landing page>
```
<sub> Example APIs suite </sub>

### Iliad extensions



## Relation to the other APIs and data formats

### Zarr

Zarr storage is getting popularity for the environmental data. It is inspired by the NetCDF and HDF formats providing access to multidimentional data adding chunking mechanism that enables access to selected chunks though HTPP range request. As legacy formats, it is not limited to geospatial information, while the profiles are expected to follow Climate and Forecast conventions and similar approach to the NCEI templates where relevant. Integration with the API includes:
* access to Zarr files through link from the catalog, which can be
* access to the groups of the Zarr file though API in the harmonised way in the same way CoverageJSON, NetCDF and other formats can be requested with trimming relevant for the specific API implementation
* semantic harmonisation through alignment to the ACDD and CF conventions

### SeaDataNet

SeaDataNet mapping will be defined in the /metadata.

### Spatio Temporal Asset Catalogue

Iliad Service layer can generate STAC files. They are not going to be directly integrated in the APIs, while some metadata can be passed to the data catalog.

### NCEI NetCDF

https://www.ncei.noaa.gov/netcdf-templates

### OpenDAP

### ERRDAP APIs
