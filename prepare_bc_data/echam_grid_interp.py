# script to interpolate regular fesom-recom grid (volume-weighted data) to ECHAM grid (T63) 
import glob
import os
import shutil
path_data='/work/bb1005/b381361/MOA_DATA_ECHAM/'
path_init = f'{path_data}orig_data/'
path_final = path_data

path_new = path_data+'fesom_recom_marine/T63/'

files_pol = glob.glob(path_init + 'PCHO*')
files_pro = glob.glob(path_init + 'DAA*')
files_lip = glob.glob(path_init + 'Lipids*')
files_ice = glob.glob(path_init + 'ice*')
files_sst = glob.glob(path_init + 'sst*')

for i,fi in enumerate(files_pol):
        yr = fi[-7:-3]
        os.system(f'cdo remapcon,dust_potential_sources_T63.nc {fi} {path_final}init_POL_marineaerosol_{yr}_T63.nc')
        os.system(f'cdo setreftime,{yr}-01-01,00:00:00,days -settaxis,{yr}-01-01,00:00:00,1month '
                  f'{path_final}init_POL_marineaerosol_{yr}_T63.nc {path_final}ocean_macromolecules_POL_marineaerosol_{yr}_T63.nc')

        os.system(f'cdo remapcon,dust_potential_sources_T63.nc {files_pro[i]} {path_final}init_PRO_marineaerosol_{yr}_T63.nc')
        os.system(f'cdo setreftime,{yr}-01-01,00:00:00,days -settaxis,{yr}-01-01,00:00:00,1month '
                  f'{path_final}init_PRO_marineaerosol_{yr}_T63.nc {path_final}ocean_macromolecules_PRO_marineaerosol_{yr}_T63.nc')


        os.system(f'cdo remapcon,dust_potential_sources_T63.nc {files_lip[i]} {path_final}init_LIP_marineaerosol_{yr}_T63.nc')
        os.system(f'cdo setreftime,{yr}-01-01,00:00:00,days -settaxis,{yr}-01-01,00:00:00,1month '
                  f'{path_final}init_LIP_marineaerosol_{yr}_T63.nc {path_final}ocean_macromolecules_LIP_marineaerosol_{yr}_T63.nc')

        os.system(f'cdo remapcon,dust_potential_sources_T63.nc {files_ice[i]} {path_final}init_fesom_recom_sea_ice_{yr}_T63.nc')
        os.system(f'cdo setreftime,{yr}-01-01,00:00:00,days -settaxis,{yr}-01-01,00:00:00,1month '
                  f'{path_final}init_fesom_recom_sea_ice_{yr}_T63.nc {path_final}fesom_recom_sea_ice_{yr}_T63.nc')

        os.system(f'cdo remapcon,dust_potential_sources_T63.nc {files_sst[i]} {path_final}init_fesom_recom_sst_{yr}_T63.nc')
        os.system(f'cdo setreftime,{yr}-01-01,00:00:00,days -settaxis,{yr}-01-01,00:00:00,1month '
                  f'{path_final}init_fesom_recom_sst_{yr}_T63.nc {path_final}fesom_recom_sst_{yr}_T63.nc')


os.system('bash apply_ice_mask.sh')
try:
        os.remove(f'{path_data}init*')
except OSError as error:
        print('No init files to remove')

try:
        shutil.move(f'{path_data}ocean_macromolecules_*.nc',path_new)
        shutil.move(f'{path_data}fesom_recom_*.nc',path_new)
except OSError as error:
        print('No files to move')

print('done')
