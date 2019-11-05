 # -*- coding: utf-8 -*-
"""
Implement drawing core functions.
"""
from matplotlib.colorbar import Colorbar, make_axes

import global_var as glv
import global_const as glc
from modules import tools


def plot_heatmap(ax, cax, df_pivoted, title, cm, dim, vmin=None, vmax=None, cm_bins=20, mode=''):
    """
    Core plotting function. Call the related function in Matplotlib and plot a heatmap.

    Args:
        ax (Axes): Axes of main part of heatmap, mainly defines the location of the main part.
        cax (Axes): Axes of colorbar of heatmap, mainly defines the location of the colorbar.
        df_pivoted (dataframe): The data to be plotted.
        title (str): Title of the plot.
        cm (matplotlib.colormap): colormap for plotting heatmap.
        dim (str): Unit.
        vmin (float): min value, useful for colorscale setting.
        vmax (float): max value, useful for colorscale setting.
        cm_bins (int): The number of bins of colormap.
        mode (str): Export mode: sequentially, annually or monthly.
    Returns:
        Axes: Return the axes object of main part of heatmap.
    """
    if vmin==None:
        if dim=='OnOff' or dim=='Onoff':
            vim = 0
        elif '%' in dim or dim=='percent' or dim=='percentage':
            vmin = 0
        else:
            vmin = df_pivoted.min().min()
    if vmax==None:
        if dim=='OnOff' or dim=='Onoff':
            vmax = 1
        elif '%' in dim or dim=='percent' or dim=='percentage':
            vmax = 100
        else:
            vmax = df_pivoted.max().max()

    # Plotting
    df_pivoted.fillna(vmax + 1)
    im = ax.imshow(df_pivoted, vmin=vmin, vmax=vmax, cmap=tools.discrete_cmap(cm_bins, cm), interpolation='nearest', aspect='auto')
    ax.axis('on')

    # Colorbar
    if cax is None:
        cax, kw = make_axes(ax)
    make_colorbar(cax, im, dim)
    
    # Title
    if mode=='monthly':
        title=tools.convert_number_to_month(title)
    ax.set_title(title)

    # Y-Axis
    yticklabel, ytick = tools.convert_time_to_ticklabel(df_pivoted.index, bins=6)
    ax.set_ylabel('Time')
    ax.set_yticks(ytick)
    ax.set_yticklabels(yticklabel)
    ax.invert_yaxis()

    # X-Axis
    if mode=='monthly':
        xticklabel, xtick = tools.convert_date_to_ticklabel_monthly(df_pivoted.columns)
    else:
        xticklabel, xtick = tools.convert_date_to_ticklabel(df_pivoted.columns, len(df_pivoted.columns))   
    ax.set_xticks(xtick)
    ax.set_xticklabels(xticklabel, rotation='horizontal')

    return ax


def make_colorbar(cax, im, dim):
    """
    Function to plot colorbar.

    Args:
        cax (Axes): Axes of colorbar of heatmap, mainly defines the location of the colorbar.
        im (Image): The mapping relationship between data and color.
        dim (str): Unit.
    Returns:
        Axes: Return the axes object of colorbar of heatmap.
    """
    cax.axis('on')
    if dim=='OnOff' or dim=='Onoff':
        Colorbar(cax, im, ticks=[0, 1])
    elif '%' in dim or dim=='percent' or dim=='percentage':
        Colorbar(cax, im, format='%.0f %%')
    else:
        Colorbar(cax, im, format='%.3g', label='in ' + dim)
    return cax


