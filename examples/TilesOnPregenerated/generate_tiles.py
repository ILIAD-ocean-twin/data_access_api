
import os
import math
import numpy as np
import xarray as xr
from PIL import Image

# Constants for Web Mercator projection
TILE_SIZE = 256
INITIAL_RESOLUTION = 2 * math.pi * 6378137 / TILE_SIZE
ORIGIN_SHIFT = 2 * math.pi * 6378137 / 2.0

def latlon_to_meters(lat, lon):
    mx = lon * ORIGIN_SHIFT / 180.0
    my = math.log(math.tan((90 + lat) * math.pi / 360.0)) * 6378137
    return mx, my

def meters_to_pixels(mx, my, zoom):
    res = INITIAL_RESOLUTION / (2 ** zoom)
    px = (mx + ORIGIN_SHIFT) / res
    py = (ORIGIN_SHIFT - my) / res
    return int(px), int(py)

def pixels_to_tile(px, py):
    tx = int(px / TILE_SIZE)
    ty = int(py / TILE_SIZE)
    return tx, ty

def save_tile(tile_data, output_dir, z, x, y):
    os.makedirs(os.path.join(output_dir, str(z), str(x)), exist_ok=True)
    tile_path = os.path.join(output_dir, str(z), str(x), f"{y}.png")
    img = Image.fromarray(tile_data)
    img.save(tile_path)

def generate_tiles(netcdf_file, variable, output_dir="tiles", zoom_levels=range(0, 3)):
    ds = xr.open_dataset(netcdf_file)
    data = ds[variable].values
    lats = ds['lat'].values
    lons = ds['lon'].values

    for z in zoom_levels:
        print(f"Generating tiles for zoom level {z}...")
        for i in range(len(lats)):
            for j in range(len(lons)):
                lat = lats[i]
                lon = lons[j]
                value = data[i, j]

                mx, my = latlon_to_meters(lat, lon)
                px, py = meters_to_pixels(mx, my, z)
                tx, ty = pixels_to_tile(px, py)

                # Create a simple grayscale tile with the value
                tile_data = np.full((TILE_SIZE, TILE_SIZE), int(value) % 256, dtype=np.uint8)
                save_tile(tile_data, output_dir, z, tx, ty)

    print("Tile generation complete.")
