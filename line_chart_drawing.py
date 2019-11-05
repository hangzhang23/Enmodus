# -*- coding: utf-8 -*-
"""
Implement drawing core functions.
"""
import pandas as pd
from logzero import logger

from modules import tools
import global_var as glv
import global_const as glc


def plot_linechart(ax, database, infobase, start_date, end_date, mode='preview'):
    """
    Core plotting function. Call the related function in Matplotlib and plot a linechart.

    Args:
        figure (figure): figure of linechart for main axes and second axes.
        database (list): plotting-sensor's data are stored in list in format series
        infobase (list): plotting-sensor's title and dim are stored in list in format list.
        start_date (Datetime): The displayed the date range.
        end_date (Datetime): The displayed the date range.
        mode (str): preview, sequentially, annually or monthly
    Returns:
        Axes, Axes: Return the axes object of line chart.
    """
    ax2 = ax.twinx()

    if len(database)<glc.NUM_OF_FILENAME_DROPDOWN:
        database += [None for j in range(glc.NUM_OF_FILENAME_DROPDOWN - len(database))]

    if len(infobase)<glc.NUM_OF_FILENAME_DROPDOWN:
        infobase += [None for j in range(glc.NUM_OF_FILENAME_DROPDOWN - len(infobase))]

    # colorlist = ['red', 'green', 'blue', 'chocolate', 'gold']
    units_lst = tools.get_units_lst(infobase)
    curvelist = []
    labellist = []

    if len(units_lst) == 1:
        ax.set_ylabel(units_lst[0], fontsize=12)
        ax.axis('on')
        ax2.axis('off')
    elif len(units_lst) == 2:
        ax.set_ylabel(units_lst[0], fontsize=12)
        ax2.set_ylabel(units_lst[1], fontsize=12)
        ax.axis('on')
        ax2.axis('on')

    for i in range(glc.NUM_OF_FILENAME_DROPDOWN):
        if database[i] is not None and infobase[i] is not None :
            title = infobase[i]['title']
            dim = infobase[i]['dim']
            color = tools.convert_rgb2mcolor(infobase[i]['color'])
            alpha = infobase[i]['alpha'] /100
            style = infobase[i]['style']
            width = infobase[i]['width'] / 2
            if dim == units_lst[0]:
                curvelist += ax.plot(database[i].index, database[i], c=color, alpha=alpha, linestyle=style, linewidth=width)
            elif dim == units_lst[1]:
                curvelist += ax2.plot(database[i].index, database[i], c=color, alpha=alpha, linestyle=style, linewidth=width)
            labellist.append(infobase[i]['title'])
    
    if mode=='preview':
        ax.legend(curvelist, labellist, loc=3, prop={'size': 10}, bbox_to_anchor=(0.0, 1.0), ncol=5)
    elif mode=='annually' or mode=='sequentially':
        ax.set_title(title)
    elif mode=='monthly':
        ax.set_title(tools.convert_number_to_month(title))
        xticklabel, xtick = tools.convert_date_to_ticklabel_monthly(database[0].index)
        ax.set_xticks(xtick)
        ax.set_xticklabels(xticklabel, rotation='horizontal')
    else:
        raise NotImplementedError
    print(end_date, type(end_date))
    ax.set_xlim(start_date, end_date+pd.Timedelta('23 hour 59 min 59 s'))
    return ax, ax2
