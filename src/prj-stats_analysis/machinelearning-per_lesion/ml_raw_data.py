# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 18:54:51 2020

@author: smalk
"""

import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import lib_prj
from plotly.offline import plot

# dir_main = 'C:/Users/smalk/Desktop/research/prj-mcp'
# path_db = dir_main + '/data/database/db_CONFIRM-merged.accdb'

dir_main = 'C:/Users/smalk/OneDrive/Desktop/python-dev/prj-mcp-analysis'
path_db = dir_main + '/data/db_CONFIRM-merged.accdb'

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

# DEFINE FUNCTION:  clean_cols
def clean_cols(df:'pd.DataFrame') -> 'pd.DateFrame':
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    df.columns = df.columns.str.replace('\t','')
    df.columns = df.columns.str.replace('\ufeff', '')
    df.columns = df.columns.str.replace("''", '')
    return df

# DEFINE FUNCTION: mmar_agg
def mmar_agg_per_vessel(df:'pd.DataFrame', agg_func, tag='') -> 'pd.Dataframe':
    df_agg = df.groupby(['id_patient', 'id_main_vessel'], as_index=False).agg(agg_func)
    df_agg = df_agg.pivot(index='id_patient', columns='id_main_vessel', values='mass_mcp_perc').rename(columns={'lad' : 'mmar_lad' + tag, 'lcx' : 'mmar_lcx' + tag, 'rca' : 'mmar_rca' + tag}).fillna(0)
    df_agg['mmar_total' + tag] = df_agg.sum(axis=1)
    df_agg['mmar_agg_type'] = agg_func
    return df_agg.reset_index().rename(columns={'id_patient' : 'confirm_idc'})

# DEFINE FUNCTION: view_combined_per_vessel
def view_combined_per_vessel(df:'pd.DataFrame', title):
    df_melt = pd.melt(df, id_vars=['confirm_idc', 'mmar_agg_type', 'mi_event'], value_vars=['mmar_lad', 'mmar_lcx', 'mmar_rca', 'mmar_total'], value_name='mmar', var_name='mmar_vessel')
    args_plotly = {
    'x' : 'mmar_vessel',
    'points' : 'all',
    'color' : 'mi_event',
    'labels' : {'mi_event' : 'MI'},
    'facet_col' : 'mmar_agg_type',
    }
    figure_label = 'MMAR Max'
    y_data = 'mmar'
    y_label = 'MMAR (%)'
    figure_fname_lable = figure_label.lower().replace(' ', '')
    args_plotly['y'] = [y_data]
    args_plotly['title'] = title
    fig = lib_prj.visualize.boxplot_plotly(df_melt, args_plotly, '')
    fig.update_yaxes(title=y_label)
    fig.update_xaxes(title='')
    # fig.update_layout(showlegend=False)
    plot_url = plot(fig, filename=title.replace(' ','_') + '.html')


# In[ ] MMAR DATA - LOAD DATA
qsel_mmar = "SELECT tblMCP.id_vessel_study, tblMCP.mass_mcp_perc, tblMCP.mass_mcp_g, tblMCP.id_main_vessel FROM tblMCP WHERE (((tblMCP.id_vessel) Like '%dist%'));"
pd_mmar = db_query(path_db, qsel_mmar)
pd_mmar = pd_mmar.rename(columns={'id_vessel_study' : 'lesion_id'})

# In[ ] CONFIRM DATA - LOAD DATA
qsel_confirm = "SELECT tblConfirmPerLesion.* FROM tblConfirmPerLesion;"
pd_confirm = db_query(path_db, qsel_confirm)
pd_confirm['lesion_culprit_ica_ct'] = pd.to_numeric(pd_confirm['lesion_culprit_ica_ct'], errors='coerce').fillna(0)
pd_confirm['is_hrp'] = (pd_confirm['pr'] + pd_confirm['sc'] + pd_confirm['lap']) > 1
# pd_confirm['fram_risk_confirm'] = pd_confirm['fram_risk_confirm'].fillna(pd_confirm['fram_risk_confirm'].mean())
# In[ ] COMBINE DATA - MERGE DATAFRAMES
PD_COMBINED = pd_mmar.merge(pd_confirm, how='left', on='lesion_id')

# In[ ] BASIC FIGURES


if __name__ == '__main__':
    view_combined_per_vessel(PD_COMBINED, '')






