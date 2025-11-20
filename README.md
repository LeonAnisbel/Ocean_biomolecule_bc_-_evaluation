# Compute biomolecule ocean concentration and model evaluation
> This project computes the ocean carbon concentration of marine biomolecules from phytoplankton exudation based on FESOM-REcoM model tracers.
> 
> This data serve as bottom boundary conditions for the [ECHAM6.3-HAMM2.3 model with marine organic tracers](https://zenodo.org/records/14193491) as described by [Leon-Marcos et al. (2025)](https://doi.org/10.5194/gmd-18-4183-2025). 
> 
> Adapts the data to use as bottom boundary conditions for the ECHAM-HAM model simulations.
> 
> Performs the interpolation of simulated biomolecules to the locations of the available in-situ water samples of analogous groups. See more information in [Leon-Marcos et al. (2025)](https://doi.org/10.5194/gmd-18-4183-2025).
> 
> The biogeochemical data is publicly available on [Zenodo](https://doi.org/10.5281/zenodo.15172565) under FESOM-REcoM_tracers_&_biomolecule.zip.\
> The biogeochemistry model data were previously interpolated from the so-called farc mesh to a horizontal regular grid (0.25 ° x0.25 °) and, additionally, a volume-weighted mean was calculated over the upper 30 m of the water column. Sea ice and sst refer to the surface level only.
> 
> Biomolecule names: dissolved carboxylic acidic containing polysaccharides (PCHO), dissolved combined amino acids (DCAA), and polar lipids (PL)
> 

<br/>


> ### Scripts under prepare_bc_data
> 1. run *[Biomolecule_calculation.ipynb](prepare_bc_data/Biomolecule_calculation.ipynb)* to compute carbon ocean concentration of marine biomolecules. It also adds more explanatory attributes to the sst and sic data. This creates new netcdf files stored in *[orig_data](prepare_bc_data/orig_data)* folder.
>  
> 
> 2. run *[echam_grid_interp.py](prepare_bc_data/echam_grid_interp.py)* to interpolate the regular grid to the ECHAM-HAM grid so that it servers as bottom boundary condition for the aerosol model simulations.
> 
> 
> 3. execute then the bash script *[apply_ice_mask.sh](prepare_bc_data/apply_ice_mask.sh)* to create the ice mask criteria used in the ECHAM-HAM sea salt emission subroutine during the model runs.
> 
> 
> 4. execute one last nan correction bash script *[set_nan_to_zeros_biomolecules.sh](prepare_bc_data/set_nan_to_zeros_biomolecules.sh)*. It will replace nan values by null for all biomolecule groups.
>
> Note: Update the directory paths before running the scripts. 
> 
> The data is ready for its use in ECHAM-HAM model simulations !
>
> Find [here](https://zenodo.org/records/14203456) simulation experiment configuration files to perform the simulations in Levante HPC system.
> 
> * Use *[apply_mask.sh](prepare_bc_data/apply_mask.sh)* to create the sea ice mask used to compute OMF and biomolecules average values in sea ice free regions (SIC<10%). However, this is not necessary or used in the creation of the boundary conditions for ECHAM-HAM model.

<br/>


> ### Plot global multiannual monthly averaged biomolecule concentration
> 1. Set up the conda environment with *conda activate environment.yml*
> 
> 
> 2. run *[Macromolecules_fesom_recon_maps.py](biomolecules_map_plot/Macromolecules_fesom_recon_maps.py)* to create a 3-panel figure with the multiannual monthly averaged carbon concentration of each biomolecule.
> 

<br/>


> ### Evaluation of biomolecule ocean carbon concentration
> 1. run *[Biomolecules_evaluation_fesom_recon.ipynb](biom_evaluation/Biomolecules_evaluation_fesom_recon.ipynb)* to perform the interpolation of modelled biomolecules to the locations where seawater samples where collected.
. This will create the file *[model_seawater.pkl](biom_evaluation/pd_files/model_seawater.pkl)* with the observations and model interpolated data of ocean surface carbon concentration of biomolecules.  
> 
> 
> 2. run *[Macromolecules_fesom_recon_daily_monthly.ipynb](biom_evaluation/Macromolecules_fesom_recon_daily_monthly.ipynb)* to create the box plot with seawater samples and interpolated biomolecule ocean concentration for all available locations (see also [Leon-Marcos et al. (2025)](https://doi.org/10.5194/gmd-18-4183-2025).). 
> 
> 
> 3. run *[Ocean_biom_box_map_plot_thesis.py](biom_evaluation/Ocean_biom_box_map_plot_thesis.py)* to create a similar plot as in point 2 but with an additional panel showing the station locations and acronyms in a map.
> 
