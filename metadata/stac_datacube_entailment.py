import xarray as xr
import rasterio
from stac_pydantic import Item
from stac_pydantic.links import Link
from stac_pydantic.shared import Asset
from datetime import datetime
import json
import os
from pandas.api.types import is_numeric_dtype

def extract_netcdf_metadata(netcdf_file, record, lon='lon',lat='lat', time='time'):
    # Open the NetCDF file using xarray
    ds = xr.open_dataset(netcdf_file)

    # Extract relevant metadata
    record["properties"]["title"] = ds.attrs.get('title', record["properties"]["title"])
    record["properties"]["description"] = ds.attrs.get('description', record["properties"]["description"])
    start_datetime = ds.coords[time].min().values.astype('datetime64[ms]').item().isoformat()
    record["properties"]["datetime"] = str(start_datetime)+"Z",
    record["properties"]["start_datetime"] = str(start_datetime)+"Z"
    record["properties"]["updated"] = datetime.utcnow().isoformat() + "Z",
    record["properties"]["end_datetime"] = str(ds.coords[time].max().values.astype('datetime64[ms]'))+"Z"
    record["bbox"] = [
            ds[lon].min().item(),
            ds[lat].min().item(),
            ds[lon].max().item(),
            ds[lat].max().item()
        ]
    record["crs"] = ds.crs if 'crs' in ds else 'EPSG:4326'
    create_cube_dimensions(ds, record)
    create_cube_variables(ds, record)
    return record

def _toiso(d):
    return d.values.astype('datetime64[ms]').item().isoformat()



def create_cube_variables(ds, record):
    dims = [str(d) for d in ds.coords.keys()]
    vars = [str(v) for v in ds.variables.keys()]
    record['properties']["cube:variables"] = {}
    for v in vars:
        print(v)
        if not any(v == selected_v for selected_v in dims):
            record['properties']["cube:variables"][v] = {
                "dimensions": ds.variables[v].dims,
            }
            if is_numeric_dtype(ds.variables[v].dtype):
                record['properties']["cube:variables"][v]["type"] = "data"
            else:
                record['properties']["cube:variables"][v]["type"] = "auxiliary"
            
            u = ds.variables[v].attrs.get("units")
            if u:
                record['properties']["cube:variables"][v]['unit'] = u


def create_cube_dimensions(ds, record):
    dims = [str(d) for d in ds.coords.keys()]
    record['properties']["cube:dimensions"] = {}
    for d in dims:
        print(d)
        if ds.coords[d].attrs.get('standard_name') == 'time':
            record['properties']["cube:dimensions"][d] = {"type": "temporal",
                                        "extent": [_toiso(ds.coords[d].min()),
                                                   _toiso(ds.coords[d].max())]
                                        }
        elif ds.coords[d].attrs.get('standard_name') == 'degrees_east':
            record['properties']["cube:dimensions"][d] = {"type": "spatial",
                                        "axis": "x",
                                        "extent": [ds.coords[d].min().item(),
                                                   ds.coords[d].max().item()],
                                                   "step": len(ds.coords[d]),
                                                   "reference_system": "https://www.opengis.net/def/crs/OGC/1.3/CRS84"
                                        }
        elif ds.coords[d].attrs.get('standard_name') == 'degrees_north':
            record['properties']["cube:dimensions"][d] = {"type": "spatial",
                                        "axis": "y",
                                        "extent": [ds.coords[d].min().item(),
                                                   ds.coords[d].max().item()],
                                                   "step": len(ds.coords[d]),
                                                   "reference_system": "https://www.opengis.net/def/crs/OGC/1.3/CRS84"
                                        }
        else:
            record['properties']["cube:dimensions"][d] = {"type": d,
                                        "extent": [ds.coords[d].min().item(),
                                                   ds.coords[d].max().item()]}
        u = ds.coords[d].attrs.get('units')
        if u:
            record['properties']["cube:dimensions"][d]['unit'] = u



def main(netcdf_file, output_folder, source_record_file, dest_record_file):

    os.makedirs(output_folder, exist_ok=True)
    with open(source_record_file, 'r') as file:
        record = json.load(file)

    extract_netcdf_metadata(netcdf_file, record)

    with open(dest_record_file, 'w') as f:
        json.dump(record, f, indent=2, default=str)

if __name__ == "__main__":
    netcdf_file_path = "~/Downloads/simulation.nc"  # Replace with your NetCDF file path
    source_record_file = "tests/record_example.json"  # Replace with your desired output directory
    output_folder = "tests/"
    dest_record_file = "record_example_wth_netcdf_data.json"  # Replace with your desired output directory
    main(netcdf_file_path, output_folder, source_record_file, dest_record_file)
