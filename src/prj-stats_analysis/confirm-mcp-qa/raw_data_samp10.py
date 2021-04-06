import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import lib_prj
from plotly.offline import plot
import numpy as np
import re

# MAIN DATASET - GHAZAL PROCESSING
# dir_main = 'C:/Users/smalk/Desktop/research/prj-mcp'
# path_db = dir_main + '/data/database/db_CONFIRM-merged.accdb'
dir_main = 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY/DATABASE'
path_db = dir_main + '/db_CONFIRM-old.accdb'

# dir_main = 'C:/Users/smalk/OneDrive/Desktop/python-dev/prj-mcp-analysis'
# path_db = dir_main + '/data/db_CONFIRM-merged.accdb'

# DATASET WITH CLEERLY CENTERLINES
# path_db = 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY-CLEERLY/DATABASE/db_CONFIRM-cleerly.accdb'


# In[ ] SCCT MMAR VESSEL DATA - LOAD DATA
qsel_scct = "SELECT tblMCP.id_patient, tblMCP.id_vessel, tblMCP.mass_mcp_perc, tblMCP.id_main_vessel FROM tblMCP WHERE (((tblMCP.id_vtree) Like '%scct%'));"
pd_scct = lib_prj.process.db_query(path_db, qsel_scct)
pd_scct = pd_scct.reset_index().rename(columns={'id_patient' : 'confirm_idc'})
pd_scct = pd_scct.drop(columns=['index'])

# FILTER VESSEL BRANCHES USING REGEX - TO ALLOW GROUPING OF SUB BRANCHES
filt_br = lambda b : re.sub(r"((_\d)+$)|(\br_)|(\bl_)", '', b)
pd_scct['id_vessel'] = [filt_br(br) for br in pd_scct['id_vessel']]
scct_brs = list(pd.Series([filt_br(br) for br in pd_scct['id_vessel'].unique()]).unique())
pd_scct = pd_scct.groupby(by=['confirm_idc', 'id_vessel']).agg('sum').reset_index()
pd_scct['confirm_idc'] = pd_scct['confirm_idc'].astype('float')
pd_scct[pd_scct['mass_mcp_perc'] < 0 ] = 0
pd_scct = pd_scct.rename(columns={'mass_mcp_perc' : 'mass_mcp_perc_10'}) 

# In[ ] MMAR DATA - LOAD DATA
qsel_mmar = "SELECT tblMCP.id_patient, tblMCP.id_vessel_study, tblMCP.mass_mcp_perc, tblMCP.id_main_vessel FROM tblMCP WHERE (((tblMCP.id_vessel) Like '%dist%'));"
pd_mmar = lib_prj.process.db_query(path_db, qsel_mmar)
pd_mmar = pd_mmar.reset_index().rename(columns={'id_patient' : 'confirm_idc', 'id_vessel_study' : 'lesion_id'})



