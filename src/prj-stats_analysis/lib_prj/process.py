# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:01:54 2020

@author: smDesktop
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols

def mk_pd_dict(df_data, metric_var, dict_var, ignore_cols=[]):
    '''

    Parameters
    ----------
    df_data : TYPE
        DESCRIPTION.
    metric_var : TYPE
        DESCRIPTION.

    Returns
    -------
    df_dict : TYPE
        DESCRIPTION.

    '''
       
    df_dict = dict()
    for k,v in zip(dict_var.keys(), dict_var.values()):
        if v == 'sum':
            df_dict[k] = df_data.groupby('confirm_idc', as_index=False).sum()
        elif v == 'avg':
            df_dict[k] = df_data.groupby('confirm_idc', as_index=False).mean()
        else:
            df_dict[k] = df_data.groupby('confirm_idc', as_index=False).agg(v)
        for i in ignore_cols:
            df_dict[k][i] = df_data[i]
    return df_dict

def agg_dataframe_dict(agg_var, dict_df):
    '''
    

    Parameters
    ----------
    agg_var : STR
        Name of aggregation column.
    dict_df : DICT["agg_label"] = pd.DataFrame
        Keys are aggregate labels, values are DataFrames representing aggregation based on criteria described in aggregate labels.

    Returns
    -------
    df_agg : DATAFRAME
        Aggregated DataFrame.  Entries are repeated.  Beware.
    '''
    
    df_agg = pd.DataFrame()
    for k,v in zip(dict_df.keys(), dict_df.values()):
        v[agg_var] = k
        df_agg = df_agg.append(v)
    return df_agg

def filt_dummy_var(pd_data, dummy_col, cond=1):
    pd_filt = pd_data[pd_data[dummy_col] == cond]
    pd_filt.reset_index(inplace=True)
    return pd_filt

def stats_anova(pd_data, idx_cols, var_col):
    pd_comb_data = pd.concat([filt_dummy_var(pd_data, dcol)[var_col] for dcol in idx_cols], axis=1)
    pd_comb_data.columns = idx_cols
    pd_melt = pd.melt(pd_comb_data.reset_index(), id_vars=['index'], value_vars=idx_cols)
    pd_melt.columns = ['index', 'idx_cols', 'value']
    model = ols('value ~ C(idx_cols)', data=pd_melt).fit()
    return sm.stats.anova_lm(model, typ=2)
