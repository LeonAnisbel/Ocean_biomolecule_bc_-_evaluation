base_path='/work/bb1005/b381361/echam_data_pool/emissions_inventories/fesom_recom_marine/T63'

liste=$(ls -d ${base_path}/fesom_recom_sea_ice_*_T63.nc)
for i in $liste
do
fnm="${i%_*}"
dat=$(echo $fnm | cut -b 83-110)
#echo $i $dat
cdo gtc,10 ${i}  ${base_path}/${dat}_mask_T63.nc
done
