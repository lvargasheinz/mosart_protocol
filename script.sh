export chym_file="../new_input5/chym_stk.nc"
export mosart_half="../../eCLM_shared_data/common/mosart/MOSART_Global_half_20151015.nc"
export mosart_0125="../..//eCLM_newcases/eCLM_static-file-generator/mkmapgrids/rof_small.nc"

cp $chym_file .
python3 fdir.py
cdo griddes fdir.nc > grid.txt
cdo selvar,dra $chym_file dra.nc
cdo remapnn,grid.txt dra.nc dra2.nc 
cdo gridarea fdir.nc area.nc
ncrename -v cell_area,area area.nc
cdo mulc,1e6 dra2.nc areaTotal2.nc
ncrename -v dra,areaTotal2 areaTotal2.nc
cdo selvar,acc $chym_file acc.nc
python3 ID.py
rm tmp*nc
cdo selvar,msk $chym_file msk.nc
cdo setctomiss,1 msk.nc tmp.nc
cdo addc,1 tmp.nc tmp2.nc
cdo remapnn,grid.txt tmp2.nc frac.nc
ncrename -v msk,frac frac.nc 
rm tmp*nc
cp fdir.nc tmp.nc
cdo ifthen frac.nc tmp.nc fdir.nc
cdo ifthen frac.nc dra2.nc dra3.nc 
cdo ifthen frac.nc areaTotal2.nc areaTotal.nc
ncrename -v areaTotal2,areaTotal areaTotal.nc
python3 dnID.py
rm tmp*nc
cdo ifthen frac.nc dnID.nc tmp.nc
mv tmp.nc dnID.nc
python3 latixy.py
python3 longxy.py
rm tmp*nc
cdo mulc,1000 LENGTH_KM.nc tmp.nc
cdo remapdis,grid.txt tmp.nc tmp2.nc
cdo ifthen frac.nc tmp2.nc rlen.nc
ncrename -v Band1,rlen rlen.nc
cdo div rlen.nc area.nc gxr.nc
ncrename -v rlen,gxr gxr.nc
cdo selvar,dem $chym_file dem.nc
cdo remapnn,grid.txt dem.nc dem2.nc
python3 hslp.py
rm tmp*.nc
cdo div riv_tc_csu.nc ria_ha_csu.nc tmp.nc
cdo mulc,0.1 tmp.nc tmp2.nc
cdo remapdis,grid.txt tmp2.nc tmp4.nc
cdo setmisstoc,0 tmp4.nc tmp5.nc
cdo setrtomiss,-9999,2 tmp5.nc tmp6.nc
cdo setmisstoc,2 tmp6.nc tmp7.nc
cdo ifthen frac.nc tmp7.nc rdep.nc
ncrename -v Band1,rdep rdep.nc
rm tmp*nc
cdo mulc,1e-4 sgr_dk_rav.nc tmp.nc
cdo remapdis,grid.txt tmp.nc tmp2.nc
cdo ifthen frac.nc tmp2.nc rslp.nc
cdo ifthen frac.nc tmp2.nc tslp.nc
ncrename -v Band1,rslp rslp.nc
ncrename -v Band1,tslp tslp.nc
rm tmp*nc
cdo div ria_ha_csu.nc LENGTH_KM.nc tmp.nc
cdo mulc,10 tmp.nc tmp2.nc
cdo setmisstoc,0 tmp2.nc tmp4.nc
cdo setrtomiss,-9999,30 tmp4.nc tmp5.nc
cdo setmisstoc,30 tmp5.nc tmp6.nc
cdo remapdis,grid.txt tmp6.nc tmp7.nc
cdo ifthen frac.nc tmp7.nc rwid.nc
rm tmp*nc
ncrename -v Band1,rwid rwid.nc
cdo mulc,5 rwid.nc rwid0.nc
ncrename -v rwid,rwid0 rwid0.nc

cdo selvar,nh $mosart_half tmp.nc
cdo remapnn,grid.txt tmp.nc tmp2.nc
cdo ifthen frac.nc tmp2.nc nh.nc 
rm tmp*nc
cp areaTotal.nc tmp.nc
ncrename -v areaTotal,Band1 tmp.nc
ncap2 -s 'where(Band1<17e9) Band1=0.05;' tmp.nc tmp2.nc
ncap2 -s 'where(Band1>0.06) Band1=0.0477163;' tmp2.nc tmp3.nc
ncrename -v Band1,nr tmp3.nc
cdo ifthen frac.nc tmp3.nc nr.nc
cp nr.nc nt.nc 
ncrename -v nr,nt nt.nc
rm tmp*nc
cdo selvar,twid $mosart_0125 tmp.nc
cdo remapnn,grid.txt tmp.nc tmp2.nc
cdo ifthen frac.nc tmp2.nc twid.nc
rm tmp*nc
cdo merge twid.nc rwid.nc rwid0.nc latixy.nc longxy.nc nr.nc nh.nc nt.nc rdep.nc rlen.nc rslp.nc tslp.nc area.nc areaTotal.nc areaTotal2.nc dnID.nc fdir.nc frac.nc gxr.nc hslp.nc merged.nc
