# vector data

Vector data in Iliad represents observations, areas (like protected areas), cultural heritage spots.
Sometimes they are organised in the timeseries (observations from one sensor) and trajectories (particles tracking, but also relevant for vessel mounted observations).

Data can be serialised in number of formats like CSV, GeoJSON, GeoParquet but also NetCDF/Zarr and exposed by the web services like OGC WFS, OGC API Features/EDR, Sensor Things API.

Basic primitives used to represent features in Iliad are noe factored out into Cross Domain models https://ogcincubator.github.io/cross-domain-model/
SOS/SSN - e.g. Observation, FeatureOfInterest, ObservableProperty
QUDT - e.g. Quantity, Unit, also extends DCAT to ontology
RFD-DataCube - e.g. dimensions for structured representations like NetCDF

## vector data access using WFS

OGC Web Features Service is the well adopted standard exposed by multiple spatial data servers.
It is also supported by the typoical GIS solutions like QGIS.
Examples how the vector data can be consumed in the programatic environments from the WFS server directly and presented from the GML or JSON formats are in the [Jupyter notebook](examples/OGC_EDR/access_features_WFS.ipynb)

# Semantic enablement

WFS nor OGC API Features doe not define what the vectors represent. For that reason both of these standards propose the feature types. Features types can be defined together with the properties containing domain specific information. Example are the features types are proposed as the INSPIRE schemas. binding properties and features types to their meanings can be done though the semantic uplift and expressed with the namespaces (in XML/GML) or LD context (in the JSON encodings)

In this case RDF representation is needed while the data is in the raw format e.g. CSV file.
Uplift requries conversion to the semantic native format like RDF, TTL, JSON-LD or semanticaly enabled format that can be CSVW, GeoJson with LD context.
First ones are most generic, while former ones 

## RDF representation from raw data files

### Using Data Preparation and Intagration Pipelines
PSNC DPI tool has the predefined configurations for the CSV and NetCDF files with the vector data that with proper mapping to the OIM is regenerating both uplifted data and OGC compliant APIs.

Features
https://dpi-enabler-ui-test.apps.paas-dev.psnc.pl/pipeline/GENERIC/3d377d87-960c-4cac-84e1-54f2e31d944d/view

Observations - Jellyfish
https://dpi-enabler-ui-test.apps.paas-dev.psnc.pl/pipeline/Generic/69a59294-abb8-427c-8fb2-9e31a7443f68/view

Observation - Aquacultures
https://dpi-enabler-ui-test.apps.paas-dev.psnc.pl/pipeline/GENERIC/0e264854-2994-4120-88ad-7f6d2ebc3a42/view

### Using external context definitions

Vanilla setups of the WFS or OGC Feature services can be raised to the semantically enhanced 

[quict start with the CSV file exposed as Features](./examples/OGC_Features/README.md)

[example configuration](./examples/OGC_Features/example-config-observations.yml)
[example configuration](./examples/OGC_Features/example-config-observations_parquet.yml)

# Features API

WFS specification covers not only the data payload format but also query functions and discovery of capabilities.

In the new OGC APIs (OGC API Features and OGC EDR) are based on the OpenAPI schema of calls and resource based URLs organised in the hierarchy. EDR for vector data additionally proposes advanced query mechanisms and locations based organisation but inherits other Features functionalities

| Feature                          | WFS (Web Feature Service)                | OGC API - Features                      |
|----------------------------------|------------------------------------------|-----------------------------------------|
| **Standard Type**                | XML-based OGC standard                   | RESTful OGC standard                    |
| **Data Format**                  | GML (default), XML, sometimes GeoJSON    | GeoJSON (default), HTML, JSON           |
| **Protocol**                     | HTTP with XML requests/responses         | HTTP with RESTful endpoints             |
| **Ease of Use**                  | Complex, requires XML parsing            | Simple, developer-friendly              |
| **Interoperability**            | Widely supported in legacy systems       | Better suited for modern web apps       |
| **Filtering**                    | OGC Filter Encoding (XML-based)          | CQL (Common Query Language)             |
| **Pagination & Sorting**        | Limited support                          | Built-in support                        |
| **OpenAPI Support**             | No                                        | Yes                                     |
| **Versioning**                   | Multiple versions (1.0, 1.1, 2.0)        | Modular and versioned via OpenAPI       |
| **Security**                     | Basic HTTP auth, custom implementations  | OAuth2, modern web security standards   |
| **Implementation Complexity**   | Higher due to XML and legacy standards   | Lower due to REST and JSON              |
| **Use Case Suitability**        | Desktop GIS, legacy enterprise systems   | Web apps, cloud-native environments     |
| **Extensibility**                | Limited                                  | Highly extensible via OpenAPI           |



Web parameters mappings

| Feature / Parameter              | WFS (Web Feature Service)                | OGC API - Features                      |
|----------------------------------|------------------------------------------|-----------------------------------------|
| **Standard Type**                | XML-based OGC standard                   | RESTful OGC standard                    |
| **Data Format**                  | GML (default), XML, sometimes GeoJSON    | GeoJSON (default), HTML, JSON           |
| **Protocol**                     | HTTP with XML requests/responses         | HTTP with RESTful endpoints             |
| **Request Type**                 | POST/GET with XML payloads               | GET with query parameters               |
| **Feature Retrieval**            | `GetFeature`                             | `/collections/{collectionId}/items`     |
| **Filtering**                    | `Filter` (OGC Filter Encoding)           | `filter` (CQL - Common Query Language)  |
| **Bounding Box Query**           | `<BBOX>` in XML                          | `bbox=minLon,minLat,maxLon,maxLat`      |
| **Spatial Reference System**     | `srsName`                                | `crs`                                    |
| **Output Format**                | `outputFormat` (e.g., `application/json`) | `f` (e.g., `f=geojson`)                 |
| **Property Selection**           | `<PropertyName>`                         | `properties=prop1,prop2`                |
| **Sorting**                      | `<SortBy>`                               | `sortby=propertyName`                   |
| **Pagination**                   | `startIndex`, `maxFeatures`              | `limit`, `offset`                       |
| **Feature Count**                | `resultType=hits`                        | `limit=0` or metadata endpoint          |
| **Versioning**                   | `version=1.0.0`, `2.0.0`                 | Defined via OpenAPI spec                |
| **Security**                     | Basic Auth, custom implementations       | OAuth2, API keys                        |
| **OpenAPI Support**              | ❌                                        | ✅                                       |
| **Ease of Integration**          | Complex XML parsing                      | Simple REST/JSON                        |

Now, the mapping of the calls can be generated based on the following table or using pygeoapi with the WFS as the backend service.

| OGC API - Features Endpoint / Parameter             | Equivalent WFS Operation / Parameter             | Notes                                                                 |
|-----------------------------------------------------|--------------------------------------------------|-----------------------------------------------------------------------|
| `GET /collections`                                  | `GetCapabilities`                                | Lists available feature collections / layers                         |
| `GET /collections/{id}`                             | `DescribeFeatureType`                            | Describes schema of a specific feature type                          |
| `GET /collections/{id}/items`                       | `GetFeature`                                     | Retrieves features from a collection                                 |
| `bbox=minLon,minLat,maxLon,maxLat`                  | `<BBOX>` filter in `GetFeature`                  | Spatial filter                                                        |
| `filter=property=value` (CQL)                       | `<Filter>` with `<PropertyIsEqualTo>`            | Attribute filter                                                      |
| `limit=n`                                           | `maxFeatures=n`                                  | Limits number of returned features                                   |
| `offset=n`                                          | `startIndex=n`                                   | Pagination offset                                                     |
| `sortby=propertyName`                               | `<SortBy>`                                       | Sorts results by property                                             |
| `properties=prop1,prop2`                            | `<PropertyName>`                                 | Selects specific properties to return                                |
| `crs=EPSG:4326`                                     | `srsName=EPSG:4326`                              | Coordinate reference system                                           |
| `f=geojson`                                         | `outputFormat=application/json`                  | Specifies output format                                               |
| `GET /collections/{id}/items?limit=0`               | `resultType=hits`                                | Returns only feature count                                            |

Pygeoapi implementation takes care of the root ('/') and collection level ('/collection/[collection name]') metainformation and all the API linkages.
profiles of the fetures with the Feature Types can be added with the templating functionality like in the [pygeoapi config](examples/Observations_Features/pygeoapi-EDR-observations.yml