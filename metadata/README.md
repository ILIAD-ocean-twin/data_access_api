# Iliad metadata definitions

Iliad metadata definition defines minimum property set for the:
* catalog entry
* Features including measurement locations
* Coverage
* Sensors

The intent of this repository is not to define catalog metadata but to outline overlaps of the metadata in the data APIs and formats.
* OGC APIs like EDR collections, Locations, Features
* Potentially STA

For selected APIs, repository contains example configurations of the API service based on extensions of the reference implementations.

## Considered metadata definitions

### STAC 
STAC v1+ is now aligned with the Records API, while it extends metadata with some fields, assets being most striking one.
In addition, STAC collected already more than 70 extensions of the core specifications. to facilitate interoperability with EDITO, following suite of extensions is suggested.
It is important to use only relevant ones but to fill at least required field of the used extensions.

|Extension|URI|
|-----|----|
|Authentication|https://stac-extensions.github.io/authentication/v1.1.0/schema.json|
|CF|https://stac-extensions.github.io/cf/v0.2.0/schema.json|
|Datacube|https://stac-extensions.github.io/datacube/v2.2.0/schema.json|
|Example Links|https://stac-extensions.github.io/example-links/v0.0.1/schema.json|
|File Info|
|Forecast|https://stac-extensions.github.io/forecast/v0.2.0/schema.json|
|Grid|https://stac-extensions.github.io/grid/v1.1.0/schema.json|
|Item Assets Definition|
|Order|
|Processing|
|Quality*|
|Rendering|
|Scientific Citation|
|Themes|
|Tiled Assets|
|Timestamps|
|Versioning Indicators|
|Video|
|Virtual Assets|
|Web Map Links|
|xarray Assets|

For validation, 

### OGC API Records

OGC API Records is the standard compliant with the OGC API Features together with STAC designed for the EO data.
It is considered as the next generation spatial data catalog (lagacy is CSW). it preserves compliance with the ISO19115 metadata model.

### ISO 19115
SeaDataNet is the profile of the ISO19115. Same time OGC Records contains mappings to ISO:[link]

It is also mapped to DCAT inofficially:
https://github.com/w3c/dxwg/blob/gh-pages/DCAT-ISO19115-mapping.xlsx


### SeaDataNet

SeaDataNet schema for environmental (EDMED) data and Common Data Index (CDS):
https://www.seadatanet.org/Standards/Metadata-formats

CDS is considered for recommended compliance of catalog service.


### GeoDCAT

GeoDCAT-AP is an extension of the DCAT-AP (Data Catalogue vocabulary) specifically designed for describing geospatial datasets, dataset series, and services. It provides a standardized way to make spatial data findable and accessible across different data portals, particularly within the European Union. Essentially, it bridges the gap between general data catalogs and those focused on geospatial information.
With DCAT 

## Iliad solution

Iliad metadata definition is set of simple and composed properties and preferably their mappings to the reference specifications.
With the Ocean Information Model metadata profile and the OGC Records development (accepted standard in 2025), Iliad co-defined the proposal for the common reference mapping to DCAT
https://github.com/ogcincubator/geodcat-ogcapi-records
and the STAC profile with the datacube, themes extension and additionally ODRL based provenance:
https://ogcincubator.github.io/iliad-apis-features/bblock/ogc.hosted.iliad.api.features.stac_multidim_data

### How to use


Alignment to the Iliad Records/STAC catalog can be done in multiple ways. one of them is to setup available services filling it with own metadata:
1. implementation of the Records API [see example configuration](../examples/OGC_records/README.md)
2. add reference to the context file from one of the above repositories by [LD enabled templates](../examples/Observations_Features/LD_templates.md)
