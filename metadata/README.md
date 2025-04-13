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

OGC API Records

### ISO 19115
SeaDataNet is the profile of the ISO19115. Same time OGC Records contains mappings to ISO:[link]
Some other mappings:[links](https://github.com/w3c/dxwg/blob/gh-pages/DCAT-ISO19115-mapping.xlsx)



### SeaDataNet

SeaDataNet schema for environmental (EDMED) data and Common Data Index (CDS):
https://www.seadatanet.org/Standards/Metadata-formats

CDS is considered for recommended compliance of catalog service - OGC API records.

Others to be considered in second order Cruise Summary Reports, EDMERP, EDIOS

### GeoDCAT
As DCAT is used heavily in the Ocen Information Model, proposed mapping of the Iliad catalog specification with GeoDCAT references and STAC payload schema is proposed:
https://ogcincubator.github.io/iliad-apis-features/bblock/ogc.hosted.iliad.api.features.stac_multidim_data/examples


## Approach
Iliad metadata definition is set of simple and composed properties and preferably their mappings to the reference specifications
