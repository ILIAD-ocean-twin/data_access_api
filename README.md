# Iliad Data Access API

Iliad Data Access API is based on the OGC API suite, which is designed to share and access various kinds of spatiotemporal data through convenient API that supports coverage and vector data, Iliad profile will be defined. The profile consists of the schema profiles, sample configurations of the reference implementations, and persistent playground hosted.


The federated architecture of the Digital Twin can require several types of interfaces:
* data and services discovery: allows browsing and filtering resources useful for the twin or its products and navigating to access services; it is usually realized by the interfaces allowing for metadata browsing, which is realized by the catalog services (T4.1 and T4.3). To ensure harmonized twin use, it is important to align metadata on the catalog and access levels.
* data access: twin data embraces source data from project sensors, 3rd party data exposed by intermediary hubs, and data generated from models,
* services access: access to applications executing Twin models like forecasts and simulations, but also analytical tools generating compositions of the data; in the project it is covered by the WP5. Alignment with DTO API concerns input and output metadata alignment and potential mechanisms that generated data can be exposed via DTO data access APIs.
* geospatial user feedback (GUF): allows users to report not only generic comments and ratings about a specific dataset, but it allows them to document several aspects related to the purpose of that feedback, to share publications connected with that data, or to describe specific usages. In this last case, users can also provide documentation of their usage of the target resource(s) as well as report issues or share specific codes or execution sentences. All this information can be referred to a whole dataset/product or to a specific geographical area that can be also documented. GUF standard documentation and schemas have been updated to [version 2](https://github.com/opengeospatial/Geospatial-User-Feedback/tree/main), which extends GUF 1.0 to allow storing reproducible usage. Moreover, an OPEN OGC API based on OGC API records and its implementation in the NiMMbus system (nimmbus.cat), as well as a new standard for GUF JSON codification, are being developed.


This repository focuses on the data access APIs that is not covered by other tasks but shall be semantically integrated with these. At the same time, data models and querying shall be adoptable to the various protocols like event streaming and catalogs.

# quick start

Clone this repostory and the pygeapi Iliad fork

```
clone https://github.com/pzaborowski/pygeoapi.git
clone https://github.com/ILIAD-ocean-twin/data_access_api.git
```

Set the environment variable paths in the data_access_api/examples/start_demo or environment and uncomment:

```
#export Iliad_api_repo=[path to the data_access_api repository]
#export Iliad_pygeoapi_repo=[path to the pygeoapi repository]
```

run the data_access_api/examples/start_demo

```
chmod +x data_access_api/examples/start_demo
./start_demo
```


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
* aggregated representation like coverages  of the observations and models outcomes based on the Coverages and Environmental Data Retrieval API in the CoverageJSON/NetCDF/Zarr formats
* vector features representation based on OGC API Features that could represent locations, physical installations but also be an alternative observations representation consumable by wider range of client applications
* catalog based on Records API/STAC with relevant extensions for metadata Description
* services API based on the OGC API Processes and Application Package
* direct access to the Cloud Optimised data stored in Zarr
* OpenDAP interface to NetCDF data


| Data Access Protocols | dataset discovery support | extended source information | access method | Semantic support of OIM |
| --------------------- | ----------------- | ----------------- | ----------------- | ----------------- |
| [SensorThingsAPI](SensorThingsAPI.md) | no general level information | all the fine grained metadata available for sensors, FoI, Thing | OData/HTTP access to granular data, filtering and grouping | [OIM](https://github.com/ILIAD-ocean-twin/OIM) LD context/entailment |
| [OGC API Coverages/WCS](CoveragesAPI.md) | OGC API compliant | limited in standard, available though extensions and the [OIM](https://github.com/ILIAD-ocean-twin/OIM) alignment | OpenAPI/HTTP, access to aggregates with trimming and resolution scaling | [OIM](https://github.com/ILIAD-ocean-twin/OIM) LD context/entailment |
| [OGC API EDR](OGC_EDR/README.md) | OGC API compliant | limited in standard, available though extensions and the [OIM](https://github.com/ILIAD-ocean-twin/OIM) alignment | OpenAPI/HTTP, access to aggregates with trimming | though [OIM](https://github.com/ILIAD-ocean-twin/OIM) LD context/entailment |
| [OGC API Tiles/WM(T)S](Tiles.md) | OGC API compliant | limited in standard, available though extensions and the [OIM](https://github.com/ILIAD-ocean-twin/OIM) alignment | OpenAPI/HTTP, access to aggregates as tiles with trimming and resolution scaling | [OIM](https://github.com/ILIAD-ocean-twin/OIM) LD context/entailment |
| [CF-storages](Archives.md) | in-file DDS metadata | file and variable level key-values | storage specific | various |
| [OpenDAP](https://www.opendap.org/) | DDS based | NetCDF-like | HTTP | NcML |

### Metadata role in data access

Metadata describing data assets is in various level integrated in the APIs s briefly mentioned in the table above.
Most modern Web API like SensorThingAPI, Features API include generic layer metadata () in the standard 


### Spatial APIs and spatial cloud native storages

Recent review of the storage formats in the spirit of the cloud nativeness has consolidated as several data formats (like Zarr, Cloud Optimised Geotiff, GeoParquet, NetCDF+Kerchunk) that enable random access to data [chunks](https://en.wikipedia.org/wiki/Chunk_(information)). These formats can be indexed and accessed directly without dedicated application level server. It can be implemented as "serverless" data access which has several pros and cons.

* potentially lower cost of setup and maintenance - e.g. put data in the web bucket.
* trade of server side preprocessing for simplicity
* server side multiresolution is provided on cost of storage instead of computing
* data push driven data management vs information driven - on default, data entities are associated with provision pipelines not client applications
* not designed for web and other light applications - visualisation, scaling
* trade of caching efficiency vs random access
* easy storage driven access management and control, not obvious are 

## Iliad specificity

Iliad efforts in the APIs development are tightly aligned to the standardisation processes, so the intention is not to design totaly new technical stack, but more to contribute to the existing and emerging standards with the experiences taken from the project and support standards APIs development where they does not exist.

However, with all the web APIs shall follow several requirements for the alignments:
* be integrated with [OIM](https://github.com/ILIAD-ocean-twin/OIM) based on the generic templates
* follow [Spatial Data on the Web Best Practices](https://www.w3.org/TR/sdw-bp/), in particular: unique URIs that are refereable between various data sources

## SensorThings APIs

[SensorThings API](https://ogcapi.ogc.org/sensorthings/) is the OGC standard endorsed as the INSPIRE good practice to share observations data. It is compliant with the ISO 19156/OGC Observations & Measurements standards.
Entry level descriptions of the API are available on the [Wikipedia](https://en.wikipedia.org/wiki/SensorThings_API)

### Use cases

STA is flexible standard useful in particular for:
 - exposing observations with all the Sensor, Observed Properties, Location in a flexible way so that client can build the query to access observations in the light way and get the whole related data though simple queries (like joins in SQL). Example STA demo is available on the [PSNC infrastruture](https://grlc-dpi-enabler-demeter.apps.paas-dev.psnc.pl/api-git/ILIAD-ocean-twin/JF-API/)
 - providing observation as the data stream as STA was design to support both request/response model on HTTP and pub/sub on MQTT
 - providing observation context definition as the supplement for the aggregated data e.g. linking aggregated in NetCDF/Zarr/EDR API to the Sensor and Location.
 - use of ODATA clients

[Implementation steps](./SensorThingsAPI.md)

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



# Relation to the other standards, APIs and data formats

### ISO TC211 19* standards

OGC standards are well aligned to the ISO TC211 standards suite and largely implement standards like 19115 metadata model. in some cases, OGC standards are endorsed as ISO (OGC Features API) and sometimes they are jointly developed (Observation & Measurements used by the STA data model).

### DCAT 

Iliad profiles of the metadata documented in the Iliad Building Blocks register refers to the DCAT ontology though OIM definitions or directly. It is part of the canonical information model for dataset description.

### Zarr

Zarr storage is getting popularity for the environmental data. It is inspired by the NetCDF and HDF formats providing access to multidimentional data adding chunking mechanism that enables access to selected chunks though HTPP range request. As legacy formats, it is not limited to geospatial information, while the profiles are expected to follow Climate and Forecast conventions and similar approach to the NCEI templates where relevant.


Integration with the API includes:
* access to Zarr files through link from the catalog
* access to the groups of the Zarr file though API in the harmonised way in the same way CoverageJSON, NetCDF and other formats can be requested with trimming relevant for the specific API implementation
* semantic harmonisation through alignment to the ACDD, CF conventions and OIM


### SeaDataNet

TBD but SeaDataNet is a combination of the ISO19115 profile for metadata, CF and own encodings for tabular data, so the overlap is in the abovementioned standards

### Spatio Temporal Asset Catalogue (STAC), Catalog Web Service (CSW) and Records API

With the recently published OGC API Records, that is a superset of STAC (STAC is de-facto profile of Records), they became of interest of Iliad as potenially including all the metadata.

Iliad Service layer can generate STAC files. They are not going to be directly integrated in the APIs, while some metadata can be passed to the data catalog.

### CF convention and NCEI NetCDF

[CF convention](https://cfconventions.org/conventions.html) defines profiles of the NetCDF format guiding how to use them for geospatial data (based on the climate and foreasts use cases). For example it define how to use dimensions, variables and attributes for geospatial data and what is relation between them (e.g. interpolation of measurement in variable and metadata in attributes).

NetCDF NCEI templates are NetCDF profiles aligned with the CF convention for number of use cases like time series, grided data, trajectories etc.
https://www.ncei.noaa.gov/netcdf-templates

Both CF conventions and NCEI templates are used in the Iliad pilots to limited extent.
Iliad proposes new validation mechanisms for the native version of the CF representation in Zarr format. There are several implementations of the CF validators for NetCDF and Zarr data maintained, but:

* implementations of both direct file clients and web services has hard requirements where CF recommends only using units, standard names
* GeoZarr standard is coming with some metadata schemas that will allow for generic tools based validation.

### *DAP services

DAP services are user in several Iliad pilots using open implementations (THREDDS/ERDDAP).
The same implementations are used by CMEMS, EMODNet and NOAA. They expose selected OGC Web Services (WCS, WMS) already.
beyond that, DAP provide specific API for NetCDF like data both in request-response and streaming which is used out of the box in Iliad and is not part of considerations in this task.
DAP services uses NetCDF DDS for metadata discovery and variables in domain, which shall be aligned with the information model. Ususally it is done though CF alignemnt.

Beyond vanila DAP, ERDDAP proposes their own API which is a combination of catalog (like Records and opensearch) and trimming and rescaling (like WCS/Coverages/EDR). This is area of potential alignment of the implementations which could be done after OGC API Coverages publication.

# Acknowledgements

The work has been co-funded by the European Union, Switzerland and the United Kingdom under the Horizon Europe:
* [Iliad project](https://www.ogc.org/initiatives/iliad/) (GA 101037643)

