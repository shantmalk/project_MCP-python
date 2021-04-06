# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:02:00 2020

@author: smDesktop
"""
import os
import shutil
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
import lib_prj
import matplotlib.pyplot as plt
from pandas.plotting import table as pd_table
import numpy as np
import pandas as pd
import six

import seaborn as sns

# For ROC
from itertools import cycle
from sklearn.metrics import roc_curve, auc
from matplotlib import cm
from functools import reduce

# For survival curve
from lifelines import KaplanMeierFitter
from lifelines import NelsonAalenFitter
from lifelines import CoxPHFitter
from lifelines.statistics import logrank_test

# TABLES

def table_mmar_confirm(df, index, ax=None, lbls=[]):
    
    def _tb_helper(_df, _index, _afunc, _col_lbl):
        df_out = pd.pivot_table(_df, index=_index, aggfunc=_afunc)
        df_out.columns = [x + _col_lbl for x in df_out.columns]
        df_out.reset_index(inplace=True)
        return df_out
    def _tb_add_pval(_df, _df_pval):
        _df['pvalue'].loc[_df['plaque_type'] == _df_pval['group'][0]] = ['%0.2f' % _df_pval['p-value'][0], '']
        return _df
    
    df_totals = _tb_helper(df, index, len, '_n').rename(columns={'confirm_idc_n' : 'n'})
    df_mean = _tb_helper(df, index, 'mean', '_mean')
    df_std = _tb_helper(df, index, np.std, '_std')
    
    df_agg_list = [df_totals, df_mean, df_std]
        # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    df_agg_pivot = reduce(lambda left,right: pd.merge(left, right, on=index,how='outer',), df_agg_list) 
    
    incld_cols = index.copy()
    incld_cols.extend(['n', 'mmar_mean', 'mmar_std'])
    df_agg_pivot = df_agg_pivot[incld_cols]
    
    df_agg_pivot['pvalue'] = ''
    
    # TODO: GENERALIZE THIS TO BE BASED ON ALL UNIQUE OCCURRENCES OF PLAQUE_TYPE
    # df_pval_all = table_pval_confirm(df, index[1], 'mmar', 'plaque_type', 'all')
    df_pval_hrp = table_pval_confirm(df, index[1], 'mmar', 'plaque_type', 'hrp')
    df_pval_lrp = table_pval_confirm(df, index[1], 'mmar', 'plaque_type', 'lrp')
    
    
    # df_agg_pivot = _tb_add_pval(df_agg_pivot, df_pval_all)
    df_agg_pivot = _tb_add_pval(df_agg_pivot, df_pval_hrp)
    df_agg_pivot = _tb_add_pval(df_agg_pivot, df_pval_lrp)

    return table_basic(df_agg_pivot.sort_values(by=index), '', ['w', '#f1f1f2', '#f1f1f2', 'w',], col_labels = lbls, ax=ax)

def table_scct_confirm(df, index, ax=None, lbls=[]):
    
    def _tb_helper(_df, _index, _afunc, _col_lbl):
        df_out = pd.pivot_table(_df, index=_index, aggfunc=_afunc)
        df_out.columns = [x + _col_lbl for x in df_out.columns]
        df_out.reset_index(inplace=True)
        return df_out
    
    df_totals = _tb_helper(df, index, len, '_n').rename(columns={'confirm_idc_n' : 'n', 'mmar_n' : 'n'})
    df_mean = _tb_helper(df, index, 'mean', '_mean')
    df_std = _tb_helper(df, index, np.std, '_std')
    
    df_agg_list = [df_totals, df_mean, df_std]
        # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    df_agg_pivot = reduce(lambda left, right: pd.merge(left, right, on=index,how='outer',), df_agg_list) 
    
    incld_cols = index.copy()
    incld_cols.extend(['n', 'mmar_mean', 'mmar_std'])
    df_agg_pivot = df_agg_pivot[incld_cols]
    df_agg_pivot['pvalue'] = ''
    
    return table_basic(df_agg_pivot.sort_values(by='mmar_mean', ascending=False), '', ['w', '#f1f1f2', ], col_labels = lbls, ax=ax, keep_pvals=False)

def table_pval_confirm(df, col_indpendent, col_var, col_lbl, col_lbl_cond):
    col_independent_inv = 'inv_'
    df[col_independent_inv] = ~(df[col_indpendent].astype('bool'))
    # Add P-values
    return _combine_anova_dict({col_lbl_cond : lib_prj.process.stats_anova(df.loc[df[col_lbl] == col_lbl_cond], [col_independent_inv, col_indpendent], col_var)})

def table_lesion_confirm(df, index, ax=None, lbls={}):
    
    def _tb_helper(_df, _index, _afunc, _col_lbl):
        df_out = pd.pivot_table(_df, index=_index, aggfunc=_afunc)
        df_out.columns = [x + _col_lbl for x in df_out.columns]
        df_out.reset_index(inplace=True)
        return df_out
    
    df_totals = _tb_helper(df, index, len, '_n').rename(columns={'confirm_idc_n' : 'n'})
    df_count = _tb_helper(df, index, 'sum', '_mean')
    df_std = _tb_helper(df, index, np.std, '_std')
    
    df_agg_list = [df_totals, df_count, df_std]
        # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    df_agg_pivot = reduce(lambda left,right: pd.merge(left, right, on=index,how='outer',), df_agg_list) 
    
    incld_cols = index.copy()
    incld_cols.extend(['n', 'mmar_mean'])
    df_agg_pivot = df_agg_pivot[incld_cols].rename(columns={'mmar_mean' : 'n_lesions'})
    table_basic(df_agg_pivot.sort_values(by=index), '', ['w', '#f1f1f2', '#f1f1f2', 'w',], col_labels = lbls, ax=ax)

def table_basic(pd_data, fpath='tmp.png', row_colors=['#f1f1f2', 'w'], col_labels = [ ], ax=None, keep_pvals=True, **kwargs):
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
    if not keep_pvals:
        pd_data = pd_data.drop(columns=['pvalue'])
    if len(col_labels):
        pd_data.columns = col_labels
    ax = render_mpl_table(pd_data, header_columns=0, col_width=3.0, row_colors=row_colors, ax=ax)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.savefig(fpath)
    
    return pd_data

def table_pvalues(pd_data_dict, fpath, row_colors=['#f1f1f2', 'w'], ax=None, **kwargs):
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
    ax = render_mpl_table(pd_data, header_columns=0, col_width=3.0, row_colors=row_colors, ax=ax)
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
    pd_data_merged = pd_data_merged.drop(columns=['pvalue']) 
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
    pd_data_merged['pvalue'] = pd_data['pvalue']
    return pd_data_merged


# GRAPHS
def get_line_from_axis(axis):
    for item in axis.get_children():
        return item
        # if isinstance(item, plt.lines.Line2D):
            # return item


def kdeplot(args):
    sns.set_style("darkgrid")
    
    default_params = {
        # 'norm' : True,
        }
    # cur_ax = sns.histplot(**{**args, **default_params})
    
    default_params = {
        'cut' : 0,
        'fill' : True,
        'alpha' : .5,
        'linewidth' : 2,
        }
    cur_ax = sns.kdeplot(**{**args, **default_params})
    # cur_ax.set_xlim(left=0)
    # start, end = cur_ax.get_xlim()
    # cur_ax.xaxis.set_ticks(np.arange(start, end, 1))
    return cur_ax

def histplot(args):
    default_params = {
        'dodge' : True,
        }
    
    cur_ax = sns.countplot(**{**args, **default_params})
    
    # default_params = {
    #     'cut' : 0,
    #     'fill' : True,
    #     'alpha' : .5,
    #     'linewidth' : 0,
    #     }
    # cur_ax = sns.kdeplot(**{**args, **default_params})
    # cur_ax.set_xlim(left=0)
    # start, end = cur_ax.get_xlim()
    # cur_ax.xaxis.set_ticks(np.arange(start, end, 1))
    return cur_ax

def swarmplot(args):
    # args['data'][args['x']] = [x.upper() for x in args['data'][args['x']]]
    default_params = {
            'whis' : np.inf,
            'linewidth' : 5,
            # 'height' : 4,
            # 'aspect' : .7,
            }
    cur_ax = sns.boxplot(**{**args, **default_params})
    # cur_ax.get_legend().remove()
    
    default_params = {
            'dodge' : True,
            'edgecolor' : 'white',
            'linewidth' : .25,
            'alpha' : .25,
            's' : 5, # CHANGE TO 10
            # 'label' : {'1' : 'MI', '0' : 'No MI'},
            }
    cur_ax = sns.stripplot(**{**args, **default_params})
    try:
        # pass
        cur_ax.get_legend().remove()
    except:
        pass
    
    return cur_ax

def linear_regression_plot(args):
    
    default_params = {
            'ci' : None,
            'fit_reg' : False,
            }
    cur_ax = sns.regplot(**{**args, **default_params})
    cur_ax.set(xlim=(-0.1, args['data'][args['x']].max() + args['data'][args['x']].max() * .05))
    cur_ax.set(ylim=(-0.1, args['data'][args['y']].max() + args['data'][args['y']].max() * .05))

    return cur_ax
    
def kmsurvival_mmar_confirm(df:'pd.DataFrame', outcome_event:str, outcome_time:str, mmar_col:str, ax=None, q_cutoff=.85, lbl='{CUTOFF:0.2f}'):
    
    if not ax:
        fig = plt.figure()
        ax = fig.add_axes()
        
    cutoff_thresh = df[mmar_col].quantile([q_cutoff])[q_cutoff]
    # cutoff_thresh = 10
    df_dummy = pd.DataFrame()
    df_dummy['outcome_event'] = df[outcome_event]
    df_dummy['outcome_time'] = df[outcome_time]
    df_dummy['mmar'] = df[mmar_col] > cutoff_thresh
    
    kmf = KaplanMeierFitter()
    i1 = df_dummy['mmar'] == True
    i2 = df_dummy['mmar'] == False
    kmf.fit(durations = df_dummy['outcome_time'][i1], event_observed = df_dummy['outcome_event'][i1], label = lbl.format(CUTOFF=cutoff_thresh))
    # kmf.plot_survival_function(show_censors=True, censor_styles={'ms' : 6, 'marker' : 's', }, ax=ax)
    kmf.plot(ax=ax, ci_show=False)
    kmf.fit(df_dummy['outcome_time'][i2], df_dummy['outcome_event'][i2], label = lbl.replace(' > ',' < ').format(CUTOFF=cutoff_thresh))
    # kmf.plot_survival_function(show_censors=True, censor_styles={'ms' : 6, 'marker' : 's', }, ax=ax)
    kmf.plot(ax=ax, ci_show=False)

def rr_boxplot(df):
    
    n = 1
    plt.figure()
    plt.vlines(1, 0, len(df))
    for idx, row in df.iterrows():
        plt.errorbar(row['rr'], idx+n, xerr=row['std'])
        plt.scatter(row['rr'], idx+n)
    lbls = [' ']
    lbls.extend(list(df['lbl']))
    plt.yticks(np.arange(len(df)+1, step=n), lbls)
    return plt


# def param_boxplot(metric_var, agg_col, fig=plt.figure()):
#     '''


#     Parameters
#     ----------
#     metric_var : STRING
#         "Metric" variable.
#     agg_col : STRING
#         "Aggregate" column name.
#     fig : plt.Figure(), optional
#         If no figure specified, create one. The default is plt.figure().

#     Returns
#     -------
#     None.

#     '''

#     pd_dict = lib_prj.process.mk_pd_dict(pd_data, metric_var, {'mmar_max' : 'max',
#                                                                'mmar_min' : 'min',
#                                                                })    
    
    
#     agg_dict = lib_prj.process.agg_dataframe_dict(agg_col, pd_dict)
#     df_dict = lib_prj.process.mk_pd_dict(df_mcp_comb, metric_var, {'mmar_max' : 'max', 'mmar_min' : 'min'})
#     df_mmar = lib_prj.process.agg_dataframe_dict(mmar_var_col, df_dict)

#     plt.figure()
#     sns.boxplot(x='mass_mcp_g', y=mmar_var_col, data=df_mmar)

def roc_plot(pd_data, outcome_var, predictor_dict, cur_ax=False):
    '''
    

    Parameters
    ----------
    pd_data : TYPE
        DESCRIPTION.
    outcome_var : TYPE
        DESCRIPTION.
    predictor_dict : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    predictor_vars = list(predictor_dict.keys())
    
    # CALCULATE ROC PLOTS
    fpr = dict()
    tpr = dict()
    thresh = dict()
    roc_auc = dict()
    
    filt_pd_data = pd_data
    #filt_pd_data[outcome_var][pd.isnull(filt_pd_data[outcome_var])]
    for i in range(len(predictor_vars)):
        # filt_pd_data = pd_data[~(pd_data[predictor_vars[i]] == 0)]
        fpr[i], tpr[i], thresh[i] = roc_curve(filt_pd_data[outcome_var], filt_pd_data[predictor_vars[i]]) # REMOVE == '1' IF NECESSARY FOR OTHER PROCESSING...
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    # COMBINE DICTIONARIES INTO PD ARRAYS:
    roc_tbls = dict()
    for p_var in predictor_vars:
        roc_tbls[p_var] = pd.DataFrame()
        roc_tbls[p_var]['fpr'], roc_tbls[p_var]['tpr'], roc_tbls[p_var]['thresh'] = roc_curve(filt_pd_data[outcome_var], filt_pd_data[p_var])
        roc_tbls[p_var]['auc'] = auc(roc_tbls[p_var]['fpr'], roc_tbls[p_var]['tpr'])
        roc_tbls[p_var]['predictor_var'] = p_var
    
    # VISUALIZE
    if not cur_ax:
        fig, cur_ax = plt.figure()
    lw = 2
        
    viridis = cm.get_cmap('Paired', len(predictor_vars))
    colors = viridis(range(len(predictor_vars)))
    for p_var, color in zip(predictor_vars, colors):
        cur_ax.plot(roc_tbls[p_var]['fpr'], roc_tbls[p_var]['tpr'], color=color,
                 lw=lw, label='{PRED_VAR} (area = {AUC:0.2f})'.format(PRED_VAR=predictor_dict[p_var], AUC=roc_tbls[p_var]['auc'][0]),
                 )
    cur_ax.plot([-0.01, 1.01], [-0.01, 1.01], color='navy', lw=lw, linestyle='--')
    cur_ax.set_xlim([-0.01, 1.01])
    cur_ax.set_ylim([-0.01, 1.01])
    cur_ax.set_xlabel('1 - Specificity')
    cur_ax.set_ylabel('Sensitivity')
    cur_ax.legend(loc="lower right")
    
    # COMBINE ROC_TBLS INTO ONE ARRAY
    roc_pd = pd.DataFrame()
    for p_var in predictor_vars:
        roc_pd = pd.concat([roc_pd, roc_tbls[p_var]])
    return cur_ax, roc_pd

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
    
def scatter_plotly(pd_data, args_plotly, axis_labels):
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
    fig = px.scatter(pd_data, **args_plotly)
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