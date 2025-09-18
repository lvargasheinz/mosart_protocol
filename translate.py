import geopandas as gpd
import numpy as np
from os.path import isfile, join, expanduser
import rasterio
from rasterio.transform import from_origin
from rasterio.features import rasterize
import os
def shapefile_to_raster(input_shp, output_tif, attribute, resolution=10):
    """
    Convert a shapefile to raster for a given attribute.
    
    Parameters:
    - input_shp: Path to input shapefile
    - output_tif: Path for output GeoTIFF
    - attribute: Attribute name to rasterize
    - resolution: Output raster resolution in units of shapefile CRS
    """
    
    # 1. Read the shapefile
    gdf = gpd.read_file(input_shp)
    
    # 2. Get the bounds and calculate raster dimensions
    bounds = gdf.total_bounds
    width = int((bounds[2] - bounds[0]) / resolution)
    height = int((bounds[3] - bounds[1]) / resolution)
    
    # 3. Create transform
    transform = from_origin(bounds[0], bounds[3], resolution, resolution)
    
    # 4. Rasterize the shapes with the attribute values
    shapes = ((geom, value) for geom, value in zip(gdf.geometry, gdf[attribute]))
    raster = rasterize(
        shapes=shapes,
        out_shape=(height, width),
        transform=transform,
        fill=0,  # background value
        dtype=np.float32
    )
    
    # 5. Save the raster
    with rasterio.open(
        output_tif,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=raster.dtype,
        crs=gdf.crs,
        transform=transform,
    ) as dst:
        dst.write(raster, 1)

# Example usage:
#calculation = os.environ.get('calculation')
attr=os.environ.get('attr')
shapefile_to_raster(
    input_shp='../new_input/hydrosheds/RiverATLAS_v10_eu.shp',
    output_tif='output.tif',
    attribute=attr,  # replace with your attribute name
    resolution=0.03125 # adjust resolution as neede
)
from osgeo import gdal
gdal.Translate(join(attr+'.nc'),'output.tif',format='NetCDF',noData=-9999)
