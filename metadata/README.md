# Iliad metadata definitions

Iliad metadata definition defines minimum property set for the:
* catalog entry
* Features including measurement locations
* Coverage
* Sensors

The intent is to provide schemas and examples of the encodings for selected APIs, respectively:
* OGC Records
* OGC EDR collections, Locations, Features
* Potentially STA

For selected APIs, repository contains example configurations of the API service based on extensions of the reference implementations.

## Considered metadata definitions

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
