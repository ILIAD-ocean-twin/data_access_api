## Custom templates

OGC API Features, EDR and other features services are the backbone of the geospatial vectors data.
Similarily to the legacy services like WFS, each feature can be extended by the profile definition.
This mechanism was already acknoledged by the INSPIRE themes implemented by many public services.

Now, with the APIs suite based on the OpenAPI and ontologies behind the data models and the OGC building blocks it is possible to define such templates technically with common contexts definitions.

In the service provision, such contxts can be refered from the JSON payload or in the HTTP headers.
This way JSON is turned into JSON-LD - semantically enabled format with the namespaces support and variables formalised binding.

Pygeoapi support JSON-LD on default witch the generic schema.org context.
To customise it with own (like Iliad) profiles it is possible to define [templates](https://docs.pygeoapi.io/en/latest/html-templating.html)

[Example configuration](./pygeoapi-EDR-observations.yml) contain:

* reference to the context files - from the Ocean information model and Iliad building blocks
```
        linked-data:
            context:
              - https://ogcincubator.github.io/iliad-apis-features/build/annotated/hosted/iliad/api/features/oim-obs/context.jsonld
              - https://raw.githubusercontent.com/ILIAD-ocean-twin/OIM/47b1aaa3ba6bbf513665993b7bbb8c04b0e162b7/jsonld/oimOceanProfile-context.jsonld
              - https://raw.githubusercontent.com/ILIAD-ocean-twin/OIM/main/jsonld/crossDomain-context.jsonld
              - https://raw.githubusercontent.com/ILIAD-ocean-twin/OIM/main/jsonld/metadata-context.jsonld
            item_template: pygeoapi/templates/collections/items/feature_observation_item.jsonld
```
* item template reference
```
item_template: pygeoapi/templates/collections/items/feature_observation_item.jsonld
```

[Example template](./feature_observation_item.jsonld) contain ready to use template that can be put in the pygeoapi templates directory

NOTE: above configurtion uses typed CSV driver, that generate nested structures in the Features collection and specific feature type definition. Using it requires using [specific release](https://github.com/pzaborowski/pygeoapi/tree/csv_typed_provider) of the pygeoapi. However, with the template it is possible to add feature type inline

```
"featureType": "sosa:Observation",
```