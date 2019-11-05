# -*- coding: utf-8 -*-
"""
Core drawing function
"""
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from modules import tools
import global_var as glv
import global_const as glc


def plot_area_chart(ax, df_data, title, dim, mode=''):
    """
    Core drawing function using matplotlib.

    Args:
        ax (Axes): drawing panel
        df_data (DataFrame): The data to draw.
        title (str): title of the chart
        dim (str): unit of the data
        mode(str): Export mode: sequentially, annually or monthly.
    """
    x = mdates.date2num(pd.date_range(start='2019-01-01 00:00:00', end='2019-01-01 23:59:59', freq='15T').to_pydatetime())

    ax.plot(x, df_data['Max'], color='black', linestyle='--', label='Max')
    ax.plot(x, df_data['Median'], color='black', label='Median')
    ax.plot(x, df_data['Min'], color='black', linestyle='-.', label='Min')
    ax.fill_between(x, df_data['95% Quartil'], df_data['5% Quartil'], facecolor='gray', alpha=0.5, label='Q5 - Q95')
    ax.fill_between(x, df_data['75% Quartil'], df_data['25% Quartil'], facecolor='brown', alpha=0.5, label='Q25 - Q75')
    # ax.set_title(title)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.99, box.height])
    ax.legend(loc=2, bbox_to_anchor=(1, 1), ncol=1)
    ax.set_ylabel(dim)
    ax.set_xlim(mdates.date2num(pd.to_datetime('2019-01-01 00:00:00').to_pydatetime()),
                mdates.date2num(pd.to_datetime('2019-01-01 23:45:00').to_pydatetime()))
    
    major_locator = mdates.MinuteLocator(byminute=[0])
    minor_locator = mdates.MinuteLocator(byminute=[0, 15, 30, 45])
    time_format = mdates.DateFormatter('%H:%M')

    ax.xaxis.set_major_locator(major_locator)
    ax.xaxis.set_minor_locator(minor_locator)
    ax.xaxis.set_major_formatter(time_format)

    if mode == 'monthly':
        title = tools.convert_number_to_month(title)
        ax.tick_params(labelsize=5)
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)
    ax.set_title(title)

    return ax
