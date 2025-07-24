Observations with localisation can be represented as generic ‘Fearures’ (points or polygons) with values.


Example data in csv file from https://github.com/pzaborowski/pygeoapi/blob/master/pygeoapi/pygeoapi/tests/data/obs.csv

```
id	stn_id	datetime	value	lat	long
371	35	2001-10-30T14:24:55Z	89.9	45	-75
377	35	2002-10-30T18:31:38Z	93.9	45	-75
238	2147	2007-10-30T08:57:29Z	103.5	43	-79
297	2147	2003-10-30T07:37:29Z	93.5	43	-79
964	604	2000-10-30T18:24:39Z	99.9	49	-122
```

Can be exposed with OGC Features API with pygeoapi implementation.


```
python3 -m venv pygeoapi
cd pygeoapi
. bin/activate
git clone https://github.com/pzaborowski/pygeoapi
cd pygeoapi
pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 setup.py install
wget https://raw.githubusercontent.com/ILIAD-ocean-twin/data_access_api/refs/heads/main/examples/OGC_Features/example-config-observations.yml -O example-config.yml
export PYGEOAPI_CONFIG=example-config.yml
export PYGEOAPI_OPENAPI=example-openapi.yml
pygeoapi openapi generate $PYGEOAPI_CONFIG > $PYGEOAPI_OPENAPI
pygeoapi serve
```
Open `http://localhost:5002/collections/` in browser

Configuration will serve data from pygeoapi/tests/data/obs.csv
You can replace this file with your data preserving lon-lat-datetime columns or change example-config-observations.yml
with your file path
```
providers:
            - type: feature
              name: CSV
              data: tests/data/obs.csv
              id_field: id
              geometry:
                  x_field: long
                  y_field: lat
```

