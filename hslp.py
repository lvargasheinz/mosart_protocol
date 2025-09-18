from netCDF4 import Dataset
from scipy.stats import gumbel_r , gumbel_l
from osgeo import gdal
from os.path import isfile, join
from os import listdir
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#Insert the path for your file here
pathresult=join("./")
import numpy as np

import numpy as np
positions = np.array([[6, 7, 8],
                          [5, 0, 1],
                          [4, 3, 2]])
def get_highest_neighbor_clockwise(grid, x,y):
#    r_start, r_end = max(0, row-1), min(row, row+2)
 #   c_start, c_end = max(0, col-1), min(col, col+2)
#    rmax=max(row
 #   a=np.zeros((3,3))
#    a=grid[x-1:x+1,y-1:y+1] #,col-1:col+1
#    a[x,y]=np.nan
    a=grid
  #  print(a)
    max_value=np.nanmax(a)
    indx=np.where(max_value)
  
    # Create position mapping (clockwise starting from right)
    positions = np.array([[6, 7, 8],
                          [5, 0, 1],
                          [4, 3, 2]])
    pos=positions[indx]
    # Mask to exclude center cell
    #mask = np.ones_like(neighborhood, dtype=bool)
    #center_r, center_c = min(1, row-r_start), min(1, col-c_start)
    #mask[center_r, center_c] = False
    return (pos)#max_value, max_pos)
nc_results = [f for f in listdir(pathresult) if isfile(join(pathresult, f)) if f.endswith("area.nc")]
ds_data=[gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,'area')) for f in nc_results]
yrmax = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_data]
yrmax=np.asarray(yrmax)
ar=yrmax[0]
ds=np.sqrt(ar)#*1000
pathresult='./'
nc_results = [f for f in listdir(pathresult) if isfile(join(pathresult, f)) if f.endswith("dem2.nc")]
ds_data=[gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,'dem')) for f in nc_results]
dra = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_data]
dra=np.asarray(dra)

alt=dra[0]
alt=np.flip(alt,0)


#ds_data=[gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,'dra')) for f in nc_results]
#dra = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_data]
#dra=np.asarray(dra)
#dra=dra[0]
ds_lon = [gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,"lon")) for f in nc_results]
longitude = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_lon]
ds_lat = [gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,"lat")) for f in nc_results]
latitude = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_lat]
latitude=np.asarray(latitude)
longitude=np.asarray(longitude)
latitude=latitude[0]
latitude=latitude[0]
longitude=longitude[0]
longitude=longitude[0]
latitude=latitude.flatten()
longitude=longitude.flatten()

lon_size=np.size(longitude)
lat_size=np.size(latitude)
print(lon_size,lat_size)
#dnID
dz=np.zeros((np.shape(alt)))
dz2=np.zeros((np.shape(alt)))
slope=np.zeros((np.shape(alt)))
positions = np.array([[6, 7, 8],
                      [5, 0, 1],
                      [4, 3, 2]])
for i in range(lat_size):
 for j in range(lon_size):
  if i!=0 and j!=0 and i!=lat_size-1 and j!=lon_size-1:
   #a=dra[i-1:i+2,j-1:j+2]
   a=np.zeros((3,3))
   a[1,1]=np.nan
   a[1,0]=alt[i,j-1]
   a[0,1]=alt[i-1,j]
   a[0,0]=alt[i-1,j-1]
   a[1,2]=alt[i,j+1]
   a[2,1]=alt[i+1,j]
   a[2,2]=alt[i+1,j+1]
   a[0,2]=alt[i-1,j+1]
   a[2,0]=alt[i+1,j-1]
   min_z=np.nanmin(a)
   indx=np.where(a==min_z)
   dz[i,j]=alt[i,j]-np.nanmean(a)
   dz2[i,j]=alt[i,j]-min_z

slope=dz2/ds




## SAVE THE CALCULATED VALUE IN A NEW NETCDF FILE ##
try: ncfile.close()  # just to be safe, make sure dataset is not already open.
except: pass
ncfile = Dataset('hslp.nc',mode='w',format='NETCDF4_CLASSIC') # Decide here the name of your file 
print(ncfile)
lat_dim = ncfile.createDimension('lat', lat_size)     # latitude axis
lon_dim = ncfile.createDimension('lon', lon_size)    # longitude axis

ncfile.title="hslp"
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
Q = ncfile.createVariable('hslp',np.float64,('lat','lon')) # note: unlimited dimension is leftmost
lat[:]=latitude
lon[:]=longitude

# Write latitudes, longitudes.
data_arr=np.zeros((lat_size,lon_size))
data_arr=np.flip(slope,0) #np.flip(dnID,0)

# Write the data.  This writes the whole 3D netCDF variable all at once.
Q[:,:] = data_arr  

print("-- Wrote data, shape is now ", Q.shape)
#print("-- Min/Max values:",Q[:,:,:].min(), Q[:,:,:].max())

ncfile.close(); print('Dataset is closed!')


