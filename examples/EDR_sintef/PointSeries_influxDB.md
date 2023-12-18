# Data organisation on source

*Disclaimer: following overview was prepared based on the Iliad pilot driven by SINTEF and our best knowledge of the Influx capabilities as for the Oct 2023. Feel free to provide feedback in the herein github issues.*

In the InfluxDB, which is columnar time series storage, measurements are collected into tables with _measurement, _time and other custom fields. There can be various custom fields for each measurement type.

Several measurements can be collected in the record representing observation at time. For example location is he observation made with GPS with lon, lat values as well as 'approved' flag. Likewise, sea_water_temperature is the value in Celcius degrees at given time plus 'approved' flag.

In general, each table and group key data can have different sampling frequency and start, so each measument type can would have independent timestamps. The assumption is they cannot be joined on time without approximation and can be treated as separate observation streams. It applies to the measurement of location as well.
If they belongs to different Group keys specifying _measument and instrument, they cannot be merged into one query result also.

# Data grid representation constraints
Grid and data cube data formats like Zarr, NetCDF, CoverageJSON are convenient to be used together with other oceanographic and marine as they share data model. On the other hand, they are based on the 'coverage' concept as function of place, time and the measured property. data representation is the table with values for each domain point. As the function must be defined on given domain, in our case of unsynchronised sample timestamps, there would be either different domains for each sensor measurements stream or great part of the values of the function would be undefined.

Example: measurement 'a' is given at t0, t4, t6, measurement 'b' is given at t1, t4, t5, the domain of merged data is t0,t1,t4,t5, but a(t1), a(t6), b(t6) are unknown and NA value must appear in the datacube query peyload.


# API constraints

API for this datastream can be both request/response and [pub/sub](https://opengeospatialdata.springeropen.com/articles/10.1186/s40965-017-0030-7) model. [TODO: link/page to the good comparison of the two models].

For the pub/sub model Sensor Things API proposes to use separate data streams so that each is described properly and the online observation payload minimised.

For the RESTful API, the data can be combined on the one endpoint in one or several datasets but the consequences of the structure for API exposing measurements are:

* to keep data simple and compact, either 1 response shall include only one property or the collection queries shall be limited to one property (constraint to EDR reference)

* it is safe to keep each measurement type from particular sensor separately in queries, querying all the measurements stream is not recommended but can be supported by the internal collection/additional dimension.

For example, following the EDR API collections structure collection can contain many types of measurements with various definitions and units. Additional concern to query only one parameter would be an additional limitation

* most of the metadata describing sensor is not given in the influx db. either the definition of the collection and/or observed property needs to grap these properties from the configuration. it can be done as set of properties or reference to the

* separation of

Proposed API collections structure could be hierarchical:
```
\collections - list all highest level collections
\collections\search - extension to EDR to search for collections by the observed property
\collections\{provider/group} - collection with all the measuments (like temp, salinity) but with the constraint only one can be queried at the same time.
\collections\{provider/group+location} - collection with all the measuments (like temp, salinity) from given location with the the constraint only one can be queried at the same time. it shall contain the links directly to the queryable properties. Data type is Point Series in case of constant (approximate) location
```

or flattened to one
```
\collections - list all highest level collections
\collections\search
\collections\{provider_dataset} - collection with all the measuments (like temp, salinity) from given location with the the constraint only one can be queried at the same time. it shall contain the links directly to the queryable properties. Data type is also Point Series in case of constant (approximate) location.
```
