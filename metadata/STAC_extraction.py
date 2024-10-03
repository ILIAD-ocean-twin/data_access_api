import xarray as xr
import rasterio
from stac_pydantic import Item
from stac_pydantic.links import Link
from stac_pydantic.shared import Asset
from datetime import datetime
import json
import os
from pandas.api.types import is_numeric_dtype

wasGeneratedBy = {
            "provType": "Activity",
            "id": "surveys:DP-1-S1",
            "activityType": "InitialSurvey",
            "endedAtTime": "2023-10-05T05:03:15+01:00",
            "wasAssociatedWith": "staff:jd234",
            "used": {
            "id": "regulations:Act3",
            "entityType": "Legislation",
            "wasAttributedTo": "agents:someGovernment",
            "links": [
                {
                "href": "https://some.gov/linktoact/",
                "rel": "related"
                }
            ]
            }
            }

def extract_netcdf_metadata(netcdf_file,lon='lon',lat='lat', time='time'):
    # Open the NetCDF file using xarray
    ds = xr.open_dataset(netcdf_file)
    
    # Extract relevant metadata
    metadata = {
        "title": ds.attrs.get('title', 'No Title'),
        "description": ds.attrs.get('description', 'No Description'),
        "start_datetime": ds.coords[time].min().values.astype('datetime64[ms]').item().isoformat(),
        "end_datetime": ds.coords[time].max().values.astype('datetime64[ms]'),
        "bbox": [
            ds[lon].min().item(),
            ds[lat].min().item(),
            ds[lon].max().item(),
            ds[lat].max().item()
        ],
        "crs": ds.crs if 'crs' in ds else 'EPSG:4326',
        "variables": list(ds.data_vars),
        "properties": create_properties(ds)
    }
    return metadata


def _toiso(d):
    return d.values.astype('datetime64[ms]').item().isoformat()


def create_contacts_example(ds, ps):
    ps["contacts"] = [
      {
        "name": "name of the contact, name or organisation is required or both, all the other fields are optiopnal. Roles can be defined on the contact or phones|emails|addresses level",
        "organization": "name of the organisation, name or organisation is required or both, all the other fields are optional. schema https://github.com/opengeospatial/ogcapi-records/blob/master/core/openapi/schemas/contact.yaml",
        "identifier": " optional identifier of the contact",
        "position": "optional position of the contact",
        "logo": {
             "href": "https://example.com/logo.png",
             "rel": "icon",
             "type": "image/png",
             "description": "descritpion is not required here just for a not in the example: link shall have rel=icon and type shall be image"
           },
        "links": [
           {
             "href": "https://woudc.org",
             "rel": "about",
             "type": "text/html"
           }
        ],
        "phones":[{"value": "+99123456983123", "role": "contactPoint"}],
        "emails":[{"value": "jsmith@example.com", "role": "rightsHolder"}],
        "addresses":[{"deliveryPoint":["optional detailed address"],"city":"optional city", "administrativeArea":"optional administrativeArea", "postalCode":"optional postalCode", "country":"optional country"}],
        "contactInstructions": "SEE PAGE: https://woudc.org/contact.php",
        "roles": [ "contactPoint", "rightsHolder", "pubisher", "creator", "distributor", "originator", "principalInvestigator", "processor", "resourceProvider", "u" ]
      }
    ]



def create_themes_properties(ds, ps):
    ps["themes"] = [
      {
        "concepts": [
          {
            "id": "12301",
            "name": "water resources management"
          },
          {
              "id": "water_resources_management",
              "url": "http://www.eionet.europa.eu/gemet/concept/12301"
           }

        ],
        "scheme": "http://www.eionet.europa.eu/gemet/concept/"
      },
      {
          "concepts": [{"id": "water_quality"}],
          "scheme": "http://mmisw.org/ont/ioos/category"
      }
    ]
    ps["keywords"] = [
            "water",
            "ozoother keyword"
        ]
    ps["wasGeneratedBy"] = wasGeneratedBy


def create_properties(ds):
    ps = {}
    create_cube_dimensions(ds, ps)
    create_cube_variables(ds, ps)
    create_themes_properties(ds, ps)
    create_contacts_example(ds, ps)
    return ps


def create_cube_variables(ds, ps):
    vars = [str(v) for v in ds.variables.keys()]
    ps["cube:variables"] = {}
    for v in vars:
        print(v)
        if any(v == selected_v for selected_v in ['sea_water_salinity','diameter'] ):
            ps["cube:variables"][v] = {
                "dimensions": ds.variables[v].dims,
            }
            if is_numeric_dtype(ds.variables[v].dtype):
                ps["cube:variables"][v]["type"] = "data"
            else:
                ps["cube:variables"][v]["type"] = "auxiliary"
            
            u = ds.variables[v].attrs.get("units")
            if u:
                ps["cube:variables"][v]['unit'] = u


def create_cube_dimensions(ds, ps):
    dims = [str(d) for d in ds.coords.keys()]
    ps["cube:dimensions"] = {}
    for d in dims:
        print(d)
        if ds.coords[d].attrs.get('standard_name') == 'time':
            ps["cube:dimensions"][d] = {"type": "temporal",
                                        "extent": [_toiso(ds.coords[d].min()),
                                                   _toiso(ds.coords[d].max())]
                                        }
        elif ds.coords[d].attrs.get('standard_name') == 'degrees_east':
            ps["cube:dimensions"][d] = {"type": "spatial",
                                        "axis": "x",
                                        "extent": [ds.coords[d].min().item(),
                                                   ds.coords[d].max().item()],
                                                   "step": len(ds.coords[d]),
                                                   "reference_system": "https://www.opengis.net/def/crs/OGC/1.3/CRS84"
                                        }
        elif ds.coords[d].attrs.get('standard_name') == 'degrees_north':
            ps["cube:dimensions"][d] = {"type": "spatial",
                                        "axis": "y",
                                        "extent": [ds.coords[d].min().item(),
                                                   ds.coords[d].max().item()],
                                                   "step": len(ds.coords[d]),
                                                   "reference_system": "https://www.opengis.net/def/crs/OGC/1.3/CRS84"
                                        }
        else:
            ps["cube:dimensions"][d] = {"type": d,
                                        "extent": [ds.coords[d].min().item(),
                                                   ds.coords[d].max().item()]}
        u = ds.coords[d].attrs.get('units')
        if u:
            ps["cube:dimensions"][d]['unit'] = u




def create_stac_item(metadata, netcdf_file, output_folder):
    # Create a STAC Item using extracted metadata
    _id=str(os.path.basename(netcdf_file).split('.')[0])
    start_datetime = metadata["start_datetime"]
    end_datetime = metadata["end_datetime"]
    
    item = Item(
        id=_id,
        type="Feature",
        stac_version="1.1.0",
        stac_extensions=["https://stac-extensions.github.io/datacube/v2.2.0/schema.json",
                         "https://stac-extensions.github.io/themes/v1.0.0/schema.json",
                         "https://stac-extensions.github.io/cf/v0.2.0/schema.json",
                         "https://stac-extensions.github.io/contacts/v0.1.1/schema.json",
                         "https://stac-extensions.github.io/version/v1.2.0/schema.json",
                         "https://stac-extensions.github.io/processing/v1.2.0/schema.json"],
        conformsTo=["https://ogcincubator.github.io/geodcat-ogcapi-records/bblock/ogc.geo.geodcat.geodcat-stac-eo/",
                    "https://ogcincubator.github.io/iliad-apis-features/bblock/ogc.hosted.iliad.api.stac_record",
                    "https://stac-extensions.github.io/datacube/v2.2.0/schema.json",
                    "https://stac-extensions.github.io/datacube/v2.2.0/schema.json",
                    "https://stac-extensions.github.io/themes/v1.0.0/schema.json",
                    "https://stac-extensions.github.io/cf/v0.2.0/schema.json",
                    "https://stac-extensions.github.io/contacts/v0.1.1/schema.json",
                    "https://stac-extensions.github.io/version/v1.2.0/schema.json",
                    "https://stac-extensions.github.io/processing/v1.2.0/schema.json"],
        properties={**metadata["properties"], **{
            "title": metadata["title"],
            "description": metadata["description"],
            "datetime": str(start_datetime)+"Z",
            "start_datetime": str(start_datetime)+"Z",
            "end_datetime": str(end_datetime)+"Z",
            "created": datetime.utcnow().isoformat() + "Z",
            "updated": datetime.utcnow().isoformat() + "Z"},
            "rights": "string defining access rights inline or as URL",
            "applicableLegislation": "string defining applicable legislation inline or as URL, use wasGeneratedBy.used for cases whereever you can assign quality measure to particular processing step",
            "convention": "CF-1.6",
            "version": "optional resource behind the record version string",
            "deprecated": False,
            "latest-version": "optional link to the record with latest version",
            "predecessor-version": "optional link to the record with previous version",
            "successor-version": "optional link to the record with next version",
            "cf:parameter": [
                {
                "name": "sea_water_salinity",
                "schema": "http://vocab.nerc.ac.uk/standard_name/",
                "unit": "https://qudt.org/2.1/vocab/unit/GM-PER-KiloGM"
                }
            ],
            
            "dqv:hasQualityMeasurement": "optional description of the quality measures used to generate the content, use wasGeneratedBy.used for cases whereever you can assign quality measure to particular processing step"
        },
        geometry={
            "type": "Polygon",
            "coordinates": [[
                [metadata["bbox"][0], metadata["bbox"][1]],
                [metadata["bbox"][0], metadata["bbox"][3]],
                [metadata["bbox"][2], metadata["bbox"][3]],
                [metadata["bbox"][2], metadata["bbox"][1]],
                [metadata["bbox"][0], metadata["bbox"][1]]
            ]]
        },
        bbox=metadata["bbox"],
        assets={
            "data": Asset(
                href=netcdf_file,
                title="NetCDF Data",
                media_type="application/x-netcdf"
            )
        },
        links=[
            Link(
                rel="self",
                title="optional link to this record",
                href=f"{output_folder}/{_id}.json"
            ),
            Link(
                rel="enclosure",
                type="application/x-hdf",
                title="optional raw file",
                href=f"{netcdf_file}"
            ),
            Link(
                rel="preview",
                type="image/png",
                title="optional thumbnail image preview",
                href=f"{netcdf_file}"
            ),
            Link(
                rel="sample",
                type="application/x-hdf",
                title="optional link to the sample data, either one enclosure or service is required in Iliad profile",
                href=f"{output_folder}/{_id}.zip"
            ),
            Link(
                rel="sample",
                type="application/x-hdf",
                title="link to the data, either one enclosure or service is required in Iliad profile",
                href=f"{output_folder}/{_id}.zip"
            ),
            Link(
                rel="conformance",
                type="text/html",
                title="link to the resource confirmance speficication",
                href=f"https://cfconventions.org/Data/cf-conventions/cf-conventions-1.11/cf-conventions.pdf"
            ),
            
            Link(
                rel="service",
                type="application/xml",
                title="optional link to the web service (not raw file) like OGC Web Map Service (WMS) either one enclosure or service is required in Iliad profile",
                href=f"https://example.com/ows/wms"
            ),
            Link(
                rel="license",
                type="text/html",
                title= "optional link to the data descritpion page",
                href=f"https://example.com/license"
            ),
            Link(
                rel="license",
                type="text/html",
                title= "optional link to the license",
                href=f"https://example.com/license"
            ),
            Link(
                rel="next",
                type="text/html",
                title= "optional link to the next in the serie",
                href=f"https://example.com/next_data_record"
            ),
            Link(
                rel="prev",
                type="text/html",
                title= "optional link to the previous in the serie",
                href=f"https://example.com/prev_data_record"
            ),
            Link(
                rel="parent",
                type="text/html",
                title= "optional link to the parent if data in series or other parent in the hierarchy",
                href=f"https://example.com/prev_data_record"
            )
        ]
    )

    return item


def main(netcdf_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Extract metadata from the NetCDF file
    metadata = extract_netcdf_metadata(netcdf_file)

    # Create a STAC item
    stac_item = create_stac_item(metadata, netcdf_file, output_folder)
    stac_dict = stac_item.to_dict()

    stac_dict['time']= {"interval": [stac_item.properties.start_datetime,
                                      stac_item.properties.end_datetime],
                        "resolution": "P1D"}
    stac_dict['crs'] = "https://www.opengis.net/def/crs/OGC/1.3/CRS84"

    # Save the STAC item to a JSON file
    output_file = os.path.join(output_folder, f"{stac_item.id}.json")
    with open(output_file, 'w') as f:
        json.dump(stac_dict, f, indent=2, default=str)

    print(f"STAC item created at {output_file}")

if __name__ == "__main__":
    netcdf_file_path = "~/Downloads/simulation.nc"  # Replace with your NetCDF file path
    output_directory = "tests/simulation"  # Replace with your desired output directory
    themes = {}
    main(netcdf_file_path, output_directory)
