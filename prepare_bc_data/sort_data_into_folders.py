import numpy as np 
import glob,os
import shutil


years = np.arange(1990,2020)
path_data='/work/bb1005/b381361/MOA_DATA_ECHAM/'
path_new = path_data+'fesom_recom_marine/T63/'
# no year files
os.system(f'rm {path_data}/init*')
os.system(f'mv {path_data}/*marineaerosol*')
#####

for i in years:
    #try:
     #   os.mkdir(path_new+str(i))
        
    #except OSError:
     #   pass
    
    files_pol = glob.glob(f'{path_data}*POL_marineaerosol_{str(i)}_T63.nc')
    files_pro = glob.glob(f'{path_data}*PRO_marineaerosol_{str(i)}_T63.nc')
    files_lip = glob.glob(f'{path_data}*LIP_marineaerosol_{str(i)}_T63.nc')    
    #print(files)
    #for i,fi in enumerate(files_pol):
     
        #if os.path.exists(f'{path_new}{str(i)}/{fi[len(path_data):]}'):
         #   os.remove(f'{path_new}{str(i)}/{fi[len(path_data):]}')
            
        #else:
            #{str(i)}
         #   shutil.move(fi,f'{path_new}')



 

