from osgeo import gdal
gdal.Translate('acc0.nc','tif/hyd_eu_acc_30s.tif',format='NetCDF',noData=-9999)

