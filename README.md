# Iliad Data Access API (T4.5)

Iliad Data Access API is based on the OGC EDR API, that is designed to access MetOcean data through convenient API that supports coverage and vector data, Iliad profile will be defined. The profile consist of the schema profile, sample configurations of the reference implementations and persistent playground hosted.

## Technical description

Base EDR is built on top of the OpenAPI specification and OGC APIs practice to support hierarchical, filterable and queryable discovery. Default encoding of the OGC APIs is JSON for M2M with HTML for human-machine interfaces (HMI) support. EDR supports binary data in NetCDF as well. Further extensions are possible.
In addition, OGC API Records is proposed in Iliad for metadata repository of datasets and data, and Sensor Things API for the sensor data and measurements.

Iliad APIs definition contains:
 - reference to the core Standards
 - extensions proposed for the marine environment including data models and semantic uplift for the ocean Information Model support
 - alignment proposed for the selected legacy marine standards
 - example configurations of the API based on the reference implementations with proposed extensions
 - [TODO] schemas and validation guidelines and tools



EDR API reference documentation is:
 - [EDR landing page with specification](https://ogcapi.ogc.org/edr/)
 - [GitHub repository with API introduction](https://github.com/opengeospatial/ogcapi-environmental-data-retrieval)

Additional learning materials
 - [Video FOSS4G introduction to EDR and other OGC APIs](https://youtu.be/ctoyVX2C07U?t=712)


### Main functions

Like other OGC APIs, EDR provides entry point landing page with:
 - `/` self-description of the interface and data in the metadata form
 - `/collections` - links to the data and collections
 - `/conformance` - conformance declaration defining which functionalities from the specifications are implemented in particular endpoint

Descritpion of the endpoints is provided in the [API overview](https://ogcapi.ogc.org/edr/overview.html)

Main resources that are exposed in the Iliad EDR are:
 - coverages - each coverage file exposed as one collection, variables available as properties within collection. Data can be queried (trimmed) according to query parameter like cube or point
 - locations - fixed points or areas that defines details of the localisation related to the data gathered for given area. E.g. measurement/sensor localisation with the detailed information about the sensor inline or as link.
 - vector observations - point measurements, camera images and videos that are exposed by the APIs

 As the extension for non localised data, alignemnt with sensor description can be considered in the future.

EDR APIs supports filtering collections with bounding box, time extent. for more advanced queries, OGC API Records is recommended. As the extestion of the OGC API Features, it can supports multiple properties including free text search and CQL queries.

EDR API supports querying data in [multiple ways] (https://docs.ogc.org/is/19-086r5/19-086r5.html#toc44)

### Multiple APIs

If multiple endpoints needs to be combined, reasonable approach is to organise them in the self-describing hierarchy. In this case root level landing page provides all the underlying links and conformance classes, while each of the sub-APIs refered has detailed information about the resources it exposes.

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

Reference EDR implementation supports

### SeaDataNet

SeaDataNet mapping will be defined in the /metadata.

### Spatio Temporal Asset Catalogue

Iliad Service layer can generate STAC files. They are not going to be directly integrated in the APIs, while some metadata can be passed to the data catalog.

### NCEI NetCDF

https://www.ncei.noaa.gov/netcdf-templates

### OpenDAP

### ERRDAP APIs
