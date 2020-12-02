# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 18:54:45 2020

@author: smalk

REFERENCES:  
    https://datagraphi.com/blog/post/2019/9/23/feature-selection-with-sklearn-in-python
    https://pubmed.ncbi.nlm.nih.gov/27252451/
"""

import ml_raw_data
import pandas as pd
from plotly.offline import plot
from plotly.express import bar
import lib_prj
from sklearn.feature_selection import VarianceThreshold
from scipy.stats import entropy

def view_features_variance(df:'pd.DataFrame', ft, title):
    args_plotly = {
    'y' : 'index',
    'x' : ft,
    }
    y_label = 'Information Gain - ' + args_plotly['x']
    figure_fname_label = title.lower().replace(' ', '')
    args_plotly['title'] = title
    fig = bar(df, **args_plotly)
    fig.update_yaxes(title=y_label)
    fig.update_xaxes(title='')
    plot_url = plot(fig, filename=title.replace(' ','_') + '.html')

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

def information_gain_df(df, col_select, split):
    features = pd.DataFrame(columns=['index', split])
    for ii in range(len(col_select)):
        features = features.append({'index' : col_select[ii], split : information_gain(df[col_select[ii]], df[split])}, ignore_index=True)
    return features.sort_values(by=[split])


# In[ ]
df = ml_raw_data.PD_COMBINED
cols = [
        'mmar_lad_max',
        'mmar_lcx_max',
        'mmar_rca_max',
        'mmar_total_max',
        'mmar_lad_min',
        'mmar_lcx_min',
        'mmar_rca_min',
        'mmar_total_min',
        'mmar_lad_mean',
        'mmar_lcx_mean',
        'mmar_rca_mean',
        'mmar_total_mean',
        'mmar_lad_sum',
        'mmar_lcx_sum',
        'mmar_rca_sum',
        'mmar_total_sum',
        'age_confirm',
        'sex_confirm',
        'bmi_confirm',
        'height_confirm',
        'weight_confirm',
        'htn_confirm',
        'dm_confirm',
        'chol_confirm',
        'total_cholesterol_confirm',
        'ldl_confirm',
        'hdl_confirm',
        'famhx_confirm',
        'smokecurrent_confirm',
        'smokepast_confirm',
        'renal_insufficiency_confirm',
        'creatinine_confirm',
        'pv_disease_confirm',
        'cv_disease_confirm',
        'chest_pain_confirm',
        'exertion_confirm',
        'relief_confirm',
        'typicality_confirm',
        'sob_confirm',
        'acs_confirm',
        'cacscateg400_confirm',
        'cacscateg1000_confirm',
        'calciumscore_confirm',
        'lm_severity_confirm',
        'lm_composition_confirm',
        'plad_severity_confirm',
        'plad_composition_confirm',
        'mlad_severity_confirm',
        'mlad_composition_confirm',
        'dlad_severity_confirm',
        'dlad_composition_confirm',
        'diag1_severity_confirm',
        'diag1_composition_confirm',
        'diag2_severity_confirm',
        'diag2_composition_confirm',
        'plcx_severity_confirm',
        'plcx_composition_confirm',
        'dlcx_severity_confirm',
        'dlcx_composition_confirm',
        'om1_severity_confirm',
        'om1_composition_confirm',
        'om2_severity_confirm',
        'om2_composition_confirm',
        'leftpl_severity_confirm',
        'leftpl_composition_confirm',
        'prca_severity_confirm',
        'prca_composition_confirm',
        'mrca_severity_confirm',
        'mrca_composition_confirm',
        'drca_severity_confirm',
        'drca_composition_confirm',
        'pda_severity_confirm',
        'pda_composition_confirm',
        'rightpl_severity_confirm',
        'rightpl_composition_confirm',
        'pl_severity_confirm',
        'pl_composition_confirm',
        'rpda_severity_confirm',
        'rpda_composition_confirm',
        'lpda_severity_confirm',
        'lpda_composition_confirm',
        'ramus_severity_confirm',
        'ramus_composition_confirm',
        'anomalous_confirm',
        'rightdominant_confirm',
        'low_ef_confirm',
        'efinpercent_confirm',
        'lvedv_confirm',
        'lvesv_confirm',
        'rwma_confirm',
        'ef_by_other_modality_confirm',
        'nitroglycerin_confirm',
        'contrast_amount_confirm',
        'scan_type_confirm',
        'ct_scan_type_confirm',
        'ma_confirm',
        'kv_confirm',
        'dlp_ccta_confirm',
        'dlp_total_confirm',
        'study_quality_confirm',
        'acei_confirm',
        'asa_confirm',
        'at2_antagonist_confirm',
        'bb_confirm',
        'ca_blocker_confirm',
        'diuretics_confirm',
        'coumadin_confirm',
        'hypoglycemics_confirm',
        'metformin_confirm',
        'insulin_confirm',
        'lipid_lowering_confirm',
        'statin_confirm',
        'nitrates_confirm',
        'clopidogrel_confirm',
        'death_confirm',
        'time_followup_confirm',
        'obstructive_cad_confirm',
        'cad_or_revasc_confirm',
        'obstructive_cad_70_confirm',
        'num_vessel_disease_confirm',
        'lost_followup_confirm',
        'calcified_only_confirm',
        'mixed_only_confirm',
        'non_calcified_only_confirm',
        'num_calc_segs_confirm',
        'num_mixed_segs_confirm',
        'num_noncalc_segs_confirm',
        'df_probability_confirm',
        'lm_stenosis_confirm',
        'plad_stenosis_confirm',
        'mlad_stenosis_confirm',
        'dlad_stenosis_confirm',
        'diag1_stenosis_confirm',
        'diag2_stenosis_confirm',
        'plcx_stenosis_confirm',
        'dlcx_stenosis_confirm',
        'om1_stenosis_confirm',
        'om2_stenosis_confirm',
        'leftpl_stenosis_confirm',
        'prca_stenosis_confirm',
        'mrca_stenosis_confirm',
        'drca_stenosis_confirm',
        'pda_stenosis_confirm',
        'rightpl_stenosis_confirm',
        'pl_stenosis_confirm',
        'rpda_stenosis_confirm',
        'lpda_stenosis_confirm',
        'ramus_stenosis_confirm',
        'stenosis_50_confirm',
        'stenosis_70_confirm',
        'any_lm_stenosis_confirm',
        'duke_cad_confirm',
        'segment_stenosis_score_confirm',
        'segment_involvement_score_confir',
        'num_vessel_plaque_confirm',
        'num_vessel_mod_confirm',
        'num_vessel_severe_confirm',
        'fram_risk_confirm',
        'morisescore_confirm',
        'duke_jeopardy_confirm',
        'max_stenosis_confirm',
        'fu_time_confirm',
        'acm_time_confirm',
        'mace_event_confirm',
        'mace_time_confirm',
        'mi_time',
        'fu_ptca_confirm',
        'ptca_time_confirm',
        'ptca90_confirm',
        'fu_cabg_confirm',
        'cabg_time_confirm',
        'cabg90_confirm',
        'revasc_event_confirm',
        'revasc_time_confirm',
        'er_90_confirm',
        'late_revasc_event_confirm',
        'late_revasc_time_confirm',
        'macelr_event_confirm',
        'macelr_time_confirm',
        'lm_50_confirm',
        'lad_50_confirm',
        'lcx_50_confirm',
        'rca_50_confirm',
        'interval_revasc',
        'cad_severity',
        'propscore',
        'propscore_nocad',
        'propscore_nodm',
        'propscore_nohtn',
        'propscore_nochol',
        'propscore_nosm',
        'propscore_nofam',
        'propscore_nofamsm',
        'propscore_nofamhtn',
        'propscore_nofamchol',
        'propscore_norf',
        'propscore_good',
        ] 

# In[ ] FILTER COLUMNS - If majority of values is None, remove

updated_cols = cols.copy()
for ii in range(len(cols)):
    cur_count = (len(df[cols[ii]]) - df[cols[ii]].count()) / len(df[cols[ii]])
    if cur_count > 0:
        updated_cols.remove(cols[ii])
    
    # if 'mmar' in cols[ii]:
    #     updated_cols.remove(cols[ii])
        
# THESE ARE THE SAME AS MI_EVENT - REMOVE THEM FROM MODEL
# BLACKLIST:
# updated_cols.remove('mi_event')
updated_cols.remove('mace_event_confirm')
updated_cols.remove('mace_time_confirm')
updated_cols.remove('mi_time')
updated_cols.remove('macelr_time_confirm')
updated_cols.remove('macelr_event_confirm')
updated_cols.remove('death_confirm')
updated_cols.remove('acm_time_confirm')
updated_cols.remove('propscore_good')
updated_cols.remove('propscore_norf')


cols = updated_cols.copy()

X = df[cols]
Y = df['mi_event']


# In[ ] METHOD 1 - CALCULATE VARIANCE BETWEEN GROUPS
# var = VarianceThreshold(threshold=0.3)
# var = var.fit(X,Y)

# # In[ ]
# cols = var.get_support(indices=True)
# cor = df.corr()
# # In[ ] VISUALIZE
# import seaborn as sns
# import matplotlib.pyplot as plt
# plt.figure(figsize=(50,50))
# sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
# plt.show()

# # In[ ]
# cor_target = cor['mi_event']
# cor_target['mi_event'] = -1
# features = cor_target[cor_target>0]
# view_features_variance(features.reset_index().sort_values(by=['mi_event']), '')
# selected_feats = features.index

# In[ ] INFORMATION-GAIN METHOD (SAME AS UCLA GROUP)

# members = df['rightpl_composition_confirm']
# # members = df['mmar_rca_max']
# split = df['mi_event']
# result = information_gain(members, split)
# print (result)

# In[ ] INFORMATION-GAIN METHOD (SAME AS UCLA GROUP)
# Most robust method
# Similarities with previous UCLA study, but note the outcome in this code is MI event, the outcome in the UCLA study was all-cause mortality
OUTCOME = 'mace_event_confirm'
ft = information_gain_df(df, cols, OUTCOME)
ft = ft[ft[OUTCOME] > 0 ]
# view_features_variance(ft, '') # VISUALIZE
FEATURES = ft