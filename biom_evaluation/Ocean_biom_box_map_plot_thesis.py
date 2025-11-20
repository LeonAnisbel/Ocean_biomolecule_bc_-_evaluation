import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from sklearn.metrics import mean_squared_error
from scipy.stats import linregress
import cartopy.crs as ccrs
import codecs

import global_vars


## Statistical indicators
def equat_stat(model, observ):
    """
    Function to compute statistics
    :var model: list of interpolated model values
    :var observ: list of observation values
    :return: list of statistics [rmse, pearsons_coeff, pval_corr, mean_bias, nmb]
    """
    # Root Mean Squared Error
    model, observ = np.array(model), np.array(observ)
    rmse = np.sqrt(mean_squared_error(model, observ))

    # Correlation coefficient (R)
    res_lin_reg = linregress(observ, model)
    pearsons_coeff = res_lin_reg.rvalue
    pval_corr = res_lin_reg.pvalue

    # Mean Bias and Normalised Mean Bias (NMB)
    mean_bias = np.nanmean(np.subtract(model, observ))
    #     nmb = np.mean(bias/observ)
    nmb = np.nansum(np.subtract(model, observ)) / np.nansum(observ)

    # Normalised Mean Standard Deviation (NMSD)
    std_obs = np.std(observ)
    std_mod = np.std(model)
    nmsd = (std_mod - std_obs) / std_obs

    print('No. observations:', len(observ), '\n',
          'RMSE:', rmse, '\n',
          'Pearson:', pearsons_coeff, '\n',
          'pval:', pval_corr, '\n',
          'MB:', mean_bias, '\n',
          'NMB:', nmb, '\n')

    return [rmse, pearsons_coeff, pval_corr, mean_bias, nmb]


def function_plot_two_pannel(ax, location, names):
    """
    Creates map with station locations
    :var ax: matplotlib axes object
    :var location: list of locations
    :var names: list of names
    :return: matplotlib object
    """

    ax.coastlines(resolution='110m', color='gray')
    ax.set_extent([-100, 40, -90, 90])

    ind = 0
    for loc, n in zip(location, names):
        if len(loc) == 2:
            ax.scatter(x=loc[1], y=loc[0],
                       color='gray',
                       label=n,
                       marker='o',
                       transform=ccrs.PlateCarree())

            plt.text(loc[1] + 3, loc[0] - 3, n,
                     horizontalalignment='right',
                     transform=ccrs.Geodetic(),
                     bbox={'facecolor': 'lightgray',
                           'boxstyle': 'round',
                           'pad': 0.2,
                           'alpha': 0.5})
        else:
            ind = 1
            for l in loc:
                ax.scatter(x=l[1], y=l[0],
                           color='k',
                           label=n,
                           marker='o',
                           alpha=1,
                           transform=ccrs.PlateCarree())

            plt.text(l[1] + 10, l[0] - 5, n,
                     horizontalalignment='right',
                     transform=ccrs.Geodetic(),
                     bbox={'facecolor': 'lightgray',
                           'boxstyle': 'round',
                           'pad': 0.2,
                           'alpha': 0.8})

    gl = ax.gridlines(draw_labels=True,
                      x_inline=False,
                      y_inline=False)
    gl.xlocator = ticker.FixedLocator([-60,-30, 0, 30])
    gl.top_labels = False
    gl.right_labels = False
    return ax


# %%
def plot_text(dict_macrom, ax, c_na, ID, l0, l1, h1, mol_name, stat_name, loc_factor):
    """
    Creates the box plot figure with all biomolecules groups separated by dashed lines
    :var dict_macrom: dictionary with model and observation values
    :var ax: matplotlib axes object
    :var c_na: biomolecule name
    :var ID:
    :var l0: location of biomolecule name in plot
    :var l1: position (x) of statistics in plot
    :var h1:  position (y) of statistics in plot
    :var mol_name: biomolecule full name
    :var stat_name: station labels
    :var loc_factor: factor to position the labels for each panel
    :return: None
    """
    mod_data = dict_macrom[dict_macrom[''] == 'Model']
    obs_data = dict_macrom[dict_macrom[''] == 'Observation']
    stat_all = equat_stat(mod_data[c_na], obs_data[c_na])

    box2 = f'NMB={np.round(stat_all[-1], 2)} '
    print('PLOT text', box2, len(obs_data))
    box1 = mol_name
    ax.text(l0,
            50,
            box1,
            fontsize='14',
            weight='bold',
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    ax.text(l1,
            h1,
            box2,
            fontsize='12')

    for idx, s in enumerate(stat_name):
        n = str(len(obs_data[obs_data['Measurements'] == s]))

        ax.text(idx + loc_factor,
                0.35,
                f'n= {n}',
                fontsize='12')


def box_plot_vert(ax, dict_df, ID, lim):
    """
    Calls functions to create and customize box plot with all biomolecules groups separated by dashed lines
    :var ax: matplotlib axes object
    :var dict_df: pandas dataframe with model and observation values
    :var ID: list of species ids
    :var lim: y-axis limit
    :return: None
    """

    c_na = 'Concentration in the ocean ($mmol\ C\ m^{-3}$)'
    states_palette = sns.color_palette("YlGnBu", n_colors=2)
    bx = sns.boxplot(ax=ax,
                     data=dict_df, x="Measurements",
                     y=c_na, hue="", palette=states_palette,
                     flierprops={
                         'marker': 'd',  # Use diamond marker
                         'markersize': 5,  # Set marker size
                         'markerfacecolor': '#404040'},
                     width=.7)

    # calculate statistics
    stations = {'pol  DCCHO [µMC]': ['NAO', 'WAP', 'CVAO  ', 'PUR12 ', 'PUR17'],
                'pro  DCAA [µMC]': ['CVAO', 'PUR12', 'SB', 'NWAO', 'SATL', 'WMED'],
                'lip  PG': ['CVAO ', 'AS']}

    print('Stat for individual stations and organic groups')
    for molec in list(stations.keys()):
        dict_molec = dict_df[dict_df['Macromolecules'] == molec]
        for sta in stations[molec]:
            dict_stat = dict_molec[dict_molec['Measurements'] == sta]
            mod_data = dict_stat[dict_stat[''] == 'Model']
            obs_data = dict_stat[dict_stat[''] == 'Observation']


    pol_df = dict_df[dict_df['Macromolecules'] == 'pol  DCCHO [µMC]']
    pro_df = dict_df[dict_df['Macromolecules'] == 'pro  DCAA [µMC]']
    lip_df = dict_df[dict_df['Macromolecules'] == 'lip  PG']

    print('Stat for all stations')
    plot_text(pol_df, ax, c_na, ID[0], 0.1, 3, 50,
              'PCHO$_{sw}$|DCCHO$_{sw}$', stations['pol  DCCHO [µMC]'], -0.2)
    plot_text(pro_df, ax, c_na, ID[1], 5, 8, 50,
              'DCAA$_{sw}$|DCAA$_{sw}$', stations['pro  DCAA [µMC]'], 4.8)
    plot_text(lip_df, ax, c_na, ID[2], 11, 10.8, 20,
              'PL$_{sw}$|PG$_{sw}$', stations['lip  PG'], 10.8)

    # Customizing axes
    ax.tick_params(axis='both',
                   labelsize='16')
    ax.yaxis.get_label().set_fontsize(16)
    ax.set_xlabel('',
                  fontsize=16)
    ax.set_ylabel('Concentration in the ocean (mmol C m$^{-3}$)',
                  fontsize=16)
    ax.set_yscale('log')
    ax.grid(linestyle='--',
            linewidth=0.4)
    ax.set_ylim(lim)

    # dotted lines to separate groups
    ax.axvline(4.5,
               color=".3",
               dashes=(2, 2))
    ax.axvline(10.5,
               color=".3",
               dashes=(2, 2))

    ax.legend(loc="lower left",
              fontsize='16')

if __name__ == '__main__':
    data_dir = './pd_files/'
    df_all_groups = pd.read_pickle(f'{data_dir}model_seawater.pkl')
    file_water = "../Observations/SEAWATER_data.csv"

    # Creates plot used in Doctoral Thesis Chapter 5
    # Read observation data to retrieve stations locations of seawater samples
    doc = codecs.open(file_water,
                      'r',
                'UTF-8')  # open for reading with "universal" type set 'rU'
    data_water = pd.read_csv(doc, sep=',')
    WAP = data_water[data_water['Event'] == 'WAP']
    NAO = data_water[data_water['Event'] == 'PASCAL']
    CVAO = data_water[data_water['Event'] == 'CVAO']
    PUR12 = data_water[data_water['Event'] == 'PUR12']
    PUR17 = data_water[data_water['Event'] == 'PUR17']
    PUR = pd.concat([PUR12, PUR17])
    SB = data_water[data_water['Event'] == 'SB']  # Stony Brook Harbor (SB), Marina Kuznetsova* and Cindy Lee (FAA)
    NWAO = data_water[data_water['Event'] == 'NAO']  # Marina Kuznetsova et al. 2004 (FAA North Atlantic Ocean)
    SATL = data_water[data_water[
                          'Event'] == 'SATL']  # stations (STN) in the subtropical Atlantic (SATL), Reinthaler et al. 2008 (FAA)
    WMED = data_water[data_water['Event'] == 'WMED']  # The western Mediterranean (WMED), Reinthaler et al. 2008 (FAA)
    AS98 = data_water[data_water['Event'] == 'AS98']
    BS = data_water[data_water['Event'] == 'BS']
    AS08 = data_water[data_water['Event'] == 'AS08']

    var_list = [NAO, WAP, CVAO, NWAO, WMED, AS08, PUR12, PUR17, SB, SATL]
    loc_list = []
    for loc in var_list:
        l_list = [[loc['Latitude'].values[m], loc['Longitude'].values[m]] for m in range(len(loc['Longitude'].values))]
        loc_list.append(l_list)

    names = ['NAO', 'WAP', 'CVAO',
             '', 'WMED', 'AS',
             '', 'PUR12\nPUR17',
             'NWAO\nSB', 'SATL']

    #### Create figure of box plot (model and observations) and a second panel with map locations
    fig, ax0 = plt.subplots(figsize=(15, 8))
    proj = ccrs.PlateCarree()
    ax1 = fig.add_axes([0.85, 0.33, 0.4, 0.46],
                       projection=proj)
    # plot values
    box_plot_vert(ax0,
                  df_all_groups,
                  ['pol', 'pro', 'lip'],
                  [1e-2, 1e2])

    #plot map locations
    function_plot_two_pannel(ax1,
                             loc_list,
                             names)
    plt.savefig(f'{global_vars.plot_dir}/All_groups_box_map_plot.png',
                dpi=300,
                bbox_inches="tight")
    plt.close()