import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy as cart
import math
import matplotlib as mpl
import codecs
import os,glob,sys
import matplotlib.ticker as ticker
def read_files_data(path_dir):
    data = xr.open_mfdataset(path_dir,concat_dim='time', combine='nested')
    return data
    
def get_month(da,m):
    da_yr = da
    da_t = da_yr.where(da_yr.time.dt.month == m,drop=True)
    print(da_t)

    da_t_lalo = da_t        
    return da_t_lalo


def percent_trend(da_yr):
    perc_trend=[]
    for y,year in enumerate(da_yr.time.values[:-1]):
        
        perc_trend.append(((da_yr.isel(time = y+1)-da_yr.isel(time = y))))
    return xr.concat(perc_trend,dim = 'time')

def rename_time(C):
    C_mean = C['time'].dt.year    
    return C_mean



def get_monthly_mean(variable,months,yr_cond):
    v_tri_mo_var = []
    v_tri_std_var = []    
    for v in variable:

        v_month = []   
        std_month = []
        for m in months:
            v_ti = get_month(v,m)
            v_ti = v_ti.where((v_ti.time.dt.year>yr_cond[0])&
                            (v_ti.time.dt.year<yr_cond[1]),drop=True)

            v_ti = v_ti.mean(dim='time',skipna=True)

            v_month.append(v_ti)

        v_tri_mo_var.append(xr.concat(v_month,dim = 'time'))
        

    return v_tri_mo_var
    


def plot_help(subfig,C,titles,vm, units, colorbar):
    months = 4
    axes = subfig.subplots(nrows=1, ncols=1, sharex=True,
                         subplot_kw={'projection': ccrs.Robinson()})
#     for i,ax in enumerate(axes):
    cmap = plt.get_cmap(colorbar, 11)    # 11 discrete colors
    im = axes.pcolormesh(C.lon, C.lat, C,#.isel(time = months),
                        cmap=cmap, transform=ccrs.PlateCarree(),
                       vmin = 0,vmax = vm)
    axes.set_title(titles[0],loc='right', fontsize = 12)
    axes.set_title(titles[1], loc='left', fontsize = 12)
    axes.coastlines()


    cbar = subfig.colorbar(im, orientation="horizontal", extend = 'max')#,cax = cbar_ax
    cbar.ax.tick_params(labelsize=12)
    cbar.set_label(label=units, size='large', weight='bold')



def plot_6_pannel(C,names,vm):
    fig = plt.figure(constrained_layout=True,figsize = (10,7))

    (subfig1,subfig2,subfig3), (subfig4, subfig5, subfig6) = fig.subfigures(nrows = 2, ncols = 3)
    subfigs = [subfig1, subfig2, subfig3, subfig4, subfig5, subfig6]
    
    unit = "mmol C $m^{-3}$"
    colorbar = 'viridis'
    for idx,subf in enumerate(subfigs):
        if idx > 2:
            unit = ' '
            colorbar = 'jet'
        
        plot_help(subf,C[idx],names[idx],vm[idx], unit, colorbar)

    plt.savefig(plot_dir + 'Sfc_conc_plots/6_pannel_sfc_conc_OMF_MAY.png',dpi = 300,bbox_inches="tight")
#     fig.tight_layout()

    plt.show()


def plot_3_pannel(C, names, vm):
    fig = plt.figure(constrained_layout=True, figsize=(10, 4))

    (subfig1, subfig2, subfig3) = fig.subfigures(nrows=1, ncols=3)
    subfigs = [subfig1, subfig2, subfig3]

    unit = "mmol C m$^{-3}$"
    colorbar = 'viridis'
    for idx, subf in enumerate(subfigs):
        if idx > 2:
            unit = ' '
            colorbar = 'jet'

        plot_help(subf, C[idx], names[idx], vm[idx], unit, colorbar)

    plt.savefig(plot_dir + 'Sfc_conc_plots/6_pannel_sfc_conc.png', dpi=300, bbox_inches="tight")
    #     fig.tight_layout()

    plt.show()


if __name__ == '__main__':

    path_ocean = f"../prepare_bc_data/orig_data/"
    # path_omf = (f"/Users/leon/Desktop/Burrows_param/Burrows_Param_python/Burrows_param_FESON-RECOM_levante/Burrows_param_FESON-RECOM/")
    try:
        os.mkdir('plots')
    except OSError:
        pass

    try:
        os.mkdir('plots/Sfc_conc_plots')
    except OSError:
        pass

    plot_dir = './plots/'

    #C_ice_msk = read_files_data(path_ocean + "mask_a_ice*")['VAR']

    C_pcho = read_files_data(path_ocean+'PCHO_var*')['PCHO']
    C_dcaa = read_files_data(path_ocean+'DAA_var*')['DAA']
    C_lip = read_files_data(path_ocean + "Lipids_var*")['LIPIDS']
    C_conc_tot = C_pcho+C_lip+C_dcaa

    months = np.arange(1,13)
    var = [C_conc_tot, C_pcho, C_dcaa, C_lip]
    years_set = [1989,2020]

    variable = get_monthly_mean(var, months, years_set)
    C_conc_tot_mo = variable[0]
    C_pcho_mo = variable[1]
    C_dcaa_mo = variable[2]
    C_lip_mo = variable[3]


    plot_3_pannel([C_pcho_mo.mean(dim='time'),C_dcaa_mo.mean(dim='time'),C_lip_mo.mean(dim='time')],
                 [['PCHO$_{sw}$', r'$\bf{(a)}$'],['DCAA$_{sw}$', r'$\bf{(b)}$'],['PL$_{sw}$', r'$\bf{(c)}$']],
                  [8,2.5,0.4])

    # plot_6_pannel([C_pcho_mo.mean(dim='time'), C_dcaa_mo.mean(dim='time'), C_lip_mo.mean(dim='time'),
    #                C_pcho_mo.mean(dim='time'), C_dcaa_mo.mean(dim='time'), C_lip_mo.mean(dim='time')],
    #               [['PCHO$_{sw}$', r'$\bf{(a)}$'], ['DCAA$_{sw}$', r'$\bf{(b)}$'], ['PL$_{sw}$', r'$\bf{(c)}$'],
    #                ['PCHO$_{aer}$ OMF', r'$\bf{(d)}$'], ['DCAA$_{aer}$ OMF', r'$\bf{(e)}$'],
    #                ['PL$_{aer}$ OMF', r'$\bf{(f)}$']],
    #               [8, 2.5, 0.4, 0.006, 0.028, 0.35])


