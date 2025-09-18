from netCDF4 import Dataset
from scipy.stats import gumbel_r , gumbel_l
from osgeo import gdal
from os.path import isfile, join
from os import listdir
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#Insert here the size of your file
lon_size=111
lat_size=81
lon_size = 441 ;
lat_size = 321 ;



#Insert the path for your file here
pathresult=join("./")



nc_results = [f for f in listdir(pathresult) if isfile(join(pathresult, f)) if f.endswith("ID.nc")]

ds_lon = [gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,"lon")) for f in nc_results]
longitude = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_lon]
ds_lat = [gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,"lat")) for f in nc_results]
latitude = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_lat]
latitude=np.asarray(latitude)
longitude=np.asarray(longitude)
longitude2=np.asarray(longitude)
latitude=latitude[0]
latitude=latitude[0]
longitude=longitude[0]
longitude=longitude[0]
#longitude2=longitude2[0]
latitude=latitude.flatten()
longitude=longitude.flatten()
longitude=longitude#+180
longitude2=np.zeros((lat_size,lon_size))
for i in range(lon_size):
    longitude2[:,i]=longitude[i]

print(longitude)
print(latitude)
#print(latitude)38.8125 




## SAVE THE CALCULATED VALUE IN A NEW NETCDF FILE ##
try: ncfile.close()  # just to be safe, make sure dataset is not already open.
except: pass
ncfile = Dataset('longxy.nc',mode='w',format='NETCDF4_CLASSIC') # Decide here the name of your file 
print(ncfile)
lat_dim = ncfile.createDimension('lat', lat_size)     # latitude axis
lon_dim = ncfile.createDimension('lon', lon_size)    # longitude axis

ncfile.title="longxy"
print(ncfile.title)
print(ncfile)

# Define two variables with the same names as dimensions,
# a conventional way to define "coordinate variables".
lat = ncfile.createVariable('lat', np.float32, ('lat',))
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lon = ncfile.createVariable('lon', np.float32, ('lon',))
lon.units = 'degrees_east'
lon.long_name = 'longitude'
#	double dnID(ncl6, ncl7) 
# Define a 3D variable to hold the data
Q = ncfile.createVariable('longxy',np.float64,('lat','lon')) # note: unlimited dimension is leftmost
lat[:]=latitude
lon[:]=longitude

# Write latitudes, longitudes.
data_arr=np.zeros((lat_size,lon_size))
data_arr=longitude2 #np.flip(ID,0)

# Write the data.  This writes the whole 3D netCDF variable all at once.
Q[:,:] = data_arr  

print("-- Wrote data, shape is now ", Q.shape)
#print("-- Min/Max values:",Q[:,:,:].min(), Q[:,:,:].max())

ncfile.close(); print('Dataset is closed!')


