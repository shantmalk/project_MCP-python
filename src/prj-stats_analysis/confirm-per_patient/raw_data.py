import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
import lib_prj
from plotly.offline import plot
import numpy as np

dir_main = 'C:/Users/smalk/Desktop/research/prj-mcp'
path_db = dir_main + '/data/database/db_CONFIRM-merged.accdb'

# dir_main = 'C:/Users/smalk/OneDrive/Desktop/python-dev/prj-mcp-analysis'
# path_db = dir_main + '/data/db_CONFIRM-merged.accdb'


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
# pd_lesion['is_hrp'] = ((pd_lesion['pr'] + pd_lesion['sc'] + pd_lesion['lap']) > 1) & (pd_lesion['lumenareastenosis'] > 50)
pd_lesion['is_hrp'] = ((pd_lesion['pr'] + pd_lesion['sc'] + pd_lesion['lap']) > 1)
# pd_lesion['is_hrp'] = pd_lesion['lesion_worst'] & pd_lesion['mldlesion_epicardial']
# pd_lesion['is_hrp'] = pd_lesion['lesion_worst']

pd_lesion['is_hrp'] = pd_lesion['is_hrp'].astype('int16')
pd_lesion['is_lrp'] = np.where(pd_lesion['is_hrp'], 0, 1)
pd_lesion['is_lrp'] = pd_lesion['is_lrp'].astype('int16')

pd_lesion['is_hrp_lad'] = np.where(pd_lesion['is_hrp'] & (pd_lesion['mldlesion_arterial_dist'] == 'lad'), 1, 0)
pd_lesion['is_lrp_lad'] = np.where(pd_lesion['is_lrp'] & (pd_lesion['mldlesion_arterial_dist'] == 'lad'), 1, 0)

pd_lesion['is_hrp_lcx'] = np.where(pd_lesion['is_hrp'] & (pd_lesion['mldlesion_arterial_dist'] == 'lcx'), 1, 0)
pd_lesion['is_lrp_lcx'] = np.where(pd_lesion['is_lrp'] & (pd_lesion['mldlesion_arterial_dist'] == 'lcx'), 1, 0)

pd_lesion['is_hrp_rca'] = np.where(pd_lesion['is_hrp'] & (pd_lesion['mldlesion_arterial_dist'] == 'rca'), 1, 0)
pd_lesion['is_lrp_rca'] = np.where(pd_lesion['is_lrp'] & (pd_lesion['mldlesion_arterial_dist'] == 'rca'), 1, 0)


# In[ ] CONFIRM DATA - ADDRESS MISSING VALUES
pd_confirm['fram_risk_confirm'] = pd_confirm['fram_risk_confirm'].fillna(pd_confirm['fram_risk_confirm'].mean())

# In[ ] FILTER MI OCCURRENCE FOR UNIFIED TIME AFTER CTA
# pd_confirm= pd_confirm.loc[pd_confirm['mi_time'] < (3 * 365)]
# pd_confirm['mi_event'] = pd_confirm['mi_event'] & (pd_confirm['mi_time'] <= 365)
# pd_confirm = pd_confirm.loc[(pd_confirm['mi_event'] & (pd_confirm['mi_time'] <= 365 * 1)) | (pd_confirm['mi_event'] == 0)]

# pd_confirm = pd_confirm.loc[pd_confirm['mi_event'] == 1]

# pd_confirm['mi_event'] = (pd_confirm['mi_type'] == 1) | (pd_confirm['mi_type'] == 2)

# In[ ] MMAR DATA - LOAD DATA
qsel_mmar = "SELECT tblMCP.id_patient, tblMCP.id_vessel_study, tblMCP.mass_mcp_perc, tblMCP.id_main_vessel FROM tblMCP WHERE (((tblMCP.id_vessel) Like '%dist%'));"
pd_mmar = lib_prj.process.db_query(path_db, qsel_mmar)
pd_mmar = pd_mmar.reset_index().rename(columns={'id_patient' : 'confirm_idc', 'id_vessel_study' : 'lesion_id'})
pd_mmar = pd_mmar.merge(pd_lesion[['lesion_id', 'mldlesion_arterial_dist', 'is_lrp', 'is_hrp', 'is_hrp_lad', 'is_lrp_lad', 'is_hrp_lcx', 'is_lrp_lcx', 'is_hrp_rca', 'is_lrp_rca', 'lumenareastenosis', 'plaquevolume_lesion', 'lesion_length', 'lumenvolume_lesion','lumenminimaldiameter']], how='left', on='lesion_id')
# pd_mmar['mass_mcp_perc'] = pd_mmar['mass_mcp_perc'] * \
#                             (pd_mmar['plaquevolume_lesion'] * pd_mmar['lesion_length'] * pd_mmar['lumenareastenosis']) / \
#                             (pd_mmar['lumenvolume_lesion'])

pd_mmar['is_hrp'] = pd_mmar['is_hrp'] & (pd_mmar['mass_mcp_perc'] > 12.5)
pd_mmar['is_hrp'] = pd_mmar['is_hrp'].astype('int16')
pd_mmar['is_lrp'] = np.where(pd_mmar['is_hrp'], 0, 1)
pd_mmar['is_lrp'] = pd_mmar['is_lrp'].astype('int16')

pd_mmar['is_hrp_lad'] = np.where(pd_mmar['is_hrp'] & (pd_mmar['mldlesion_arterial_dist'] == 'lad'), 1, 0)
pd_mmar['is_lrp_lad'] = np.where(pd_mmar['is_lrp'] & (pd_mmar['mldlesion_arterial_dist'] == 'lad'), 1, 0)

pd_mmar['is_hrp_lcx'] = np.where(pd_mmar['is_hrp'] & (pd_mmar['mldlesion_arterial_dist'] == 'lcx'), 1, 0)
pd_mmar['is_lrp_lcx'] = np.where(pd_mmar['is_lrp'] & (pd_mmar['mldlesion_arterial_dist'] == 'lcx'), 1, 0)

pd_mmar['is_hrp_rca'] = np.where(pd_mmar['is_hrp'] & (pd_mmar['mldlesion_arterial_dist'] == 'rca'), 1, 0)
pd_mmar['is_lrp_rca'] = np.where(pd_mmar['is_lrp'] & (pd_mmar['mldlesion_arterial_dist'] == 'rca'), 1, 0)

# In[ ] CONFIRM - FILTER FOR MATCHED CASES FOR CASE-CONTROL SETUP
df_match_id_count = pd.DataFrame()
df_match_id_count['confirm_idc'] = pd_mmar.confirm_idc.unique()
df_match_id_count = df_match_id_count.merge(pd_confirm[['confirm_idc', 'mi_match_id']], how='left', on='confirm_idc')
df_match_id_count = df_match_id_count.groupby(['mi_match_id'], as_index=False).agg('count')
df_match_id_count = df_match_id_count.loc[df_match_id_count['confirm_idc'] == 2]
df_match_confirm = pd_confirm['confirm_idc'].loc[pd_confirm['mi_match_id'].isin(df_match_id_count['mi_match_id'])]

# pd_mmar = pd_mmar.loc[pd_mmar['confirm_idc'].isin(df_match_confirm)] # TOGGLE TO FILTER FOR CASE-CONTROLLED PATIENTS

# In[ ] CONFIRM DATA - LESION DATA - ADD HRP/LRP MMAR
pd_mmar['mass_mcp_perc'] =  pd_mmar['mass_mcp_perc']
pd_mmar['mmar_hrp'] = np.where(pd_mmar['is_hrp'], pd_mmar['mass_mcp_perc'], 0)
pd_mmar['mmar_lrp'] = np.where(~(pd_mmar['is_hrp']), pd_mmar['mass_mcp_perc'], 0)

# In[ ] MMAR DATA - AGGREGATE
pd_mmar_max_hrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'max', '_hrp', 'mmar_hrp')
pd_mmar_min_hrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'min', '_hrp', 'mmar_hrp')
pd_mmar_mean_hrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'mean', '_hrp', 'mmar_hrp')
pd_mmar_sum_hrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'sum', '_hrp', 'mmar_hrp')
pd_mmar_count_hrp = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_hrp', criteria_col='is_hrp')

pd_mmar_max_lrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'max', '_lrp', 'mmar_lrp')
pd_mmar_min_lrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'min', '_lrp', 'mmar_lrp')
pd_mmar_mean_lrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'mean', '_lrp', 'mmar_lrp')
pd_mmar_sum_lrp = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'sum', '_lrp', 'mmar_lrp')
pd_mmar_count_lrp = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_lrp', criteria_col='is_lrp')

pd_mmar_max = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'max')
pd_mmar_min = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'min')
pd_mmar_mean = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'mean')
pd_mmar_sum = lib_prj.process.mmar_agg_per_patient(pd_mmar, 'sum')
pd_mmar_count = lib_prj.process.count_lesion_per_patient(pd_mmar, criteria_col='is_hrp')
pd_mmar_count['mmar_all'] = pd_mmar_count_hrp['mmar_all_hrp'] + pd_mmar_count_lrp['mmar_all_lrp']

# In[ ] LESION COUNT - PER VESSEL
pd_mmar_count_lad_hrp = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_hrp', criteria_col='is_hrp_lad')
pd_mmar_count_lad_lrp = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_lrp', criteria_col='is_lrp_lad')
pd_mmar_count_lad = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_hrp', criteria_col='is_hrp_lad')
pd_mmar_count_lad['mmar_all'] = pd_mmar_count_lad_hrp['mmar_all_hrp'] + pd_mmar_count_lad_lrp['mmar_all_lrp']

pd_mmar_count_lcx_hrp = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_hrp', criteria_col='is_hrp_lcx')
pd_mmar_count_lcx_lrp = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_lrp', criteria_col='is_lrp_lcx')
pd_mmar_count_lcx = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_hrp', criteria_col='is_hrp_lcx')
pd_mmar_count_lcx['mmar_all'] = pd_mmar_count_lcx_hrp['mmar_all_hrp'] + pd_mmar_count_lcx_lrp['mmar_all_lrp']

pd_mmar_count_rca_hrp = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_hrp', criteria_col='is_hrp_rca')
pd_mmar_count_rca_lrp = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_lrp', criteria_col='is_lrp_rca')
pd_mmar_count_rca = lib_prj.process.count_lesion_per_patient(pd_mmar, tag='_hrp', criteria_col='is_hrp_rca')
pd_mmar_count_rca['mmar_all'] = pd_mmar_count_rca_hrp['mmar_all_hrp'] + pd_mmar_count_rca_lrp['mmar_all_lrp']
                  
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
PD_COMBINED = PD_COMBINED.loc[~(PD_COMBINED['confirm_idc_str'].isna())]

PD_LESION = pd_lesion