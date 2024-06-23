# Observations as Features

Observations model is well defined by the ISO19156/OGC Observations and Measurements with recent revisions and in the API implementations like OGC SensorThings API.
However, they can be also exposed as the OGC Features API which is designed for any vector data represenations supported by GeoJSON.

To keep OIM compliance of Observations as Features, dedicated building blocks has been defined for
* [Collection of Observations](https://ogcincubator.github.io/iliad-apis-features/bblock/ogc.hosted.iliad.api.features.oim-obs/json-ld) (in the meaning of OGC API Features and Commons)
* [Observation item](https://ogcincubator.github.io/iliad-apis-features/bblock/ogc.hosted.iliad.api.features.oim-obs/json-ld) (in the meanig of OGC API Features)

These buiding blocks are provided with JSON schema and JSON-LD context aligned with SOSA/SSN ontology.
Features implementing this schema have few optional properties from the SOSA model like observedProperty, resultTime. For simple observations

```
{
  "id": "pop1999",
  "type": "Feature",
  "featureType": "sosa:Observation",
  "geometry": null,
  "properties": {
    "observedProperty": "https://dbpedia.org/ontology/population",
    "resultTime": "1999",
    "comment": "Example of an inline membership - would entail hasMember relations",
    "hasFeatureOfInterest": "https://demo.pygeoapi.io/master/collections/utah_city_locations/items/Spanish%20Fork",
    "hasSimpleResult": 15555.0
  }
}
```
Geometry can be declared inline for the observation of geospatial queries or in case of many observations of the same feature link to the Feature of Interest (FoI) can be dlacared though hasFeatureOfInterest.

Simple result of observation can be declared directly in the properties using hasSimpleResult field.


## Multi result Observations template

For observations with multiple results at the same time, complex hasResult can be used to next the values:

```{
  ...
  "properties": {
    "observedProperty": "https://dbpedia.org/ontology/population",
    ...
    "hasResult": {
      "a": "r1",
      "b": "r2"
    }
  }
}
```

## Application of the Observation as Feature model

To use the model of Observations as Features the easiest application:
* use your prefered OGC API Feature implementation
* add observations result according to [examples](https://opengeospatial.github.io/ogcapi-sosa/bblock/ogc.sosa.features.observation/examples) and validate with [JSON schema](https://opengeospatial.github.io/ogcapi-sosa/bblock/ogc.sosa.features.observation/json-schema)
* add the [context](https://opengeospatial.github.io/ogcapi-sosa/build/annotated/sosa/features/observation/context.jsonld) to your responses inline in the payload or HTTP header

Example of context in the payload: 
```
{
  "id": "pop1999",
    ...
  "properties": {
    "observedProperty": "https://dbpedia.org/ontology/population",
    ...
  },
  "@context": "https://opengeospatial.github.io/ogcapi-sosa/build/annotated/sosa/features/observation/context.jsonld"
}
```

In case of custom ObservedProperties or result variables one may want to refer to ovn vocabularies, which is presented in the next example

## Jellyfish pilot template

For specific applications domain vocabularies may be needed to fully define the data in the payload.
For example the Jallyfish monitoring provide observations with values of scientificName, occurrenceStatus etc.
The are defined in the [Ocean Information Model common vocabulary](https://github.com/ILIAD-ocean-twin/OIM/blob/47b1aaa3ba6bbf513665993b7bbb8c04b0e162b7/oceanCommon.ttl#L1243) based on known ontologies:

```
@prefix dwc:  <http://rs.tdwg.org/dwc/terms/> .
...
dwc:occurrenceStatus
```

So one can reuse generated [JSON-LD context](https://github.com/ILIAD-ocean-twin/OIM/tree/47b1aaa3ba6bbf513665993b7bbb8c04b0e162b7/jsonld) with this reference as additional entry:
```
{
    "@context":[
        "https://ogcincubator.github.io/iliad-apis-features/build/annotated/hosted/iliad/api/features/oim-obs/context.jsonld",
        "https://raw.githubusercontent.com/ILIAD-ocean-twin/OIM/47b1aaa3ba6bbf513665993b7bbb8c04b0e162b7/jsonld/oimOceanProfile-context.jsonld",
        "https://raw.githubusercontent.com/ILIAD-ocean-twin/OIM/main/jsonld/crossDomain-context.jsonld",
        "https://raw.githubusercontent.com/ILIAD-ocean-twin/OIM/main/jsonld/metadata-context.jsonld"
    ],
    "type":"FeatureCollection",
    "FeatureType":"sosa:ObservationCollection",
    "features":[
```

## Reference implementation

Using one of the OGC API Features 

Features added to the pygeoapi codebase:
 - custom context support for Items
 - nexted hasResult in the CSVObsProvider

In the [example configuration](https://github.com/ILIAD-ocean-twin/data_access_api/blob/master/examples/Observations_Features/example-config-observations.yml) CSV provider has been used for convenient fist steps deployment. For production deployments database backend like Elasticsearch can be considered.

 Example configuration contains:
 * references to context files
 * mapping of fields to coordinates and is
 * list of properties that will be treated as observation results and nested in properties.hasResult

 ```
 my-observations-linked:
        ...
        linked-data:
            direct-context:
              - https://ogcincubator.github.io/iliad-apis-features/build/annotated/hosted/iliad/api/features/oim-obs/context.jsonld
              - https://raw.githubusercontent.com/ILIAD-ocean-twin/OIM/47b1aaa3ba6bbf513665993b7bbb8c04b0e162b7/jsonld/oimOceanProfile-context.jsonld
              - https://raw.githubusercontent.com/ILIAD-ocean-twin/OIM/main/jsonld/crossDomain-context.jsonld
              - https://raw.githubusercontent.com/ILIAD-ocean-twin/OIM/main/jsonld/metadata-context.jsonld
        ...
        providers:
            - type: feature
              name: CSVObs
              data: /Users/piotr/Temp/JF_Israel_Jun_2011-Dec_2023_DwC_Format_25.3.2024-JF_Jun_2011-Dec_2023_DwC_Format_25.3.2024-pp.csv
              id_field: occurenceID
              geometry:
                  x_field: decimalLongitude
                  y_field: decimalLatitude
              properties_obj:
                  hasResult:
                    - scientificName
                    - occurrenceStatus
                    - basisOfRecord
                    - scientificNameID
                    - recordedBy
                    - quantificationMethod
                    - organismQuantity
                    - organismQuantityType
                    - sampleSizeUnit
                    - sampleSizeValue
                    - coordinateUncertaintyInMeters
                    - strandedJellyfish
                    - distanceWalkedinmeters
 ```

## Further use

Observation as Feature model is one of the examples of vector data with full LD support and alignement with Ocean Information Model. Based on this template any custom feature can be represented including monitoring stations, Marine Spatial Planning areas like Protected Areas.

## Limitations

Proposed solution of Feature properties containing objects (in this case hasResult with observation results) is fully compliant with OGC API Features schema but can be missing support in some implementations.
Such nesting will be not suported by tabular data formats like csv and geoparquet on the output which would require additional annoation of result properties to preserve the relation fo feature as sosa:hasResult.

Proposed solution is verbose representation of geospatially located data. For large number of Features, especially for web applications and high volume data exchange aggregate formats and APIs has been designed like NetCDF/Zarr, OGC API EDR/Coverages/Map