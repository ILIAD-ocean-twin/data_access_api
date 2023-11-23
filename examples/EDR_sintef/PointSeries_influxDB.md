# Data organisation on source

In the InfluxDB, which is columnar time series storage measurements are collected into tables with _measurement, _time and other custom fields. There can be various custom fields for each measurement type.

Several measurements can be collected in one row representing observation at time. For example location is he observation made with GPS with lon, lat values.

In general, each table and group key data can have different sampling frequency and start, so each measument type can would have independent timestamps. The assumption is they cannot be joined on time without approximation and can be treated as separate observation streams.
If they belongs to different Group keys specifying _measument and instrument, they cannot be merged into one query result also.

# Data grid representation constraints
Grid and data cube data formats like Zarr, NetCDF, CoverageJSON are convenient to be used together with other oceanographic and marine as they share data model. On the other hand, they are based on the 'coverage' concept as function of place, time and the measured property. data representation is the table with values for each domain point. As the function must be defined on given domain, in our case of unsynchronised sample timestamps, there would be either different domains for each sensor measurements stream or great part of the values of the function would be undefined.

Example: measurement 'a' is given at t0, t4, t6, measurement 'b' is given at t1, t4, t5, the domain of merged data is t0,t1,t4,t5, but a(t1), a(t6), b(t6) are unknown and NA value must appear in the datacube query peyload.


# API constraints

The consequences of the structure for API exposing measuments are:
* it is safe to keep each measument type from particular sensor separately, so the query for all the measument types is not vary probable
*  Following EDR API collections structure, lowest level of collection properties reflects properties from given station if the NetCDF NCEI templates and equivalent Zarr representation shall be suported on the endpoint. lowest level of collection including properties from all the stations is still possible with CoverageJSON
* collection could be then whole set of data from the database but with constraints on the required selected-parameters call parameters.
