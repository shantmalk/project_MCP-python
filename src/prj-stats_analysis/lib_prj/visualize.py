# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:02:00 2020

@author: smDesktop
"""
import os
import shutil
import plotly.express as px
from plotly.offline import plot
import lib_prj


# GRAPHS
def plot_plotly(fig, filename):
    lib_prj.paths.make_directory(lib_prj.paths.PATH_PLOTLY_TEMP)
    plt = plot(fig, filename=lib_prj.paths.PATH_PLOTLY_TEMP + filename)
    return plt

def boxplot_plotly(pd_data, args_plotly, axis_labels):
    '''
    Simple wrapper for boxplots using Plotly.  This ensures uniform formatting across different uses of boxplot.  
    Write the boxplot outside of function.

    Parameters
    ----------
    pd_data : Pandas array
        Pandas array of data.
    args_plotly : dict
        Dictionary of inputs to pass to Plotly when formatting/creating boxplot.  Keys must be arguments of px.box function.
    axis_labels : TYPE
        Dictionary of axis labels.

    Returns
    -------
    fig : Plotly figure
        Plotly boxplot.

    '''
    
    # Add addt parameters to args_plotly
    args_plotly['title'] = '<b>' + args_plotly['title'] + '</b>'
    
    fig = px.box(pd_data, **args_plotly)
    return fig
    
def plotly_clear_fig():
    if os.path.exists(lib_prj.paths.PATH_PLOTLY_TEMP):
        shutil.rmtree(lib_prj.paths.PATH_PLOTLY_TEMP)
        return True
    else:
        return False
            

# TEXT
def print_label(module_name):
    print()
    print('# ------------------------------------------ RUNNING ROUTINE ------------------------------------------ #')
    print('Routine name: ' + module_name)
    print()