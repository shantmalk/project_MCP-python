import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import lib_prj
from plotly.offline import plot
import numpy as np

# dir_main = 'C:/Users/smalk/Desktop/research/prj-mcp'
# path_db = dir_main + '/data/database/db_CONFIRM-merged.accdb'

dir_main = 'C:/Users/smalk/OneDrive/Desktop/python-dev/prj-mcp-analysis'
path_db = dir_main + '/data/db_CONFIRM-merged.accdb'


# In[ ] CONFIRM DATA - LOAD DATA
qsel_confirm = "SELECT tblConfirmCONFIRM.* FROM tblConfirmCONFIRM;"
pd_confirm = lib_prj.process.db_query(path_db, qsel_confirm)

qsel_lesion = "SELECT tblConfirmPerLesion.* FROM tblConfirmPerLesion;"
pd_lesion = lib_prj.process.db_query(path_db, qsel_lesion)
pd_lesion['lesion_culprit_ica_ct'] = pd.to_numeric(pd_lesion['lesion_culprit_ica_ct'], errors='coerce').fillna(0)

# In[ ] ICONIC DATA - LOAD DATA
qsel_iconic = "SELECT tblConfirmICONIC.* FROM tblConfirmICONIC;"
pd_iconic = lib_prj.process.db_query(path_db, qsel_iconic)
pd_confirm = pd_confirm.merge(pd_iconic[['mi_type', 'confirm_idc']], how='left', on='confirm_idc')

# In[ ] CONFIRM DATA - LESION DATA - DEFINE CRITERIA FOR HIGH RISK PLAQUE
pd_lesion['is_hrp'] = ((pd_lesion['pr'] + pd_lesion['sc'] + pd_lesion['lap']) > 1) & (pd_lesion['lumenareastenosis'] > 50)
# pd_lesion['is_hrp'] = ((pd_lesion['pr'] + pd_lesion['sc'] + pd_lesion['lap']) > 1) 

# In[ ] CONFIRM DATA - ADDRESS MISSING VALUES
pd_confirm['fram_risk_confirm'] = pd_confirm['fram_risk_confirm'].fillna(pd_confirm['fram_risk_confirm'].mean())

# pd_confirm['mi_event'] = pd_confirm['mi_event'] & (pd_confirm['mi_time'] <= 1000)


# In[ ] MMAR DATA - LOAD DATA
qsel_mmar = "SELECT tblMCP.id_patient, tblMCP.id_vessel_study, tblMCP.mass_mcp_perc, tblMCP.id_main_vessel FROM tblMCP WHERE (((tblMCP.id_vessel) Like '%dist%'));"
pd_mmar = lib_prj.process.db_query(path_db, qsel_mmar)
pd_mmar = pd_mmar.reset_index().rename(columns={'id_patient' : 'confirm_idc', 'id_vessel_study' : 'lesion_id'})
pd_mmar = pd_mmar.merge(pd_lesion[['lesion_id', 'is_hrp', 'lumenareastenosis', 'plaquevolume_lesion', 'lesion_length', 'lumenvolume_lesion']], how='left', on='lesion_id')
# pd_mmar['mass_mcp_perc'] = pd_mmar['mass_mcp_perc'] * \
#                             (pd_mmar['plaquevolume_lesion'] * pd_mmar['lesion_length'] * pd_mmar['lumenareastenosis']) / \
#                             (pd_mmar['lumenvolume_lesion'])


# In[ ]
df_match_id_count = pd.DataFrame()
df_match_id_count['confirm_idc'] = pd_mmar.confirm_idc.unique()
df_match_id_count = df_match_id_count.merge(pd_confirm[['confirm_idc', 'mi_match_id']], how='left', on='confirm_idc')
df_match_id_count = df_match_id_count.groupby(['mi_match_id'], as_index=False).agg('count')
df_match_id_count = df_match_id_count.loc[df_match_id_count['confirm_idc'] == 2]
df_match_confirm = pd_confirm['confirm_idc'].loc[pd_confirm['mi_match_id'].isin(df_match_id_count['mi_match_id'])]

pd_mmar = pd_mmar.loc[pd_mmar['confirm_idc'].isin(df_match_confirm)]

# In[ ] CONFIRM DATA - LESION DATA - ADD HRP/LRP MMAR
pd_mmar['mmar_hrp'] = np.where(pd_mmar['is_hrp'], pd_mmar['mass_mcp_perc'], 0)
pd_mmar['mmar_lrp'] = np.where(~(pd_mmar['is_hrp']), pd_mmar['mass_mcp_perc'], 0)

# In[ ] MMAR DATA - AGGREGATE
pd_mmar_max = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'max')
pd_mmar_min = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'min')
pd_mmar_mean = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'mean')
pd_mmar_sum = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'sum')
pd_mmar_count = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'count')

pd_mmar_max_hrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'max', '_hrp', 'mmar_hrp')
pd_mmar_min_hrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'min', '_hrp', 'mmar_hrp')
pd_mmar_mean_hrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'mean', '_hrp', 'mmar_hrp')
pd_mmar_sum_hrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'sum', '_hrp', 'mmar_hrp')
pd_mmar_count_hrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'count', '_hrp', 'mmar_hrp')

pd_mmar_max_lrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'max', '_lrp', 'mmar_lrp')
pd_mmar_min_lrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'min', '_lrp', 'mmar_lrp')
pd_mmar_mean_lrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'mean', '_lrp', 'mmar_lrp')
pd_mmar_sum_lrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'sum', '_lrp', 'mmar_lrp')
pd_mmar_count_lrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'count', '_lrp', 'mmar_lrp')

# In[ ]
pd_mmar_max_all = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'max')
                  
# In[ ] COMBINE DATA - MERGE DATAFRAMES
PD_COMBINED_MAX = pd_mmar_max.merge(pd_confirm, how='left', on='confirm_idc')
PD_COMBINED_MIN = pd_mmar_min.merge(pd_confirm, how='left', on='confirm_idc')
PD_COMBINED_MEAN = pd_mmar_mean.merge(pd_confirm, how='left', on='confirm_idc')
PD_COMBINED_SUM = pd_mmar_sum.merge(pd_confirm, how='left', on='confirm_idc')
PD_COMBINED_COUNT = pd_mmar_count.merge(pd_confirm, how='left', on='confirm_idc')
# PD_COMBINED = pd.concat([PD_COMBINED_MAX, PD_COMBINED_MIN, PD_COMBINED_MEAN, PD_COMBINED_SUM])

PD_COMBINED = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'max', '_max').merge(pd_confirm, how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'min', '_min'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'mean', '_mean'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'sum', '_sum'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'count', '_n'), how='left', on='confirm_idc')

PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'max', '_max_hrp', 'mmar_hrp'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'min', '_min_hrp', 'mmar_hrp'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'mean', '_mean_hrp', 'mmar_hrp'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'sum', '_sum_hrp', 'mmar_hrp'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'count', '_n_hrp', 'mmar_hrp'), how='left', on='confirm_idc')

PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'max', '_max_lrp', 'mmar_lrp'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'min', '_min_lrp', 'mmar_lrp'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'mean', '_mean_lrp', 'mmar_lrp'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'sum', '_sum_lrp', 'mmar_lrp'), how='left', on='confirm_idc')
PD_COMBINED = PD_COMBINED.merge(lib_prj.process.mmar_agg_per_patient(pd_mmar, 'count', '_n_lrp', 'mmar_lrp'), how='left', on='confirm_idc')





PD_LESION = pd_lesion