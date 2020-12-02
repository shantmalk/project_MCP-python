#!/usr/bin/env python
# coding: utf-8

# In[45]:


# JUPYTER NOTEBOOK - 11/18/2020
# AUTHOR:  Shant Malkasian
# DESCRIPTION:  Jupyter notebook for analyzing CONFIRM dataset.  This is a test script, focusing on applying standard data science practices.
# See https://www.kaggle.com/faressayah/linear-regression-house-price-prediction for inspiration


# # Setup

# In[1]:

from plotly.offline import plot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc
from lifelines import *
from lifelines.datasets import load_waltons
from lifelines.utils import survival_table_from_events
import lib_prj
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# DEFINE FUNCTION:  db_query
def db_query(path_db:str, qsel:str) -> "pandas.core.frame.DataFrame":
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


# In[3]:


# DEFINE FUNCTION:  mk_query
def mk_query(tbl_name:str, id_field:str) -> str:
    """mk_query creates a SQL query with a standardized format
    Queried tables created using mk_query can be aggregated on the tblConfirmPerLesion.lesion_id field
    """
    return "SELECT tblConfirmPerLesion.lesion_id, {TBL_NAME}.* FROM tblConfirmPerLesion, tblConfirmCONFIRM, {TBL_NAME} INNER JOIN [qselMCP-Completed-AllPhases] ON {TBL_NAME}.{ID_FIELD} = [qselMCP-Completed-AllPhases].[confirm_idc];".format(TBL_NAME=tbl_name, ID_FIELD=id_field)


# In[4]:


# DEFINE FUNCTION:  clean_cols
def clean_cols(df:'pandas.core.frame.DataFrame') -> 'pandas.core.frame.DateFrame':
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    df.columns = df.columns.str.replace('\t','')
    df.columns = df.columns.str.replace('\ufeff', '')
    df.columns = df.columns.str.replace("''", '')
    return df


# In[6]:


# SETUP PLOT STYLES
sns.set_style("whitegrid")
plt.style.use("fivethirtyeight")


# In[7]:


# SETUP PATHS
dir_main = 'C:/Users/smalk/Desktop/research/prj-mcp'
path_db = dir_main + '/data/database/db_CONFIRM-merged.accdb'


# In[9]:


# PARSE DATABASE - ALL DATA
# This block will combine multiple tables into one dataframe.  In this case, we will merge on the confirm_idc[INT] field

# GET TABLES FROM DATABASE
df_confirm = db_query(path_db, 'SELECT * FROM tblConfirmCONFIRM')
df_mcp = db_query(path_db, 'SELECT * FROM tblMCP').rename(columns={'id_patient' : 'confirm_idc', 'id_vessel_study' : 'lesion_id'}) # change id_patient to confirm_idc (TODO: MAKE SURE ALL NEW TALBES USE CONFIRM_IDC[INT])
df_matched = db_query(path_db, 'SELECT * FROM "qselMCP-Completed-matched"')
df_mcp = df_mcp[df_mcp['id_vessel'].str.contains('dist')]
df_lesion = db_query(path_db, 'SELECT * FROM tblConfirmPerLesion')

# TBLMCP - Set index to confirm_idc
df_mcp.set_index('confirm_idc')

# TBLMATCHID

# TBLCONFIRMCONFIRM - Set index to confirm_idc
df_confirm.set_index('confirm_idc')

# TBLCONFIRMLESION - Set index to lesion_id
df_lesion.set_index('lesion_id')

# COMBINED - Make combined table
df_combined = df_mcp.merge(df_confirm, on='confirm_idc')
df_combined = df_combined.merge(df_lesion, on=['lesion_id', 'confirm_idc'])


# # Clean data

# In[10]:


# FILTER FOR ONLY SUBTENDED MYOCARDIUM
df_main = df_combined[df_combined['id_vessel'].str.contains('dist')]
df_main.head()


# In[11]:


# COMBINE DATA


# # View data

# # Exploratory data analysis (EDA)

# In[12]: GENERAL ANALYSIS

plt.figure()
# sns.distplot(df_main.groupby(['confirm_idc']).mean()['acm_time_confirm'])
sns.distplot(df_main.groupby(['confirm_idc']).mean()['mi_time'])


# In[13]:

plt.figure()
sns.distplot(df_main['acm_time_confirm'])


# In[14]:

plt.figure()
sns.distplot(df_main['mass_mcp_g'])


# In[15]:

plt.figure()
sns.distplot(df_main[df_main['culprit_lesion_verifiedbyica'] == '1']['mass_mcp_g'])
sns.distplot(df_main[df_main['culprit_lesion_verifiedbyica'] != '1']['mass_mcp_g'])


# In[16]:

plt.figure()
# sns.distplot(df_main[df_main['culprit_lesion_verifiedbyica'] != '1']['mass_mcp_g'])
sns.distplot(df_main.groupby(['confirm_idc'])['culprit_lesion_verifiedbyica'])


# In[19]:
df_roc = df_main
df_roc['culprit_lesion_verifiedbyica'] = df_main['culprit_lesion_verifiedbyica'] == '1'
predictor_var = ['mass_mcp_g', 'mass_mcp_perc']
lib_prj.visualize.roc_plot(df_roc, 'culprit_lesion_verifiedbyica', predictor_var, {'mass_mcp_g' : 'Absolute MMAR','mass_mcp_perc' : 'Relative MMAR'})

# In[ ]:  VIEW MMAR_VAR - VIEW VARIATIONS OF MMAR AGGREGATION (MAX, MEAN, SUM)




# df_mcp_comb.columns = df_mcp_comb.columns.str.replace('_y', '')

df_mcp_comb = df_combined.copy()
# to_drop = [x for x in df_mcp_comb if x.endswith('_x')]
# df_mcp_comb.drop(to_drop, axis=1)
df_mcp_comb.columns = df_mcp_comb.columns.str.replace('_x', '')


# Remove unmatched columns
idx_matched = df_mcp_comb['mi_match_id'].str.contains("|".join(df_matched['mi_match_id']))
df_mcp_comb = df_mcp_comb.loc[idx_matched]

# Add column - special composites, combining mmar with another plaque characteristic
# df_mcp_comb['mcp_csa'] = df_mcp_comb['mass_mcp_perc'] * df_mcp_comb['']


roc_var = 'mi_event'

metric_var = 'mass_mcp_perc'
mmar_var_col = 'mmar_agg_type'
# agg_var_dict = {'mmar_avg' : 'avg',
#                 'mmar_sum' : 'sum',
#                 }

agg_var_dict = {'mmar_max' : 'max', 
                'mmar_min' : 'min',
                'mmar_avg' : 'avg',
                'mmar_sum' : 'sum',
                }

df_dict = lib_prj.process.mk_pd_dict(df_mcp_comb, metric_var, agg_var_dict, [roc_var])
df_mmar = lib_prj.process.agg_dataframe_dict(mmar_var_col, df_dict)
df_mmar['mi_event'] = df_mmar['mi_event'].fillna(0)

# In[ ]: RECREATE DATA USING "WORST" LESION
df_split_mi = df_mmar[df_mmar['mi_event'] == 1]
df_split_mi = df_mmar[df_mmar['culprit_lesion_verifiedbyica'] == 1]
df_split_no_mi = df_mmar[df_mmar['mi_event'] != 1]
df_split_no_mi = df_mmar[df_mmar['lesion_worst'] == 1]


# In[ ]: VIEW MMAR_SUM
agg_func = 'mmar_sum'
df_roc = df_mmar[df_mmar[mmar_var_col] == agg_func]
predictor_var = ['mass_mcp_g', 'mass_mcp_perc']
lib_prj.visualize.roc_plot(df_roc, roc_var, predictor_var, {'mass_mcp_g' : 'Absolute MMAR','mass_mcp_perc' : 'Relative MMAR'})[0].title(agg_func)

# In[ ]: VIEW MMAR_MAX
agg_func = 'mmar_max'
df_roc = df_mmar[df_mmar[mmar_var_col] == agg_func]
predictor_var = ['mass_mcp_g', 'mass_mcp_perc']
lib_prj.visualize.roc_plot(df_roc, roc_var, predictor_var, {'mass_mcp_g' : 'Absolute MMAR','mass_mcp_perc' : 'Relative MMAR'})[0].title(agg_func)

# In[ ]: VIEW MMAR_MIN
agg_func = 'mmar_min'
df_roc = df_mmar[df_mmar[mmar_var_col] == agg_func]
predictor_var = ['mass_mcp_g', 'mass_mcp_perc']
lib_prj.visualize.roc_plot(df_roc, roc_var, predictor_var, {'mass_mcp_g' : 'Absolute MMAR','mass_mcp_perc' : 'Relative MMAR'})[0].title(agg_func)



# In[ ]:  VIEW AGGR OF MMAR_VARS
# plt.figure()
sns.boxplot(x=metric_var, y=mmar_var_col, data=df_mmar)