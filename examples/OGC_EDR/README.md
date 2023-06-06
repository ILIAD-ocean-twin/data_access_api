# About

This is example configuration of the pygeoapi (pygeoapi.io) for NetCDF and Zarr files as Environmental Data Retrieal EPI

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
