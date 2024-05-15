# About

Environmental Data Retreival API is one of the mature OGC APIs that are built on the heritage of OGC Web Services like WCS to provide data access for numerical, multi-dimentional data which is subset of general Coverage Information Model.

With this API, that can be put in front of various data sources enabling:
* one mechanism of access regardless of underlying data format and transfer protocol
* one data model aligned to custom domain (like CF convention)
* metadata discovery service to navigate through the catalog of exposed data collections
* multi-format support behind one API
* OpenAPI based specification generated directly from server


This is example configuration of the pygeoapi (pygeoapi.io) for NetCDF and Zarr files as Environmental Data Retrieval EPI

ToDo - reference common ILIAD profiles of OMS/SOSA as target of validation testing.

It has been tested with the https://github.com/pzaborowski/pygeoapi fork of the official pygeoapi.io releases.
Once all the fixes implemented here will be applied to the mainstream, these configurations shall be migrated to the official pygeoapi.

Setup for development environment:


```
python3 -m venv pygeoapi
cd pygeoapi
. bin/activate
git clone https://github.com/pzaborowski/pygeoapi
cd pygeoapi
pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 setup.py install
wget https://raw.githubusercontent.com/ILIAD-ocean-twin/data_access_api/main/examples/OGC_EDR/configs/example-config-edr.yml -O example-config.yml
export PYGEOAPI_CONFIG=example-config.yml
export PYGEOAPI_OPENAPI=example-openapi.yml
pygeoapi openapi generate $PYGEOAPI_CONFIG > $PYGEOAPI_OPENAPI
pygeoapi serve
```
Server shall be available on http://localhost:5003


# API Access
You can now data though your browser or client application:
* see the langin page of the API:
http://localhost:5002/
* see the data collections
http://localhost:5002/collections
* details of selected collection
http://localhost:5002/collections/swan2-edr
* swagger document for developers
http://localhost:5002/openapi?f=html
* access data trimmed to needed spation-temporal extent:
http://localhost:5002/collections/nsea-edr/cube?bbox=-5.0,45.0,9.963,64.29&datetime=2024-04-18/2024-04-18&format=NetCDF
* the same data in Zarr format
[http://localhost:5002/collections/nsea-edr/position?coords=POINT(-5.0 45.0)&datetime=2024-04-18/2024-04-18&format=zarr](http://localhost:5002/collections/nsea-edr/cube?bbox=-5.0,45.0,9.963,64.29&datetime=2024-04-18/2024-04-18&format=zarr)


# Python access
under the [Jupyter link](OGC_EDR/discovery_access_EDR.ipynb) you'll find samples of data access using OWSLIB and xarray libraries.

