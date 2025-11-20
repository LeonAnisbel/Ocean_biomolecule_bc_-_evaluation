#replace nan values by null for all biomolecule groups
base_path="/work/bb1005/b381361/MOA_DATA_ECHAM/fesom_recom_marine"
exp="ac3_arctic"
liste=$(ls -d ${base_path}/T63_nan/ocean_macromolecules_*.nc)
rm tmp_*


for i in $liste
do

fnm="${i%_*}"
#dat=$(echo $fnm | cut -b 67-72)
#dat=$(echo $fnm | cut -b 59-72)

dat=$(echo $fnm | cut -b 64-140)

echo $i $dat

cdo setmisstoc,0 ${i} ${base_path}/T63/${dat}_T63.nc

done
