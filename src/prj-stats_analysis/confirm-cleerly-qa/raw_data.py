import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import lib_prj
from plotly.offline import plot
import numpy as np
import re

# In[ ] SCCT MMAR VESSEL DATA - LOAD DATA
path_db = 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY-CLEERLY/DATABASE/db_CONFIRM-cleerly.accdb'
qsel_qa = "SELECT * FROM tblInfoCTA;"
pd_qa_cleerly = lib_prj.process.db_query(path_db, qsel_qa)
pd_qa_cleerly = pd_qa_cleerly.reset_index().rename(columns={'id_patient' : 'confirm_idc'})
pd_qa_cleerly = pd_qa_cleerly.drop(columns=['index'])

# In[ ] SCCT MMAR VESSEL DATA - LOAD DATA
path_db = 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY/DATABASE/db_CONFIRM.accdb'
qsel_qa = "SELECT * FROM tblInfoCTA;"
pd_qa_vitrea = lib_prj.process.db_query(path_db, qsel_qa)
pd_qa_vitrea = pd_qa_vitrea.reset_index().rename(columns={'id_patient' : 'confirm_idc'})
pd_qa_vitrea = pd_qa_vitrea.drop(columns=['index'])

# In[ ] MERGE
pd_qa = pd_qa_cleerly.merge(pd_qa_vitrea, how='inner', on='confirm_idc')

# In[ ] CALCULATE MATCHES
pd_qa['match_cta_series_uid'] = pd_qa['cta_series_uid_x'] == pd_qa['cta_series_uid_y']
pd_qa['match_cta_series_uid'] = pd_qa['match_cta_series_uid'].astype('int')

pd_qa['match_cta_series_description'] = pd_qa['cta_series_description_x'] == pd_qa['cta_series_description_y']
pd_qa['match_cta_series_description'] = pd_qa['match_cta_series_description'].astype('int')

# In[ ] Count mismatches
print('Mismatched series:  %i' %  (len(pd_qa['match_cta_series_description']) - pd_qa['match_cta_series_description'].sum()))
print('Matching series:  %i' %  pd_qa['match_cta_series_description'].sum())

# In[ ] CALCULATE UNPROCESSED - IN VITREA NOT IN CLEERLY
pd_qa_missing_vitrea = pd_qa_vitrea.merge(pd_qa_cleerly, how='right', on='confirm_idc')
pd_qa_missing_vitrea = pd_qa_missing_vitrea[(pd_qa_missing_vitrea['id_user_x'].isnull())]

    
