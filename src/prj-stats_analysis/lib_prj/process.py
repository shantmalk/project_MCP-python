# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:01:54 2020

@author: smDesktop
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from plotly.offline import plot
from plotly.express import bar
from scipy.stats import entropy
import pyodbc
from zepid import RiskRatio
from scipy.stats import norm


def relative_risk(df:'pd.DataFrame', exposure:'str', outcome:'str'):
    
    rr = RiskRatio()
    rr.fit(df, exposure=exposure, outcome=outcome)
    est= rr.results['RiskRatio'][1]
    std = rr.results['SD(RR)'][1]
    
    # calculating p-value
    z_score = np.log(est)/std
    p_val = norm.sf(abs(z_score))*2
    
    return [exposure, est, std, p_val]

# DEFINE FUNCTION: mmar_agg
def mmar_agg_per_vessel(df:'pd.DataFrame', agg_func:'str', tag='', mmar_col='mass_mcp_perc') -> 'pd.Dataframe':
    """
    mmar_agg_per_vessel aggregates myocardial mass at-risk (MMAR) per-patient, for LAD/LCx/RCA.  Function is specifically used to process CONFIRM per-lesion data with MMAR.  The inputted df is outputted with the addition of aggregate columns.

    Parameters
    ----------
    df : 'pd.DataFrame'
        DataFrame of CONFIRM per-lesion data with associated MMAR.
    agg_func : STR
        Name of aggregate function to use (ex. max/min/mean/sum/count).
    tag : STR, optional
        Column tag to append to new aggregate columns. The default is ''.
    mmar_col : STR, optional
        Column containing MMAR data to aggregate. The default is 'mass_mcp_perc'.
        
    Returns
    -------
    pd.DataFrame
        Return df with new aggregate columns.  Returned df will have 3 new columns for the LAD, LCx and RCA.  Each column will have aggregated MMAR based on specified agg_func, for each patient.

    """
    df_agg = df.groupby(['confirm_idc', 'id_main_vessel'], as_index=False).agg(agg_func)
    df_agg = df_agg.pivot(index='confirm_idc', columns='id_main_vessel', values=mmar_col).rename(columns={'lad' : 'mmar_lad' + tag, 'lcx' : 'mmar_lcx' + tag, 'rca' : 'mmar_rca' + tag}).fillna(0)
    # df_agg['mmar_total' + tag] = df_agg.sum(axis=1) # THIS IS PROBLEMATIC - THIS SHOULD BE PLACED IN DIFFERENT FUNCTION
    df_agg['mmar_agg_type'] = agg_func
    return df_agg.reset_index()

# DEFINE FUNCTION: mmar_agg
def mmar_agg_per_patient(df:'pd.DataFrame', agg_func:'str', tag='', mmar_col='mass_mcp_perc') -> 'pd.Dataframe':
    """
    mmar_agg_per_vessel aggregates myocardial mass at-risk (MMAR) per-patient.  Function is specifically used to process CONFIRM per-lesion data with MMAR.  The inputted df is outputted with the addition of aggregate columns.

    Parameters
    ----------
    df : 'pd.DataFrame'
        DataFrame of CONFIRM per-lesion data with associated MMAR.
    agg_func : STR
        Name of aggregate function to use (ex. max/min/mean/sum/count).
    tag : STR, optional
        Column tag to append to new aggregate columns. The default is ''.
    mmar_col : STR, optional
        Column containing MMAR data to aggregate. The default is 'mass_mcp_perc'.
        
    Returns
    -------
    pd.DataFrame
        Return a new DataFrame with aggregate column.  Returned DataFrame will have 1 new column for aggregated MMAR data.  Each row will have aggregated MMAR based on specified agg_func, for each patient.

    """
    
    include_cols = ['confirm_idc', mmar_col]
    df_agg = df[include_cols].groupby(['confirm_idc'], as_index=False).agg(agg_func)
    df_agg = df_agg.rename(columns={mmar_col : 'mmar_all' + tag}).fillna(0)
    df_agg['mmar_agg_type'] = agg_func
    return df_agg.reset_index()

# DEFINE FUNCTION:  clean_cols
def clean_cols(df:'pd.DataFrame') -> 'pd.DateFrame':
    """clean_cols runs a few functions to clean data in specified pandas DataFrame

    Parameters
    ----------
    df : 'pd.DataFrame'
        Pandas DataFrame to clean.

    Returns
    -------
    df : pd.DataFrame
        Cleaned pandas DataFrame.

    """
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    df.columns = df.columns.str.replace('\t','')
    df.columns = df.columns.str.replace('\ufeff', '')
    df.columns = df.columns.str.replace("''", '')
    return df

# DEFINE FUNCTION:  db_query
def db_query(path_db:str, qsel:str) -> "pd.DataFrame":
    """db_query queries a database and returns its response
    This function is used to query a database.  It will return the response from the database as a Pandas dataframe
    
    TODO:
    Check inputs
    Check outputs
    Check if path_db exists before execution
    """
    path_db_frmt = r'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={PATH};'.format(PATH=path_db)
    conn = pyodbc.connect(path_db_frmt)
    db_resp = pd.read_sql_query(qsel, conn)
    
    # CLEAN COLUMNS
    db_resp = db_resp.replace(r'^\s*$', '0', regex=True)
    db_resp = clean_cols(db_resp)
    return db_resp

# Set of functions to streamline statistical processing
def view_features_variance(df:'pd.DataFrame', title:str):
    '''
    Provide DataFrame containing an "feature" column and column  entropy and view feature variance

    Parameters
    ----------
    df : 'pd.DataFrame'
        DataFrame of data to view variance of; Assumes DataFrame has a column 'feature' representing feature names and ft representing corresponding feature's variance.
    title : str
        Title to include in figure.

    Returns
    -------
    fig : Plotly Figure

    '''
    col_name_ft = 'feature'
    col_name_entropy = 'entropy'
    
    args_plotly = {
    'y' : col_name_ft,
    'x' : col_name_entropy,
    }
    
    y_label = 'Information Gain - ' + args_plotly['x']
    figure_fname_label = title.lower().replace(' ', '')
    args_plotly['title'] = title
    fig = bar(df, **args_plotly)
    fig.update_yaxes(title=y_label)
    fig.update_xaxes(title='')
    plot_url = plot(fig, filename=title.replace(' ','_') + '.html')
    return fig

def information_gain(members, split):
    '''
    Measures the reduction in entropy after the split  
    :param v: Pandas Series of the members
    :param split:
    :return:
    '''
    entropy_before = entropy(members.value_counts(normalize=True))
    split.name = 'split'
    members.name = 'members'
    grouped_distrib = members.groupby(split) \
                        .value_counts(normalize=True) \
                        .reset_index(name='count') \
                        .pivot_table(index='split', columns='members', values='count').fillna(0)
    
    entropy_after = entropy(grouped_distrib, axis=1)
    if not len(entropy_after):
        entropy_after = [0]
    entropy_after = entropy_after * split.value_counts(sort=False, normalize=True)
    return entropy_before - entropy_after.sum()

def information_gain_df(df:'pd.DataFrame', col_select:[str], col_split:str) -> 'pd.DataFrame':
    '''
    Calculate change in entropy associated with each column of df.  Every column of df should represent a "feature".  
    Contribution of each "feature" in reducing entropy, based on split, the name of the column in df to use as a "dependent" variable to calculate entropy in relation to.

    Parameters
    ----------
    df : 'pd.DataFrame'
        Every column should represent a "feature".
    col_select : [str]
        List of column names to include to calculate entropy of.
    col_split : str
        Column name to use as dependent variable to calculate entropy in relation to.

    Returns
    -------
    TYPE
        Return DataFrame with two columns, feature and entropy.
    '''
    
    col_name_ft = 'feature'
    col_name_entropy = 'entropy'
    
    features = pd.DataFrame(columns=[col_name_ft, col_name_entropy])
    for ii in range(len(col_select)):
        features = features.append({col_name_ft : col_select[ii], col_name_entropy : information_gain(df[col_select[ii]], df[col_split])}, ignore_index=True)
    return features.sort_values(by=[col_name_entropy])

def clean_df(df:'pd.DataFrame', col_select:[str], col_remove:[str]) -> [str]:
    '''
    Only includes selected columns as specified in col_select.  
    Additionally, filters out based on [two] criteria:  (1) Exclude columns if there are any missing values, (2) Exclude columns that have string values
    Finally, remove columns defined in blacklist
    
    Parameters
    ----------
    df : 'pd.DataFrame'
        DataFrame to assess.
    col_select : [str]
        List of column names to include.
    col_remove : [str]
        List of column names to exclude.

    Returns
    -------
    [str]
        DESCRIPTION.

    '''
    
    # Make copy of col_select
    col_clean = col_select.copy()
    
    # Iterate over only selected columns
    for ii in range(len(col_select)):
        
        # Criteria 1:  Only include columns that have NO empty cells
        cur_count = (len(df[col_select[ii]]) - df[col_select[ii]].count()) / len(df[col_select[ii]])
        if cur_count > 0:
            if col_select[ii] in col_clean:
                col_clean.remove(col_select[ii])
        
        # Criteria 2:  Only include columns that are NOT type(str)
        if type(df[col_select[ii]][0]) is str:
            if col_select[ii] in col_clean:
                col_clean.remove(col_select[ii])
    
    # Remove columns listed in col_remove
    [col_clean.remove(ii) for ii in col_remove if ii in col_clean]

    return col_clean.copy()
    


# Various adapters for working with Pandas
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


# Various statistic helpers

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
