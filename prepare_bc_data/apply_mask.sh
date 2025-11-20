# Script used to create the sea ice mask used to compute OMF and biomolecules average values in sea ice free regions (SIC<10%)
base_path='../prepare_bc_data/orig_data/'

liste=$(ls -d ${base_path}ice_var_regular_grid_interp_wv_res025*.nc)
for i in $liste
do
fnm="${i}"
dat=$(echo $fnm | cut -b  11-52)
echo $i $dat
#cdo -setmisstoc,1 ${i} tmp.nc
#cdo -setmissval,1 tmp1.nc tmp.nc
cdo lec,0.1 ${i} tmp.nc
cdo -setmisstoc,1  tmp.nc tmp1.nc
cdo setrtomiss,0,0.5 tmp1.nc mask_${dat}.nc 
done
