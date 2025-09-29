# Semantic interoperability concepts

Semantic interoperability is one of the layers of the European Interoperability Framework and similar. Next to technical interoperability, They are sometimes considered together as complementary techniques. Technical interopeability focuses around transfer protocols like HTTP, OpenAPI or OData, logical models and their encodings.
Semantic on data interpretations and conceptual models.

#### [Read more about the interoperability layers](https://joinup.ec.europa.eu/collection/nifo-national-interoperability-framework-observatory/3-interoperability-layers#3.5)

## Met-Ocean heritage

Marine community achived considerably high level of the semantic interoperability based on the agreed formats and conventions like the [Climate and Forecast conventions (CF)](http://cfconventions.org).
On top of data formats like NetCDF and their access protocols like OpenDAP (technical interoperability), CF compiles:
* [templates](https://www.ncei.noaa.gov/netcdf-templates) of interpretation of data structures with their reference to spatio-temporal domain,
* attributes vocabularies like (standard_name)[http://cfconventions.org/Data/cf-conventions/cf-conventions-1.11/cf-conventions.html#standard-name] with units, * [common transformations](http://cfconventions.org/Data/cf-conventions/cf-conventions-1.11/cf-conventions.html#appendix-coordinate-subsampling) and
* contraints on data completeness.

Some elements of the CF convention is based on particular representations in their native format of   NetCDF, parts were also adopted in the ISO19115 based models proposed by the SeaDataNet specifications.

## Machine readability and Linked data

While conventions are widely known among the community, their interpretation is closely related to the expertise that needs to coded by domain experts. Modern practices based on the W3C and similar work are using the concept of the Linked Data where the occurrences of data entities are accompanied with their reference to definitions.

For example

It is the Iliad APIs approach to exploit benefits of the modern APIs based on the JSON/XML metadata that can include references to the LD context


## Proposed semantic support levels

Based on the legacy systems review, available techniques and
1. compliance to CF conventions - data is structured and described following the conventions and the interface declares specification version compliance
2. compliance to Ocean Information Model with phenomenons, observations and analytical outcomes references (e.g. links to observable properties are provided)
3. compliance with Ocean Information Model for all the data structures spatio-temporal domain.
4. full semantic support [(5th star of semantic support)](https://5stardata.info/en/) with explicit meaning assigned to each entity and value and between domain and values including data collections like multi-dimensional values to spatio-temporal domain
5. full semantic support in the APIs description - it requires all the APIs definitions like YAML specifications (like query parameters) are also accompanied with reference to the semantic definitions; here, potential solutions shall be developed but the concept is quite new (https://json-ld.github.io/yaml-ld/spec/) and supporting tools must be surveyed. Potentially it could help with the machine discoverable services (like in the Data Spaces concept) but the behavioural descriptions of the operators could be required to fully benefit.

Proposed Iliad APIs, the target is the 3rd level support.
In practice, it means the full context/namespace is defined for all the entities and values, and it links to the common vocabularies.

### APIs semantic support implementation

NOTE:
on API level, above 3rd level is 4th level ready once the community defines crosswalks between implicit, machine readable data serialisations and it is included in the OIM.
For example definition of the relation between indexed values and domain ranges as below pseudo-coded.

```
observationAt(time, lat_value, lon_value, z_value)
  hasResult
  value(indexof(time,timedomain), indexof(lat_value, lat_domain), indexof(lon_value, lon_domain), indexof(z_value,z_dmain),
value_range)
```

Semantic support can be provided on the strages or on the APIs.
[Herein example](https://github.com/ILIAD-ocean-twin/data_access_api/blob/main/EDR_Features.md#semantic-enablement) describes how the features based API can be uplifted with the sementic annotations.
Similarily, the coverage payload from APIs can be implemented using
 - [pygeoapi templates](https://docs.pygeoapi.io/en/latest/html-templating.html)
 - [OIM contexts](https://github.com/ILIAD-ocean-twin/OIM/tree/main/metadata-json-schema)
 - [geospatial contexts](https://ogcincubator.github.io/iliad-apis-features/bblock)
https://github.com/ILIAD-ocean-twin/data_access_api/blob/main/EDR_Features.md#semantic-enablement
 Example setup is provided with feature types 