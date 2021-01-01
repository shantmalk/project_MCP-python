# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 08:00:26 2020

@author: smalk
"""

import ml_raw_data
import lib_prj.process as prc
import lib_prj.visualize as viz
import params
from plotly.offline import plot
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pandas as pd
from lifelines import CoxPHFitter
import matplotlib.pyplot as plt

# In[1] Raw data
cols = params.COLUMNS
blacklist = params.BLACKLIST
outcome = 'macelr_event_confirm'

df = ml_raw_data.PD_COMBINED
df_lesion = ml_raw_data.PD_LESION

# In[2] Clean data
# updated_cols = prc.clean_df(df.reset_index(), cols, blacklist)

# In[3] ROC-AUC ANALYSIS - USING HRP MMAR ONLY
outcome = 'macelr_event_confirm'
figure_label = 'Per-Patient:  High-risk plaque features [Outcome = ' + outcome + ']'
labels = {'mmar_total_max' : 'MMAR<MAX>',
          'mmar_total_mean' : 'MMAR<MEAN>',
          'mmar_total_sum' : 'MMAR<SUM>',
          # 'mmar_total_mean' : 'MMAR<sub>MEAN</sub>',
          }
description = '''
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)

# In[3] DESCRIPTIVE ANALYSIS - USING ALL DATA
outcome = 'mi_event'
figure_label = 'Per-Patient:  High-risk plaque features [Outcome = ' + outcome + ']'
labels = {'mmar_total_max' : 'MMAR<MAX>',
          'mmar_total_mean' : 'MMAR<MEAN>',
          'mmar_total_sum' : 'MMAR<SUM>',
          'mmar_total_max_hrp' : 'MMAR<HRP_MAX>',
          'mmar_total_mean_hrp' : 'MMAR<HRP_MEAN>',
          'mmar_total_sum_hrp' : 'MMAR<HRP_SUM>',
          'mmar_total_max_lrp' : 'MMAR<LRP_MAX>',
          'mmar_total_mean_lrp' : 'MMAR<LRP_MEAN>',
          'mmar_total_sum_lrp' : 'MMAR<LRP_SUM>',
          }
description = '''
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)

# In[3] DESCRIPTIVE ANALYSIS - USING ALL DATA
vessel = 'total'
outcome = 'mi_event'
figure_label = 'Per-Patient:  High-risk plaque features [Outcome = ' + outcome + ']' + ' VESSEL: ' + vessel
labels = {'mmar_' + vessel + '_max' : 'MMAR<MAX>',
          'mmar_' + vessel + '_mean' : 'MMAR<MEAN>',
          'mmar_' + vessel + '_sum' : 'MMAR<SUM>',
          'mmar_' + vessel + '_max_hrp' : 'MMAR<HRP_MAX>',
          'mmar_' + vessel + '_mean_hrp' : 'MMAR<HRP_MEAN>',
          'mmar_' + vessel + '_sum_hrp' : 'MMAR<HRP_SUM>',
          'mmar_' + vessel + '_max_lrp' : 'MMAR<LRP_MAX>',
          'mmar_' + vessel + '_mean_lrp' : 'MMAR<LRP_MEAN>',
          'mmar_' + vessel + '_sum_lrp' : 'MMAR<LRP_SUM>',
          }
description = '''
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)


# In[3] DESCRIPTIVE ANALYSIS - USING ALL DATA
title=''
args_plotly = {
    'x' : outcome,
    'y' : 'mmar_total_n',
    'points' : 'all',
    'labels' : {outcome : 'MACE'},
    'title' : title,
    }
fig = viz.boxplot_plotly(df, args_plotly, '')
fig.update_yaxes(title='MMAR<sub>N</sub>')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=title.replace(' ','_') + '.html')


# In[ ]
outcome='mi_event'
vessel = 'lad'
mmar_hrp = ml_raw_data.pd_mmar_mean_hrp[['confirm_idc', 'mmar_' + vessel + '_hrp', 'mmar_agg_type']].rename(columns={'mmar_' + vessel + '_hrp' : 'mmar'})
mmar_hrp['plaque_type'] = 'hrp'
mmar_lrp = ml_raw_data.pd_mmar_mean_lrp[['confirm_idc', 'mmar_' + vessel + '_lrp', 'mmar_agg_type']].rename(columns={'mmar_' + vessel + '_lrp' : 'mmar'})
mmar_lrp['plaque_type'] = 'lrp'
mmar_total = ml_raw_data.pd_mmar_mean[['confirm_idc', 'mmar_' + vessel, 'mmar_agg_type']].rename(columns={'mmar_' + vessel : 'mmar'})
mmar_total['plaque_type'] = 'all'

df_descriptive = pd.concat([mmar_hrp, mmar_lrp, mmar_total])
df_descriptive = df_descriptive.merge(df[['confirm_idc', 'mi_event', 'mi_time']], how='left', on='confirm_idc')

title='Per-Patient: MMAR<sub>MEAN</sub> based on plaque type'
fname = 'per_patient_mmar_mean_plaquetype'
# args_plotly = {
#     'x' : outcome,
#     'y' : 'mmar',
#     'points' : 'all',
#     'color' : 'plaque_type',
#     'title' : title,
#     }
# fig = viz.boxplot_plotly(df_descriptive, args_plotly, '')
# fig.update_yaxes(title='MMAR<sub>MEAN</sub>')
# fig.update_xaxes(title='')
# plot_url = plot(fig, filename=fname + '.html')

title='Per-Patient: MMAR<sub>MEAN</sub> based on plaque type'
fname = 'per_patient_mmar_mean_plaquetype'
args_plotly = {
    'x' : 'plaque_type',
    'y' : 'mmar',
    'points' : 'all',
    'color' : outcome,
    'title' : title,
    }
fig = viz.boxplot_plotly(df_descriptive, args_plotly, '')
fig.update_yaxes(title='MMAR<sub>MEAN</sub>')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=fname + '.html')


# In[ ] DESCRIPTIVE ANALYSIS
mmar_hrp = ml_raw_data.pd_mmar_mean_hrp[['confirm_idc', 'mmar_total_hrp', 'mmar_agg_type']].rename(columns={'mmar_total_hrp' : 'mmar'})
mmar_hrp['plaque_type'] = 'hrp'
mmar_lrp = ml_raw_data.pd_mmar_mean_lrp[['confirm_idc', 'mmar_total_lrp', 'mmar_agg_type']].rename(columns={'mmar_total_lrp' : 'mmar'})
mmar_lrp['plaque_type'] = 'lrp'
mmar_total = ml_raw_data.pd_mmar_mean[['confirm_idc', 'mmar_total', 'mmar_agg_type']].rename(columns={'mmar_total' : 'mmar'})
mmar_total['plaque_type'] = 'all'

df_descriptive = pd.concat([mmar_hrp, mmar_lrp, mmar_total])
df_descriptive = df_descriptive.merge(df[['confirm_idc', 'mi_event', 'mi_time']], how='left', on='confirm_idc')

title='Per-Patient: MMAR<sub>MEAN</sub> based on plaque type'
fname = 'per_patient_mmar_mean_plaquetype'
# args_plotly = {
#     'x' : outcome,
#     'y' : 'mmar',
#     'points' : 'all',
#     'color' : 'plaque_type',
#     'title' : title,
#     }
# fig = viz.boxplot_plotly(df_descriptive, args_plotly, '')
# fig.update_yaxes(title='MMAR<sub>MEAN</sub>')
# fig.update_xaxes(title='')
# plot_url = plot(fig, filename=fname + '.html')

title='Per-Patient: MMAR<sub>MEAN</sub> based on plaque type'
fname = 'per_patient_mmar_mean_plaquetype'
args_plotly = {
    'x' : 'plaque_type',
    'y' : 'mmar',
    'points' : 'all',
    'color' : outcome,
    'title' : title,
    }
fig = viz.boxplot_plotly(df_descriptive, args_plotly, '')
fig.update_yaxes(title='MMAR<sub>MEAN</sub>')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=fname + '.html')

# In[ ]
mmar_hrp = ml_raw_data.pd_mmar_sum_hrp[['confirm_idc', 'mmar_total_hrp', 'mmar_agg_type']].rename(columns={'mmar_total_hrp' : 'mmar'})
mmar_hrp['plaque_type'] = 'hrp'
mmar_lrp = ml_raw_data.pd_mmar_sum_lrp[['confirm_idc', 'mmar_total_lrp', 'mmar_agg_type']].rename(columns={'mmar_total_lrp' : 'mmar'})
mmar_lrp['plaque_type'] = 'lrp'
mmar_total = ml_raw_data.pd_mmar_sum[['confirm_idc', 'mmar_total', 'mmar_agg_type']].rename(columns={'mmar_total' : 'mmar'})
mmar_total['plaque_type'] = 'all'

df_descriptive = pd.concat([mmar_hrp, mmar_lrp, mmar_total])
df_descriptive = df_descriptive.merge(df[['confirm_idc', 'mi_event', 'mi_time']], how='left', on='confirm_idc')

title='Per-Patient: MMAR<sub>SUM</sub> based on plaque type'
fname = 'per_patient_mmar_sum_plaquetype'
args_plotly = {
    'x' : 'plaque_type',
    'y' : 'mmar',
    'points' : 'all',
    'color' : outcome,
    'title' : title,
    }
fig = viz.boxplot_plotly(df_descriptive, args_plotly, '')
fig.update_yaxes(title='MMAR<sub>SUM</sub>')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=fname + '.html')

# In[ ]
mmar_hrp = ml_raw_data.pd_mmar_max_hrp[['confirm_idc', 'mmar_total_hrp', 'mmar_agg_type']].rename(columns={'mmar_total_hrp' : 'mmar'})
mmar_hrp['plaque_type'] = 'hrp'
mmar_lrp = ml_raw_data.pd_mmar_max_lrp[['confirm_idc', 'mmar_total_lrp', 'mmar_agg_type']].rename(columns={'mmar_total_lrp' : 'mmar'})
mmar_lrp['plaque_type'] = 'lrp'
mmar_total = ml_raw_data.pd_mmar_max[['confirm_idc', 'mmar_total', 'mmar_agg_type']].rename(columns={'mmar_total' : 'mmar'})
mmar_total['plaque_type'] = 'all'

df_descriptive = pd.concat([mmar_hrp, mmar_lrp, mmar_total])
df_descriptive = df_descriptive.merge(df[['confirm_idc', 'mi_event', 'mi_time']], how='left', on='confirm_idc')

title='Per-Patient: MMAR<sub>MAX</sub> based on plaque type'
fname = 'per_patient_mmar_max_plaquetype'
args_plotly = {
    'x' : 'plaque_type',
    'y' : 'mmar',
    'points' : 'all',
    'color' : outcome,
    'title' : title,
    }
fig = viz.boxplot_plotly(df_descriptive, args_plotly, '')
fig.update_yaxes(title='MMAR<sub>MAX</sub>')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=fname + '.html')

# In[ ]
mmar_hrp = ml_raw_data.pd_mmar_min_hrp[['confirm_idc', 'mmar_total_hrp', 'mmar_agg_type']].rename(columns={'mmar_total_hrp' : 'mmar'})
mmar_hrp['plaque_type'] = 'hrp'
mmar_lrp = ml_raw_data.pd_mmar_min_lrp[['confirm_idc', 'mmar_total_lrp', 'mmar_agg_type']].rename(columns={'mmar_total_lrp' : 'mmar'})
mmar_lrp['plaque_type'] = 'lrp'
mmar_total = ml_raw_data.pd_mmar_min[['confirm_idc', 'mmar_total', 'mmar_agg_type']].rename(columns={'mmar_total' : 'mmar'})
mmar_total['plaque_type'] = 'all'

df_descriptive = pd.concat([mmar_hrp, mmar_lrp, mmar_total])
df_descriptive = df_descriptive.merge(df[['confirm_idc', 'mi_event', 'mi_time']], how='left', on='confirm_idc')

title='Per-Patient: MMAR<sub>MIN</sub> based on plaque type'
fname = 'per_patient_mmar_min_plaquetype'
args_plotly = {
    'x' : 'plaque_type',
    'y' : 'mmar',
    'points' : 'all',
    'color' : outcome,
    'title' : title,
    }
fig = viz.boxplot_plotly(df_descriptive, args_plotly, '')
fig.update_yaxes(title='MMAR<sub>MIN</sub>')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=fname + '.html')

# In[4] CONFUSION MATRIX
# (tn, fp, fn, tp)
(tn, fp, fn, tp) = confusion_matrix(df_lesion['lesion_culprit_ica_ct'], df_lesion['is_hrp']).ravel()

# In[5] CLASSIFICATION REPORT
print(classification_report(df_lesion['lesion_culprit_ica_ct'], df_lesion['is_hrp']))
df['is_n_hrp'] = df['mmar_total_n'] > 3
print(classification_report(df['macelr_event_confirm'], df['is_n_hrp']))

# In[6] HAZARD 

# ARBITRARY CUTOFFS - GIVES GOOD RESULTS FOR MMAR_HRP

# UPPER Q3
cutoff_thresh_mean = 25.16762 
cutoff_thresh_max = 39.17635
cutoff_thresh_sum = 41.98734

# MEDIAN
cutoff_thresh_mean = 8.092689 + cutoff_thresh_mean
cutoff_thresh_max = 19.71345 + cutoff_thresh_max
cutoff_thresh_sum = 19.71345 + cutoff_thresh_sum

cutoff_thresh_mean = 25
cutoff_thresh_max = 60
cutoff_thresh_sum = 60

print('========= HRP LESIONS =========')
plt.figure() 
df_dummy = pd.DataFrame()
df_dummy['outcome_event'] = df['mi_event']
df_dummy['outcome_time'] = df['mi_time']
df_dummy['mmar_sum_hrp_cutoff'] = df['mmar_total_sum_hrp'] > cutoff_thresh_sum
df_dummy['mmar_max_hrp_cutoff'] = df['mmar_total_max_hrp'] > cutoff_thresh_max
df_dummy['mmar_mean_hrp_cutoff'] = df['mmar_total_mean_hrp'] > cutoff_thresh_mean
cph = CoxPHFitter()
cph.fit(df_dummy, 'outcome_time', event_col='outcome_event')
cph.print_summary()
cph.plot()

# print('========= LRP LESIONS =========')
# plt.figure()
# df_dummy = pd.DataFrame()
# df_dummy['outcome_event'] = df['mi_event']
# df_dummy['outcome_time'] = df['mi_time']
# df_dummy['mmar_sum_lrp_cutoff'] = df['mmar_total_sum_lrp'] > cutoff_thresh_sum
# df_dummy['mmar_max_lrp_cutoff'] = df['mmar_total_max_lrp'] > cutoff_thresh_max
# df_dummy['mmar_mean_lrp_cutoff'] = df['mmar_total_mean_lrp'] > cutoff_thresh_mean
# cph = CoxPHFitter()
# cph.fit(df_dummy, 'outcome_time', event_col='outcome_event')
# cph.print_summary()
# cph.plot()

# print('========= ALL LESIONS =========')
# plt.figure()
# df_dummy = pd.DataFrame()
# df_dummy['outcome_event'] = df['mi_event']
# df_dummy['outcome_time'] = df['mi_time']
# df_dummy['mmar_sum_cutoff'] = df['mmar_total_sum'] > cutoff_thresh_sum
# df_dummy['mmar_max_cutoff'] = df['mmar_total_max'] > cutoff_thresh_max
# df_dummy['mmar_mean_cutoff'] = df['mmar_total_mean'] > cutoff_thresh_mean
# cph = CoxPHFitter()
# cph.fit(df_dummy, 'outcome_time', event_col='outcome_event')
# cph.print_summary()
# cph.plot()




