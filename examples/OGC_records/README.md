# About

This is example configuration of the pygeoapi (pygeoapi.io) for datasets records exposure.

It has been tested with the https://github.com/pzaborowski/pygeoapi fork of the official pygeoapi.io releases.
Once all the fixes implemented here will be applied to the mainstream, these configurations shall be migrated to the official pygeoapi.

To use configuration:
* clone https://github.com/pzaborowski/pygeoapi
* copy herein pygeoapi-example-config.yml into pygeoapi/example-config.yml
* copy herein sample-records.tinydb to pygeoapi/tests/data/open.canada.ca/sample-records.tinydb
* use installation according to https://docs.pygeoapi.io/en/latest/installation.html


# Test example
overview of record collection * http://localhost:5000/collections/metadata-records

queryables * http://localhost:5000/collections/foo/queryables

browse records * http://localhost:5000/collections/foo/items

paging * http://localhost:5000/collections/foo/items?offset=10&limit=10

CSV outputs * http://localhost:5000/collections/foo/items?f=csv

query records (spatial) * http://localhost:5000/collections/foo/items?bbox=-180,-90,180,90

query records (attribute) * http://localhost:5000/collections/foo/items?propertyname=foo

query records (temporal) * http://localhost:5000/collections/my-metadata/items?datetime=2020-04-10T14:11:00Z

query features (temporal) and sort ascending by a property (if no +/- indicated, + is assumed) * http://localhost:5000/collections/my-metadata/items?datetime=2020-04-10T14:11:00Z&sortby=datetime

query features (temporal) and sort descending by a property * http://localhost:5000/collections/my-metadata/items?datetime=2020-04-10T14:11:00Z&sortby=-datetime

fetch a specific record * http://localhost:5000/collections/my-metadata/items/123
