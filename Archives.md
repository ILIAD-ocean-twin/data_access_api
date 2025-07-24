# Storage formats
Most of the mainstream marine data falls under two of the data types: tabular data and multidimensional one.
Popular formats like NetCDF and CSV are the legacy standards highly utilised in the ecosystem.
Cloud services, however take benefits from the so called cloud native formats like GeoParquet and GeoZarr. Both formats are draft at the end of the Iliad project and the working groups has been estabilished during the project.
Through this process, significant advancements have been made in their specifications and implementations and both are selected for the EDITO edfault formats.
Amid there are tools like Kerchunk and Icechunk that bridge legacy formats with the cloud native capabilities, they shall be considered as compliant (and here the effort is put) with the programatic interfaces (APIs) of the file formats.

Iliad marine data outcomes are of various types which 
* time series for static locations
* multi trajectories (oil spills, )[Examples](examples/EDR_TrackingParticles/README.md)
* spatial features (cultural heritage, harbour)
* typical raster data and coverages from the eath observation platform and services like CMEMS, EMODNet and their derivates

## GeoZarr

GeoZarr is the generic Zarr based specification for geospatial data.
First level of specialisation is the description of the dimensionality, which for the spatial data is based on the geograhic coordinates (like longitude, latitude and height) and time.
Second level is the alignment with the conventions like Climate and Forecasts and other metadata stadnards (STAC and OGC API Records).
standrd specification is developed under the [GeoZarr Working group repository](https://github.com/zarr-developers/geozarr-spec)

Third Level goes beyond the core standard and defines profile for domain.
Iliad is working on the this level specifying the profiles of data based on the pilot case and integration constraints. As the example, Munkholmen sensors data is used. This data is exposed by the interactive APIs, but is also submitted to the SeaDataNet which requires alignment to their profile.
Based on this, the SeaDatanet profile is formalised in the machine readible format:
https://ogcincubator.github.io/iliad-apis-features/bblock

* [GeoZarr Array description metadata](https://ogcincubator.github.io/iliad-apis-features/bblock/ogc.hosted.iliad.api.features.zarr_array_metadata/examples) defines schema for the file structure.
* [GeoZarr Attributes description metadat](https://ogcincubator.github.io/iliad-apis-features/bblock/ogc.hosted.iliad.api.features.zarr_attrs_metadata/examples) defines schemaa for the variables description and examples for the dimansions and variables.
* [GeoZarr Attributes description metadata aligned to the SeaDataNet time series profile](https://ogcincubator.github.io/iliad-apis-features/bblock/ogc.hosted.iliad.api.features.zarr_attrs_sdn) defines SeaDataNet compliant profile of the second one.

Iliad building blocks, the toolset was initiated to support semantic enrichment though the context generation based on the underlying ontologies.
To use the examples it is possible either to use the examples and pregenerated contextx definitions as wel as publish their own profiles extending both schema and the references to the ontologies and semantic vocabularies.

## GeoParquet

Based on the popularity of the Paruet format, geoparquet is used in many setups as the next generation tabular binary data format. It is lighter than raw textual formats like CSV

Conversion of the CSV data into GeoParquet and upload to the EDITO S3 storage is provided in this [example jupyter notebook](./examples/OGC_Features/geoparquet.ipynb)

While tabular format is easy to understand and serialise, it is not always effective for the structured data with nested variables. Flattening to tables is an option then, but it brings substantial problems with scalable mapping to the ontologies. While the toolset support of the geoparquet is limited to the tabular formats, it seams like this sub-opimal solution is the only way forward wihout wider investment in the toolsets development which could not be fit in the Iliad timeline.