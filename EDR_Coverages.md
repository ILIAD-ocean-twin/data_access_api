# Coverages of gridded data

A coverage is a "function which returns values from its range for any direct position within its domain" (ISO 19123-1:2023)[https://www.iso.org/obp/ui/en/#iso:std:iso:19123:-1:ed-1:v1:en]. In this documents, focus is on the gridded coverages where the domain is multidimensional spatio-temporal grid, e.g. lon, lat, depth, time.

These files are often (but not exclusively) stored in the binary formats like NetCDF and recently Zarr files. Applications can access these files directly at whole or using chunking mechanisms (directly in Zarr, using translation with Kerchunk/Icechunk index files).
Current work on the GeoZarr community estabilished also as the OGC Standard Working Group will stabilise the interface that can be shared among these implementations and include constrints from the Climate and Forecasts convention and metadata from STAC extensions.
The effort is to minimise incompliance with the grid data NCEI profiles, so Iliad is using both approaches but base on the cloud native transformations of the abovementioned conventions.

On top of the storages of any kind, the value of the harmonised APIs is:
 - storage agnostic interface
 - alignment with the other services in metadata, self descriptiveness and data organisation including OGC APIs, STAC
 - web optimisation with on-the fligh multi-resolution support (selected), tiling (selected)
 - transfer optimisation with on-the flight data trimming using only coordinates
 - support of multiple reference systems on the flight

 All in all, web services and APIs simplifies client implementations (need to support only WS/API), reduce skills needed by the user like geo transformations, limit storage and transfer needs (no need to store resolution piramids, various CRSes) on the cost of service requirements.

## EDR API setup

This API exposes simplified version of the coverages API (see below) with the:
 - OpenAPI and resource based service easy to integrate with access management, security layers
 - OGC Commons and OGC Features aligned API structure
 - multiple queries options available
 - coverageJSON, NetCDF, Zarr output payload and HTML human interface
 - flexible and extendible data structures support
 - embracing both vector and grid data under one interface,
 - (recenty) Pub-Sub protocol

API can be set easily on top of the abovementioned storage formats based on the reference implementation
[example EDR configuration](./examples/OGC_EDR/README.md)

## Coverage WS, Maps and Tiles

Maps and Tiled maps are popular services optimised for the web access to the coverage data. These are often used for raster generation/access for visualisation.
WMS and [OGC API Maps](https://ogcapi.ogc.org/maps/), WMTS and [OGC API Tiles](https://ogcapi.ogc.org/tiles/overview.html) are examples of popular implementations supported by multiple open and proprietary GIS software inlcuding servers, web and descktop clients - [certified products](https://portal.ogc.org/public_ogc/compliance/compliant.php).

Web Coverage Service and [OGC API Coverage draft](https://ogcapi.ogc.org/coverages/) are the popular rich interfaces to access trimmed and potentially rescaled 

Several of the Iliad partners support above services, mostly as legacy OGC Web Services inlcuding:
 - ADAM platofrm by Meeo
 - Terrasigme platform
 - THREDDS servers offered by Ramani and Hydromod
 
 they are also provided by the CMEMS and EMODNet either directly via ERDDAP or with the other GIS aplications.

To implement modern APIs on the legacy service, pygeoapi can be used as the proxy.
as the data can be heavy, it shall be considered the proxy maps the binary data requests directly to the legacy service and does not process files.
[example Maps on WMS configuration](./examples/OGC_API_MapsOnWMS/example-config-Tiles.yml)

Semantisation of the data can be either implemented directly in the storages using Ramani service or on the fligh with the OIM+ [OGC Building blocks annotations](https://ogcincubator.github.io/iliad-apis-features/bblock/ogc.hosted.iliad.api.features.coverageJSON) using LD-context in the payload or the response headers according to the [W3C JSON-LD specification](https://www.w3.org/TR/json-ld11/#interpreting-json-as-json-ld)


## OGC APIs vs OGC Web services

OGC API proxy implementation enriches the legacy API with the modern services.

| **Functionality**        | **WMS (1.3.0)**                         | **OGC Maps API (1.0.0)**                         | **Notes**                                                                 |
|-------------------------|-----------------------------------------|--------------------------------------------------|--------------------------------------------------------------------------|
| **Get Map**             | `REQUEST=GetMap`                        | `GET /map`                                       | Retrieves a map image; Maps API uses RESTful endpoint.                   |
| **Get Capabilities**    | `REQUEST=GetCapabilities`              | `GET /conformance`, `GET /`                      | Maps API splits capabilities into conformance and landing page.         |
| **Layer Selection**     | `LAYERS=layer1,layer2`                 | `collections=layer1,layer2`                      | Maps API uses `collections` parameter.                                   |
| **Spatial Subsetting**  | `BBOX=minx,miny,maxx,maxy`             | `bbox=minx,miny,maxx,maxy` or `subset=...`       | Maps API supports both `bbox` and flexible `subset` syntax.             |
| **CRS Selection**       | `CRS=EPSG:4326`                        | `crs=EPSG:4326`                                  | Similar usage; Maps API also supports custom projections.               |
| **Image Format**        | `FORMAT=image/png`                     | `Accept: image/png` or `f=image/png`             | Maps API uses HTTP headers or query param `f`.                          |
| **Image Size**          | `WIDTH=800&HEIGHT=600`                 | `width=800&height=600`                           | Same meaning; Maps API also supports `scale-denominator`.               |
| **Transparency**        | `TRANSPARENT=TRUE`                     | `transparent=true`                               | Maps API adds `void-transparent` for areas with no data.                |
| **Background Color**    | `BGCOLOR=0xFFFFFF` (vendor-specific)   | `bgcolor=0xFFFFFF`                               | Standardized in Maps API.                                               |
| **Time Filtering**      | `TIME=2020-01-01/2020-01-31`           | `datetime=2020-01-01/2020-01-31` or `subset=time`| Maps API supports ISO8601 and flexible subsetting.                      |
| **Feature Info**        | `REQUEST=GetFeatureInfo`               | Not part of Maps API Core                        | Feature info is handled in other OGC APIs (e.g., Features API).         |
| **Legend Graphic**      | `REQUEST=GetLegendGraphic`             | Not part of Maps API Core                        | May be added in future Maps API extensions.                             |
| **Styled Maps**         | `STYLES=default`                       | `style=default`                                  | Maps API supports styled maps via dedicated requirements class.         |


## OGC API vs ERDDAP API

| **Functionality**         | **OGC EDR API**                                      | **ERDDAP API**                                      | **Notes**                                                                 |
|--------------------------|------------------------------------------------------|-----------------------------------------------------|--------------------------------------------------------------------------|
| **Discovery**            | `/collections`, `/conformance`, `/api`               | `/info/index.html`, `/search/index.html`            | Both provide metadata and dataset discovery.                             |
| **Data Access**          | `/collections/{id}/position`, `/area`, `/trajectory` | `/griddap/{dataset}.fileType?query`                 | EDR uses RESTful paths; ERDDAP uses query strings.                       |
| **Subsetting**           | `bbox`, `subset=Lat(10:20)`                          | `latitude>=10&latitude<=20`                         | EDR uses `subset`; ERDDAP uses logical expressions.                      |
| **Temporal Filtering**   | `subset=time("2020-01-01":"2020-01-31")`             | `time>=2020-01-01&time<=2020-01-31`                 | Both support ISO 8601 time filtering.                                   |
| **Parameter Selection**  | `parameter_names=B02,B03`                            | `variable1,variable2,...`                           | EDR uses `parameter_names`; ERDDAP uses variable names in query.         |
| **Output Format**        | `Accept: application/netcdf`, `f=GeoTIFF`            | `.nc`, `.csv`, `.json`, `.graph`                    | ERDDAP uses file extensions; EDR uses MIME types or query param `f`.     |
| **Sampling Types**       | `position`, `area`, `trajectory`, `corridor`         | `grid`, `table`, `trajectory`                       | EDR has more explicit sampling types.                                    |
| **Rescaling**            | ❌ Not supported                                      | ✅ Supported via `stride`, `regrid`, `interpolate`  | ERDDAP allows downsampling and interpolation.                            |
| **Pub/Sub Support**      | Part 2: Publish-Subscribe                            | ❌ Not supported                                     | EDR supports event-driven data access.                                   |
