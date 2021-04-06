import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import lib_prj
from plotly.offline import plot
import numpy as np
import re

# DATASET WITH CLEERLY CENTERLINES
# path_db = 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY-CLEERLY/DATABASE/db_CONFIRM-cleerly.accdb'
path_db = 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY/DATABASE/db_CONFIRM.accdb'


# In[ ] CONFIRM DATA - LOAD DATA
qsel_confirm = "SELECT tblConfirmCONFIRM.* FROM tblConfirmCONFIRM;"
pd_confirm = lib_prj.process.db_query(path_db, qsel_confirm)
pd_confirm['confirm_idc'] = pd_confirm['confirm_idc'].astype('int64')

qsel_lesion = "SELECT tblConfirmPerLesion.* FROM tblConfirmPerLesion;"
pd_lesion = lib_prj.process.db_query(path_db, qsel_lesion)
pd_lesion['lesion_culprit_ica_ct'] = pd.to_numeric(pd_lesion['lesion_culprit_ica_ct'], errors='coerce').fillna(0)

# In[ ] ICONIC DATA - LOAD DATA
qsel_iconic = "SELECT tblConfirmICONIC.* FROM tblConfirmICONIC;"
pd_iconic = lib_prj.process.db_query(path_db, qsel_iconic)
pd_confirm = pd_confirm.merge(pd_iconic[['mi_type', 'confirm_idc']], how='left', on='confirm_idc')


# In[ ] REDCAP DATA - LOAD DATA
# CONTAINS TROPONIN DATA
qsel_redcap = "SELECT tblConfirmRedcap.* FROM tblConfirmRedcap;"
pd_redcap = lib_prj.process.db_query(path_db, qsel_redcap)


# In[ ] SCCT MMAR VESSEL DATA - LOAD DATA
qsel_scct = "SELECT tblMCP.id_patient, tblMCP.id_vessel, tblMCP.mass_mcp_perc, tblMCP.id_main_vessel FROM tblMCP WHERE (((tblMCP.id_vtree) Like '%scct%'));"
pd_scct = lib_prj.process.db_query(path_db, qsel_scct)
pd_scct = pd_scct.reset_index().rename(columns={'id_patient' : 'confirm_idc'})
pd_scct = pd_scct.drop(columns=['index'])
# FILTER VESSEL BRANCHES USING REGEX - TO ALLOW GROUPING OF SUB BRANCHES
# filt_br = lambda b : re.sub(r"((_\d)+$)|(\br_)|(\bl_)", '', b)
filt_br = lambda b : re.sub(r"((_\d)+$)", '', b)
filt_br_r = lambda b : re.sub(r"(\br_)", 'R-', b)
filt_br_l = lambda b : re.sub(r"(\bl_)", 'L-', b)
pd_scct['id_vessel'] = [filt_br_l(filt_br_r(filt_br(br))) for br in pd_scct['id_vessel']]
scct_brs = list(pd.Series([filt_br_l(filt_br_r(filt_br(br))) for br in pd_scct['id_vessel'].unique()]).unique())
pd_scct = pd_scct.groupby(by=['confirm_idc', 'id_vessel']).agg('sum').reset_index()
pd_scct['confirm_idc'] = pd_scct['confirm_idc'].astype('float')
pd_scct = pd_scct.merge(pd_confirm[['confirm_idc', 'mi_event', 'mi_type', 'mace_event_confirm']], on='confirm_idc', how='left')

# In[ ] MCP-MMAR QA - LOAD DATA
qsel_mcp_qa = "SELECT tblMCP_QA.id_patient, tblMCP_QA.qa_centerlines, tblMCP_QA.qa_mcp, tblMCP_QA.qa_lv_segmentation FROM tblMCP_QA;"
pd_mcp_qa = lib_prj.process.db_query(path_db, qsel_mcp_qa)
pd_mcp_qa['id_patient'] = pd_mcp_qa['id_patient'].astype('float')
pd_mcp_qa = pd_mcp_qa.reset_index().rename(columns={'id_patient' : 'confirm_idc'})


pd_mcp_qa = pd_mcp_qa.loc[(pd_mcp_qa['qa_mcp'] == 3) & (pd_mcp_qa['qa_centerlines'] == 3) & (pd_mcp_qa['qa_lv_segmentation'] == 3)]

# pd_mcp_qa = pd_mcp_qa[np.where(pd_mcp_qa['qa_mcp'] == 3 & pd_mcp_qa['qa_centerlines'] == 3 & pd_mcp_qa['qa_lv_segmentation'] == 3, 3)]

PD_SCCT = pd_scct.merge(pd_mcp_qa[['confirm_idc']], on='confirm_idc', how='right')





