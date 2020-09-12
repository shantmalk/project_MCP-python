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
import matplotlib.pyplot as plt
from pandas.plotting import table as pd_table
import numpy as np
import pandas as pd
import six

# For ROC
from itertools import cycle
from sklearn.metrics import roc_curve, auc
from matplotlib import cm

# For survival curve
from lifelines import KaplanMeierFitter
from lifelines import NelsonAalenFitter
from lifelines import CoxPHFitter
from lifelines.statistics import logrank_test

# TABLES
def table_basic(pd_data, fpath, row_colors=['#f1f1f2', 'w'], **kwargs):
    '''
    

    Parameters
    ----------
    pd_data : TYPE
        DESCRIPTION.
    args : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    
    
    # SETUP AXIS:
    pd_data = pd_data.round(2) 
    pd_data = table_merge_mean_std(pd_data)
    ax = render_mpl_table(pd_data, header_columns=0, col_width=3.0, row_colors=row_colors)
    plt.savefig(fpath)

def table_pvalues(pd_data_dict, fpath, row_colors=['#f1f1f2', 'w'], **kwargs):
    '''
    

    Parameters
    ----------
    pd_data : TYPE
        DESCRIPTION.
    args : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    # COMBINE PD_DATA_DICT INTO ONE DATAFRAME
    pd_data = _combine_anova_dict(pd_data_dict)
    
    # SETUP AXIS:
    pd_data = pd_data.round(2) 
    ax = render_mpl_table(pd_data, header_columns=0, col_width=3.0, row_colors=row_colors)
    plt.savefig(fpath)

def _combine_anova_dict(pd_data_dict):
    '''
    Combines inputted dictionary into one Pandas dataframe for cleaner output.  Inputted dictionary keys are the group labels and values will be ANOVA Pandas results.

    Parameters
    ----------
    pd_data_dict : DICTIONARY[GROUP_LBL(STR) : ANOVA_RESULT(PD)]
        DESCRIPTION.

    Returns
    -------
    pd_data_comb : TYPE
        DESCRIPTION.

    '''
    groups = [ ]
    p_values = [ ]
    [(groups.append(grp_lbl), p_values.append(anova_result['PR(>F)'][0])) for (grp_lbl, anova_result) in pd_data_dict.items()]
    pd_data_comb = pd.DataFrame(list(zip(groups, p_values)), columns=['group', 'p-value'])
    return pd_data_comb

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    '''
    
    Ripped from the internet https://stackoverflow.com/questions/19726663/how-to-save-the-pandas-dataframe-series-data-as-a-figure
    
    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    col_width : TYPE, optional
        DESCRIPTION. The default is 3.0.
    row_height : TYPE, optional
        DESCRIPTION. The default is 0.625.
    font_size : TYPE, optional
        DESCRIPTION. The default is 14.
    header_color : TYPE, optional
        DESCRIPTION. The default is '#40466e'.
    row_colors : TYPE, optional
        DESCRIPTION. The default is ['#f1f1f2', 'w'].
    edge_color : TYPE, optional
        DESCRIPTION. The default is 'w'.
    bbox : TYPE, optional
        DESCRIPTION. The default is [0, 0, 1, 1].
    header_columns : TYPE, optional
        DESCRIPTION. The default is 0.
    ax : TYPE, optional
        DESCRIPTION. The default is None.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    ax : TYPE
        DESCRIPTION.

    '''
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax

def table_merge_mean_std(pd_data):
    '''
    Merges numerical columnes for "_mean" and "_std" with a "±" sign 

    Parameters
    ----------
    pd_data : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    pd_data_merged = pd_data
    cols = list(filter(lambda x: (x.find('_std') > -1 or x.find('_mean') > -1), list(pd_data_merged.columns)))
    cols_cleaned = list(set(x.replace('_std','').replace('_mean','') for x in cols))
    cols_cleaned.sort()
    for ii in range(len(cols_cleaned)):
        col_lbl_mean = cols_cleaned[ii] + '_mean'
        col_lbl_std = cols_cleaned[ii] + '_std'
        pd_data_merged = pd_data_merged.drop(columns=[col_lbl_mean, col_lbl_std])
        col_mean = pd_data[col_lbl_mean].apply(str)
        col_std = pd_data[col_lbl_std].apply(str)
        pd_data_merged[cols_cleaned[ii]] = col_mean + ' ± ' + col_std
    
    return pd_data_merged


# GRAPHS

def roc_plot(pd_data, outcome_var, predictor_vars):
    '''
    

    Parameters
    ----------
    pd_data : TYPE
        DESCRIPTION.
    outcome_var : TYPE
        DESCRIPTION.
    predictor_vars : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    # CALCULATE ROC PLOTS
    fpr = dict()
    tpr = dict()
    thresh = dict()
    roc_auc = dict()
    for i in range(len(predictor_vars)):
        fpr[i], tpr[i], thresh[i] = roc_curve(pd_data[outcome_var], pd_data[predictor_vars[i]])
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    # COMBINE DICTIONARIES INTO PD ARRAYS:
    roc_tbls = dict()
    for p_var in predictor_vars:
        roc_tbls[p_var] = pd.DataFrame()
        roc_tbls[p_var]['fpr'], roc_tbls[p_var]['tpr'], roc_tbls[p_var]['thresh'] = roc_curve(pd_data[outcome_var], pd_data[p_var])
        roc_tbls[p_var]['auc'] = auc(roc_tbls[p_var]['fpr'], roc_tbls[p_var]['tpr'])
        roc_tbls[p_var]['predictor_var'] = p_var
    
    # VISUALIZE
    plt.figure()
    lw = 2
        
    viridis = cm.get_cmap('Paired', len(predictor_vars))
    colors = viridis(range(len(predictor_vars)))
    for p_var, color in zip(predictor_vars, colors):
        plt.plot(roc_tbls[p_var]['fpr'], roc_tbls[p_var]['tpr'], color=color,
                 lw=lw, label='{PRED_VAR} (area = {AUC:0.2f})'.format(PRED_VAR=p_var, AUC=roc_tbls[p_var]['auc'][0]))
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('1 - Specificity')
    plt.ylabel('Sensitivity')
    plt.legend(loc="lower right")
    
    # COMBINE ROC_TBLS INTO ONE ARRAY
    roc_pd = pd.DataFrame()
    for p_var in predictor_vars:
        roc_pd = pd.concat([roc_pd, roc_tbls[p_var]])
    return plt, roc_pd

def survival_curve(pd_qsel_data, outcome_var, outcome_time, predictor_class, labels):
    '''
    

    Parameters
    ----------
    pd_qsel_data : TYPE
        DESCRIPTION.
    outcome_var : TYPE
        DESCRIPTION.
    outcome_time : TYPE
        DESCRIPTION.
    predictor_class : TYPE
        DESCRIPTION.

    Returns
    -------
    plt : TYPE
        DESCRIPTION.

    '''
    
    grp1_filt = pd_qsel_data[predictor_class] == 1
    grp1 = pd_qsel_data[grp1_filt]
    
    grp2_filt = pd_qsel_data[predictor_class] == 0
    grp2 = pd_qsel_data[grp2_filt]
    
    
    plt.figure()
    kmf = KaplanMeierFitter()
    
    kmf.fit(grp1[outcome_time], grp1[outcome_var], label=labels[0])
    kmf.plot()
        
    kmf.fit(grp2[outcome_time], grp2[outcome_var], label=labels[1])
    kmf.plot()    
    plt.xlabel('Time (days)')
    plt.ylabel('Percent Survival')
    
    summary_ = logrank_test(grp1[outcome_time], grp2[outcome_time], grp1[outcome_var], grp2[outcome_var], alpha=99)
    print(summary_) 
    
    return plt

def hazard_rates_curve(pd_qsel_data, outcome_var, outcome_time, predictor_class, labels):
    '''
    

    Parameters
    ----------
    pd_qsel_data : TYPE
        DESCRIPTION.
    outcome_var : TYPE
        DESCRIPTION.
    outcome_time : TYPE
        DESCRIPTION.
    predictor_class : TYPE
        DESCRIPTION.

    Returns
    -------
    plt : TYPE
        DESCRIPTION.

    '''
    
    grp1_filt = pd_qsel_data[predictor_class] == 1
    grp1 = pd_qsel_data[grp1_filt]
    
    grp2_filt = pd_qsel_data[predictor_class] == 0
    grp2 = pd_qsel_data[grp2_filt]
    
    plt.figure()
    naf = NelsonAalenFitter()
    
    naf.fit(grp1[outcome_time], grp1[outcome_var], label=labels[0])
    naf.plot()
        
    naf.fit(grp2[outcome_time], grp2[outcome_var], label=labels[1])
    naf.plot()    
    plt.xlabel('Time (days)')
    plt.ylabel('Cumulative Hazard')
    return plt

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