from netCDF4 import Dataset
from scipy.stats import gumbel_r , gumbel_l
from osgeo import gdal
from os.path import isfile, join
from os import listdir
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
#Insert the path for your file here
pathresult=join("./")
import numpy as np

import numpy as np
positions = np.array([[6, 7, 8],
                          [5, 0, 1],
                          [4, 3, 2]])
pathresult='./'
D8_CODES = {
    1: (0, 1),   # East
    2: (-1, 1),   # Northeast
    4: (-1, 0),   # North
    8: (-1, -1),  # Northwest
    16: (0, -1),   # West
    32: (1, -1),  # Southwest
    64: (1, 0),   # South
    128: (1, 1)    # Southeast
}
args=[0,1,2,3,4,5,6,7,8]
args_fdir=[32,64,128,16,0,1,8,4,2]
args_fdir_ops=[2,4,8,1,0,16,128,64,32]


nc_results = [f for f in listdir(pathresult) if isfile(join(pathresult, f)) if f.startswith("ID.nc")]
ds_data=[gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,'ID')) for f in nc_results]
yrmax = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_data]
yrmax=np.asarray(yrmax)
ID=yrmax[0]
pathresult='./'
nc_results = [f for f in listdir(pathresult) if isfile(join(pathresult, f)) if f.endswith("dra3.nc")]
ds_data=[gdal.Open("NETCDF:{0}:{1}".format(pathresult + f,'dra')) for f in nc_results]
dra = [f.ReadAsArray(0, 0, f.RasterXSize, f.RasterYSize) for f in ds_data]
dra=np.asarray(dra)
dra=dra[0]

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
control_frac=np.zeros((np.shape(ID)))
print(lon_size,lat_size)
dnID=np.zeros((np.shape(ID)))

dra[0,:]=-9999
dra[lat_size-1,:]=-9999


dra[:,0]=-9999

dra[:,lon_size-1]=-9999

for i in range(lat_size):
 for j in range(lon_size):
  if dra[i,j]<=0:
    dnID[i,j]=-9999
    control_frac[i,j]=-9999
#    dra[i,j]=0
for i in range(lat_size):
 for j in range(lon_size):
  if i!=0 and j!=0 and i!=lat_size-1 and j!=lon_size-1: #and dra[i,j]>0:
   a=dra[i-1:i+2,j-1:j+2]
   max_value=np.nanmax(a)
   a_flat=a.flatten()
   indx=np.argmax(a_flat)
   indx0=indx
   ids=ID[i-1:i+2,j-1:j+2]
   ids_flat=ids.flatten()
   if max_value==0:
    dnID[i,j]=-9999
   else:
    dnID[i,j]=ids_flat[indx0]


dnID2=dnID*1


dnID[0,:]=-9999
dnID[lat_size-1,:]=-9999

dnID[:,0]=-9999
dnID[:,lon_size-1]=-9999

vish=0
vish0=0
for i in range(lat_size):
 for j in range(lon_size):
  if i!=0 and j!=0 and i!=lat_size-1 and j!=lon_size-1:
    limits=1
    a=np.zeros((3,3))
    a[0,0]=dra[i-1,j-1]
    a[0,1]=dra[i-1,j]
    a[1,0]=dra[i,j-1]
#    a[1,1]=dra[i,j]
    a[2,0]=dra[i+1,j-1]
    a[0,2]=dra[i-1,j+1]
    a[1,2]=dra[i,j+1]
    a[2,1]=dra[i+1,j]
    a[2,2]=dra[i+1,j+1]
    if dra[i,j]<=0:
     if np.any(a)<=0:
         print('ok')
#     else: 
 #     dnID[i,j]=ID[i,j]
for i in range(lat_size):
 for j in range(lon_size):
   if ID[i,j]==58536:
    print(dnID[i,j],'alo')
    print(dra[i,j],'alo')
for i in range(lat_size):
 for j in range(lon_size):
  dra2=dra*1
  if i!=0 and j!=0 and i!=lat_size-1 and j!=lon_size-1:
  # print(dnID[451,1437],i,j)
   if dnID[i,j]==0 or dnID[i,j]==ID[i,j]:
    vish0=vish0+1
    limits=1
    a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
    a[limits,limits]=np.nan
    b=a[(~np.isnan(a)) & (a<0)]
    center=dra[i,j]
    if center==0:
                center=1e20
    c=a[(~np.isnan(a)) & (a> center)]
    if np.size(b)>0 or np.size(c)>0:
     if np.size(b)>0:
      positions=np.argwhere((~np.isnan(a)) & (a<0))
#      print(positions,a)
     else:
      positions=np.argwhere((~np.isnan(a)) & (a> center))
#     print(a,positions)
     target_row, target_col = positions[0]
     dy = target_col - limits
     dx = target_row - limits
     dxx=np.zeros(limits)
     dyy=np.zeros(limits)
     dxx[:abs(dx)]=dx/abs(dx)
     dyy[:abs(dy)]=dy/abs(dy)
     for m in range(limits):
      dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
    else:
     limits=2
     a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
     a[limits,limits]=np.nan
     b=a[(~np.isnan(a)) & (a<0)]
     center=dra[i,j]
     if center==0:
                center=1e20
     c=a[(~np.isnan(a)) & (a> center)]
     if np.size(b)>0 or np.size(c)>0:
      if np.size(b)>0:
        positions=np.argwhere((~np.isnan(a)) & (a<0))
      else:
        positions=np.argwhere((~np.isnan(a)) & (a> center))
      target_row, target_col = positions[0]
      dy = target_col - limits
      dx = target_row - limits
      dxx=np.zeros(limits)
      dyy=np.zeros(limits)
      dxx[:abs(dx)]=dx/abs(dx)
      dyy[:abs(dy)]=dy/abs(dy)
      for m in range(limits):
        dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
     else:
      limits=3
      a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
      a[limits,limits]=np.nan
      b=a[(~np.isnan(a)) & (a<0)]
      center=dra[i,j]
      if center==0:
                center=1e20
      c=a[(~np.isnan(a)) & (a> center)]
      if np.size(b)>0 or np.size(c)>0:
       if np.size(b)>0:
        positions=np.argwhere((~np.isnan(a)) & (a<0))
       else:
#    if np.size(c)>0:
        positions=np.argwhere((~np.isnan(a)) & (a> center))
       target_row, target_col = positions[0]
       dy = target_col - limits
       dx = target_row - limits
       dxx=np.zeros(limits)
       dyy=np.zeros(limits)
       dxx[:abs(dx)]=dx/abs(dx)
       dyy[:abs(dy)]=dy/abs(dy)
       for m in range(limits):
        dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
      else:
       limits=4
       a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
       a[limits,limits]=np.nan
       b=a[(~np.isnan(a)) & (a<0)]
       center=dra[i,j]
       if center==0:
                center=1e20
       c=a[(~np.isnan(a)) & (a> center)]
       if np.size(b)>0 or np.size(c)>0:
        if np.size(b)>0:
         positions=np.argwhere((~np.isnan(a)) & (a<0))
        else: 
   #      np.size(c)>0:
         positions=np.argwhere((~np.isnan(a)) & (a> center))
        target_row, target_col = positions[0]
        dy = target_col - limits
        dx = target_row - limits
        dxx=np.zeros(limits)
        dyy=np.zeros(limits)
        dxx[:abs(dx)]=dx/abs(dx)
        dyy[:abs(dy)]=dy/abs(dy)
        for m in range(limits):
         dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
       else:
        limits=5
        a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
        a[limits,limits]=np.nan
        b=a[(~np.isnan(a)) & (a<0)]
        center=dra[i,j]
        if center==0:
                center=1e20
        c=a[(~np.isnan(a)) & (a> center)]
        if np.size(b)>0 or np.size(c)>0 and ID[i,j]!=1227389:
         if np.size(b)>0:
          positions=np.argwhere((~np.isnan(a)) & (a<0))
         else:
#         if np.size(c)>0:
          positions=np.argwhere((~np.isnan(a)) & (a> center))
         target_row, target_col = positions[0]
         dy = target_col - limits
         dx = target_row - limits
         dxx=np.zeros(limits)
         dyy=np.zeros(limits)
         dxx[:abs(dx)]=dx/abs(dx)
         dyy[:abs(dy)]=dy/abs(dy)
         for m in range(limits):
          dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
        else:
         limits=6
         a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
         a[limits,limits]=np.nan
         b=a[(~np.isnan(a)) & (a<0)]
         center=dra[i,j]
         if center==0:
                center=1e20
         c=a[(~np.isnan(a)) & (a> center)]
         if np.size(b)>0 or np.size(c)>0:
          if np.size(b)>0:
           positions=np.argwhere((~np.isnan(a)) & (a<0))
          else:
           positions=np.argwhere((~np.isnan(a)) & (a> center))
          target_row, target_col = positions[0]
          if ID[i,j]==1227389:
            target_row, target_col = positions[1]
          dy = target_col - limits
          dx = target_row - limits
          dxx=np.zeros(limits)
          dyy=np.zeros(limits)
          dxx[:abs(dx)]=dx/abs(dx)
          dyy[:abs(dy)]=dy/abs(dy)
          for m in range(limits):
           dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
         else:
          limits=7
          a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
          a[limits,limits]=np.nan
          b=a[(~np.isnan(a)) & (a<0)]
          center=dra[i,j]
          if center==0:
                center=1e20
          c=a[(~np.isnan(a)) & (a> center)]
          if np.size(b)>0 or np.size(c)>0:
           if np.size(b)>0:
            positions=np.argwhere((~np.isnan(a)) & (a<0))
           else:
            positions=np.argwhere((~np.isnan(a)) & (a> center))
           target_row, target_col = positions[0]
           dy = target_col - limits
           dx = target_row - limits
           dxx=np.zeros(limits)
           dyy=np.zeros(limits)
           dxx[:abs(dx)]=dx/abs(dx)
           dyy[:abs(dy)]=dy/abs(dy)
           for m in range(limits):
            dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
          else:
           limits=8
           a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
           a[limits,limits]=np.nan
           b=a[(~np.isnan(a)) & (a<0)]
           center=dra[i,j]
           if center==0:
                center=1e20
           c=a[(~np.isnan(a)) & (a> center)]
           if np.size(b)>0 or np.size(c)>0:
            if np.size(b)>0:
             positions=np.argwhere((~np.isnan(a)) & (a<0))
            else:
             positions=np.argwhere((~np.isnan(a)) & (a> center))
            target_row, target_col = positions[0]
            dy = target_col - limits
            dx = target_row - limits
            dxx=np.zeros(limits)
            dyy=np.zeros(limits)
            dxx[:abs(dx)]=dx/abs(dx)
            dyy[:abs(dy)]=dy/abs(dy)
            for m in range(limits):
             dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
           else:
            limits=9
            a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
            a[limits,limits]=np.nan
            b=a[(~np.isnan(a)) & (a<0)]
            center=dra[i,j]
            if center==0:
                center=1e20
            c=a[(~np.isnan(a)) & (a> center)]
            if np.size(b)>0 or np.size(c)>0:
             if np.size(b)>0:
              positions=np.argwhere((~np.isnan(a)) & (a<0))
             else:
              positions=np.argwhere((~np.isnan(a)) & (a> center))
             target_row, target_col = positions[0]
             dy = target_col - limits
             dx = target_row - limits
             dxx=np.zeros(limits)
             dyy=np.zeros(limits)
             dxx[:abs(dx)]=dx/abs(dx)
             dyy[:abs(dy)]=dy/abs(dy)
             for m in range(limits):
              dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
 #             print(dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))])
#              print(ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))])
            else:
                vish=vish+1
                a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
                a[limits,limits]=np.nan
#                p=np.argmax(


           #     print(ID[i,j],'aaa')
   #a[limits,limits]=center

for i in range(lat_size):
 for j in range(lon_size):
   if ID[i,j]==58536:
    print(dnID[i,j],'alo')
    print(dra[i,j],'alo')


for i in range(lat_size):
 for j in range(lon_size):
   if ID[i,j]==2006:
    print(dnID[i,j],'alo2')
   if i==138 and j==7:
#       print(dra[i-7:i+8,j-7:j+8])
       print(dra[i-2:i+3,j-2:j+3])
       print(ID[i,j],dnID[i,j])
print(vish,vish0,'vishshh')
dnID[0,:]=-9999
dnID[lat_size-1,:]=-9999

dnID[:,0]=-9999
dnID[:,lon_size-1]=-9999
for i in range(lat_size):
 for j in range(lon_size):
   if ID[i,j]==164102:#i==456 and j==1438:#ID[i,j]==123564099: #574056: #494882: #513020: #484975: #289139 : #292441: #126357: #12694:
    print('aaa',dnID[i-2:i+3,j-2:j+3])
    print(ID[i-2:i+3,j-2:j+3])
    print(dra[i-2:i+3,j-2:j+3])
    print(dnID[i-3:i+4,j-3:j+4])
    print(ID[i-3:i+4,j-3:j+4])
    print(dra[i-3:i+4,j-3:j+4])


print('new effort',vish)
for i in range(lat_size):
 for j in range(lon_size):
    if i==98 and j==204:
        print(dra[i-3:i+4,j-3:j+4])
        print('hereeee')
        print(np.max(dra[i-4:i+5,j-4:j+5]))
        print(np.min(dra[i-4:i+5,j-4:j+5]))
        print(np.max(dra[i-36:i+37,j-36:j+37]))
        print(np.min(dra[i-36:i+37,j-36:j+37]))
#        plt.imshow(dra[i-36:i+37,j-36:j+37])
 #       plt.show()
        print(longitude[j],latitude[j])
        print('done')

vish=0
dra2=dra*1
for i in range(lat_size):
 for j in range(lon_size):
  dra2=dra*1
  if i!=0 and j!=0 and i!=lat_size-1 and j!=lon_size-1 and i==100000000:
  # print(dnID[451,1437],i,j)
   if dnID[i,j]==0 or dnID[i,j]==ID[i,j]:
    if ID[i,j]==2006:
        print('im here')
    vish0=vish0+1
    limits=10
    if center==0:
                center=1e20
    a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
    print(ID[i,j],i,j)
    a[limits,limits]=np.nan
    b=a[(~np.isnan(a)) & (a<0)]
    center=dra[i,j]
    c=a[a>center]
    if np.size(b)>0 or np.size(c)>0:
     if ID[i,j]==2006:
         print('im here')
         print(b)
         print(c)
         print(a)
     if np.size(b)>0:
      positions=np.argwhere((~np.isnan(a)) & (a<0))
     else:
      positions=np.argwhere(a>center)
     if ID[i,j]==2006:
         print('im here')
         print(positions)
     target_row, target_col = positions[0]
     dy = target_col - limits
     dx = target_row - limits
     dxx=np.zeros(limits)
     dyy=np.zeros(limits)
     dxx[:abs(dx)]=dx/abs(dx)
     dyy[:abs(dy)]=dy/abs(dy)
     for m in range(limits):
      dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
     if ID[i,j]==2006:
      print('im here3')    
      print(dnID[i,j])
    else:
     limits=11
     if center==0:
                center=1e20
     a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
     a[limits,limits]=np.nan
     b=a[np.argwhere((~np.isnan(a)) & (a<0))]
     center=dra[i,j]
     c=a[a>center]
     if np.size(b)>0 or np.size(c)>0:
      if np.size(b)>0:
        positions=np.argwhere(np.argwhere((~np.isnan(a)) & (a<0)))
      else:
        positions=np.argwhere(a>center)
      target_row, target_col = positions[0]
      dy = target_col - limits
      dx = target_row - limits
      dxx=np.zeros(limits)
      dyy=np.zeros(limits)
      dxx[:abs(dx)]=dx/abs(dx)
      dyy[:abs(dy)]=dy/abs(dy)
      for m in range(limits):
        dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
     else:
      limits=12
      if center==0:
                center=1e20
      a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
      a[limits,limits]=np.nan
      b=a[np.argwhere((~np.isnan(a)) & (a<0))]
      center=dra[i,j]
      c=a[a>center]
      if np.size(b)>0 or np.size(c)>0:
       if np.size(b)>0:
        positions=np.argwhere(np.argwhere((~np.isnan(a)) & (a<0)))
       else:
#    if np.size(c)>0:
        positions=np.argwhere(a>center)
       target_row, target_col = positions[0]
       dy = target_col - limits
       dx = target_row - limits
       dxx=np.zeros(limits)
       dyy=np.zeros(limits)
       dxx[:abs(dx)]=dx/abs(dx)
       dyy[:abs(dy)]=dy/abs(dy)
       for m in range(limits):
        dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
      else:
       limits=13
       if center==0:
                center=1e20
       a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
       a[limits,limits]=np.nan
       b=a[np.argwhere((~np.isnan(a)) & (a<0))]
       center=dra[i,j]
       c=a[a>center]
       if np.size(b)>0 or np.size(c)>0:
        if np.size(b)>0:
         positions=np.argwhere(np.argwhere((~np.isnan(a)) & (a<0)))
        else: 
   #      np.size(c)>0:
         positions=np.argwhere(a>center)
        target_row, target_col = positions[0]
        dy = target_col - limits
        dx = target_row - limits
        dxx=np.zeros(limits)
        dyy=np.zeros(limits)
        dxx[:abs(dx)]=dx/abs(dx)
        dyy[:abs(dy)]=dy/abs(dy)
        for m in range(limits):
         dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
       else:
        limits=14
        if center==0:
                center=1e20
        a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
        a[limits,limits]=np.nan
        b=a[np.argwhere((~np.isnan(a)) & (a<0))]
        center=dra[i,j]
        c=a[a>center]
        if np.size(b)>0 or np.size(c)>0 and ID[i,j]!=1227389:
         if np.size(b)>0:
          positions=np.argwhere(np.argwhere((~np.isnan(a)) & (a<0)))
         else:
#         if np.size(c)>0:
          positions=np.argwhere(a>center)
         target_row, target_col = positions[0]
         dy = target_col - limits
         dx = target_row - limits
         dxx=np.zeros(limits)
         dyy=np.zeros(limits)
         dxx[:abs(dx)]=dx/abs(dx)
         dyy[:abs(dy)]=dy/abs(dy)
         for m in range(limits):
          dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
        else:
         limits=15
         a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
         a[limits,limits]=np.nan
         b=a[np.argwhere((~np.isnan(a)) & (a<0))]
         center=dra[i,j]
         c=a[a>center]
         if np.size(b)>0 or np.size(c)>0:
          if dnID[i,j]==574056:
             print('found it')
          if np.size(b)>0:
           positions=np.argwhere(np.argwhere((~np.isnan(a)) & (a<0)))
          else:
           positions=np.argwhere(a>center)
          target_row, target_col = positions[0]
          if ID[i,j]==1227389:
            target_row, target_col = positions[1]
          dy = target_col - limits
          dx = target_row - limits
          print(ID[i+dx,j+dy])
          print(dra[i+dx,j+dy])
          print(positions[0])
          dxx=np.zeros(limits)
          dyy=np.zeros(limits)
          dxx[:abs(dx)]=dx/abs(dx)
          dyy[:abs(dy)]=dy/abs(dy)
          for m in range(limits):
           dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
         else:
          limits=16
          a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
          a[limits,limits]=np.nan
          b=a[np.argwhere((~np.isnan(a)) & (a<0))]
          center=dra[i,j]
          c=a[a>center]
          if np.size(b)>0 or np.size(c)>0:
           if np.size(b)>0:
            positions=np.argwhere(np.argwhere((~np.isnan(a)) & (a<0)))
           else:
            positions=np.argwhere(a>center)
           target_row, target_col = positions[0]
           dy = target_col - limits
           dx = target_row - limits
           dxx=np.zeros(limits)
           dyy=np.zeros(limits)
           dxx[:abs(dx)]=dx/abs(dx)
           dyy[:abs(dy)]=dy/abs(dy)
           for m in range(limits):
            dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
          else:
           limits=17
           a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
           a[limits,limits]=np.nan
           b=a[np.argwhere((~np.isnan(a)) & (a<0))]
           center=dra[i,j]
           c=a[a>center]
           if np.size(b)>0 or np.size(c)>0:
            if np.size(b)>0:
             positions=np.argwhere(np.argwhere((~np.isnan(a)) & (a<0)))
            else:
             positions=np.argwhere(a>center)
            target_row, target_col = positions[0]
            dy = target_col - limits
            dx = target_row - limits
            dxx=np.zeros(limits)
            dyy=np.zeros(limits)
            dxx[:abs(dx)]=dx/abs(dx)
            dyy[:abs(dy)]=dy/abs(dy)
            for m in range(limits):
             dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
           else:
            limits=18
            a=dra2[i-limits:i+1+limits,j-limits:j+1+limits]
            a[limits,limits]=np.nan
            b=a[np.argwhere((~np.isnan(a)) & (a<0))]
            center=dra[i,j]
            if center==0:
                center=1e20
            c=a[a>center]
            if np.size(b)>0 or np.size(c)>0:
             if np.size(b)>0:
              positions=np.argwhere(np.argwhere((~np.isnan(a)) & (a<0)))
             else:
              positions=np.argwhere(a>center)
             target_row, target_col = positions[0]
             dy = target_col - limits
             dx = target_row - limits
             dxx=np.zeros(limits)
             dyy=np.zeros(limits)
             dxx[:abs(dx)]=dx/abs(dx)
             dyy[:abs(dy)]=dy/abs(dy)
             for m in range(limits):
              dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))]=ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))]
 #             print(dnID[int(i+np.sum(dxx[:m])),int(j+np.sum(dyy[:m]))])
#              print(ID[int(i+np.sum(dxx[:m+1])),int(j+np.sum(dyy[:m+1]))])
             if ID[i,j]==1235640:
                 print(positions[0])
                 print('look here',a)
                 print(dnID[i-limits:i+1+limits,j-limits:j+1+limits])
                 print(ID[i-limits:i+1+limits,j-limits:j+1+limits])
                 print(dra[i-limits:i+1+limits,j-limits:j+1+limits])
                 print(dnID[i-3:i+4,j-3:j+4])
            else:
                vish=vish+1
   a[limits,limits]=center
print(vish,'vishhhh')
for i in range(lat_size):
 for j in range(lon_size):
   if ID[i,j]==2890:
    print(dnID[i,j],'alo3')

print('new effort',vish)
for i in range(lat_size):
 for j in range(lon_size):
  if ID[i,j]==623458:
   teste=dnID[i-3:i+4,j-3:j+4]
   print(teste-teste0,'teste3')
  if ID[i,j]==1235638:
      print(dnID[i,j])


for i in range(lat_size):
 for j in range(lon_size):
  if ID[i,j]==493233: #513020: #484975: #289139 : #292441: #126357: #12694:
    print(dra[i-9:i+10,j-9:j+10])
print(vish,'vish')
vish=0


print((vish,'vish'))

control_frac[dnID==-9999]=-9999
#dnID[:,lon_size-4:lon_size-1]=-9999

for i in range(lat_size):
 for j in range(lon_size):
  if ID[i,j]==623458:
   teste=dnID[i-3:i+4,j-3:j+4]
   print(teste-teste0,'teste4')
  if ID[i,j]==1329:
      print(dnID[i,j])
      dnID[i,j]=1330
  if ID[i,j]==139803:
      dnID[i,j]=140244
#plt.show()

if ID[i,j]==623458:
 teste=dnID[i-3:i+4,j-3:j+4]
 print(teste-teste0)
for i in range(lat_size):
 for j in range(lon_size):
   if ID[i,j]==25491:#i==456 and j==1438:#ID[i,j]==123564099: #574056: #494882: #513020: #484975: #289139 : #292441: #126357: #12694:
    print('starts here')
    print(dnID[i-2:i+3,j-2:j+3])
    print(ID[i-2:i+3,j-2:j+3])
    print(dra[i-2:i+3,j-2:j+3])
    print(dnID[i-3:i+4,j-3:j+4])
    print(ID[i-3:i+4,j-3:j+4])
    print(dra[i-3:i+4,j-3:j+4])
    print(dnID[i-4:i+5,j-4:j+5])
    print(ID[i-4:i+5,j-4:j+5])
    print(1,dra[i-4:i+5,j-4:j+5])
    print(2,dra[i-5:i+6,j-5:j+6])
    print(3,dra[i-6:i+7,j-6:j+7])
    print(4,dra[i-7:i+8,j-7:j+8])
    print(5,dra[i-8:i+9,j-8:j+9])
    print(6,dra[i-9:i+10,j-9:j+10])
    print(dnID[i-9:i+10,j-9:j+10])
    print(ID[i-9:i+10,j-9:j+10])
    print(i,j)

## SAVE THE CALCULATED VALUE IN A NEW NETCDF FILE ##
try: ncfile.close()  # just to be safe, make sure dataset is not already open.
except: pass
ncfile = Dataset('dnID.nc',mode='w',format='NETCDF4_CLASSIC') # Decide here the name of your file 
print(ncfile)
lat_dim = ncfile.createDimension('lat', lat_size)     # latitude axis
lon_dim = ncfile.createDimension('lon', lon_size)    # longitude axis

ncfile.title="dnID"
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
Q = ncfile.createVariable('dnID',np.float64,('lat','lon')) # note: unlimited dimension is leftmost
lat[:]=latitude
lon[:]=longitude

# Write latitudes, longitudes.
data_arr=np.zeros((lat_size,lon_size))
data_arr=dnID

# Write the data.  This writes the whole 3D netCDF variable all at once.
Q[:,:] = data_arr  

print("-- Wrote data, shape is now ", Q.shape)
#print("-- Min/Max values:",Q[:,:,:].min(), Q[:,:,:].max())

ncfile.close(); print('Dataset is closed!')


