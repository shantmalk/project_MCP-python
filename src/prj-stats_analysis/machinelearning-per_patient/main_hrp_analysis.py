# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 08:00:26 2020

@author: smalk
"""

import raw_data
import lib_prj.process as prc
import lib_prj.visualize as viz
import params
from plotly.offline import plot
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines import KaplanMeierFitter
from zepid import RiskRatio
from scipy.stats import norm
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.metrics import roc_auc_score

# In[1] Raw data
cols = params.COLUMNS
blacklist = params.BLACKLIST
outcome = 'macelr_event_confirm'

df = raw_data.PD_COMBINED
df_lesion = raw_data.PD_LESION

# In[3] ROC-AUC ANALYSIS - USING HRP MMAR ONLY
outcome = 'macelr_event_confirm'
figure_label = 'Per-Patient:  High-risk plaque features [Outcome = ' + outcome + ']'
labels = {'mmar_all_max' : 'MMAR<MAX>',
          'mmar_all_mean' : 'MMAR<MEAN>',
          'mmar_all_sum' : 'MMAR<SUM>',
          }
description = '''
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)

# In[3] DESCRIPTIVE ANALYSIS - USING ALL DATA
vessel = 'all'
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
    'y' : 'mmar_all_n',
    'points' : 'all',
    'labels' : {outcome : 'MACE'},
    'title' : title,
    }
fig = viz.boxplot_plotly(df, args_plotly, '')
fig.update_yaxes(title='MMAR<sub>N</sub>')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=title.replace(' ','_') + '.html')

# In[ ] DESCRIPTIVE ANALYSIS
mmar_hrp = raw_data.pd_mmar_mean_hrp[['confirm_idc', 'mmar_all_hrp', 'mmar_agg_type']].rename(columns={'mmar_all_hrp' : 'mmar'})
mmar_hrp['plaque_type'] = 'hrp'
mmar_lrp = raw_data.pd_mmar_mean_lrp[['confirm_idc', 'mmar_all_lrp', 'mmar_agg_type']].rename(columns={'mmar_all_lrp' : 'mmar'})
mmar_lrp['plaque_type'] = 'lrp'
mmar_total = raw_data.pd_mmar_mean[['confirm_idc', 'mmar_all', 'mmar_agg_type']].rename(columns={'mmar_all' : 'mmar'})
mmar_total['plaque_type'] = 'all'

df_descriptive = pd.concat([mmar_hrp, mmar_lrp, mmar_total])
df_descriptive = df_descriptive.merge(df[['confirm_idc', 'mi_event', 'mi_time']], how='left', on='confirm_idc')

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
mmar_hrp = raw_data.pd_mmar_sum_hrp[['confirm_idc', 'mmar_all_hrp', 'mmar_agg_type']].rename(columns={'mmar_all_hrp' : 'mmar'})
mmar_hrp['plaque_type'] = 'hrp'
mmar_lrp = raw_data.pd_mmar_sum_lrp[['confirm_idc', 'mmar_all_lrp', 'mmar_agg_type']].rename(columns={'mmar_all_lrp' : 'mmar'})
mmar_lrp['plaque_type'] = 'lrp'
mmar_all = raw_data.pd_mmar_sum[['confirm_idc', 'mmar_all', 'mmar_agg_type']].rename(columns={'mmar_all' : 'mmar'})
mmar_all['plaque_type'] = 'all'

df_descriptive = pd.concat([mmar_hrp, mmar_lrp, mmar_all])
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
mmar_hrp = raw_data.pd_mmar_max_hrp[['confirm_idc', 'mmar_all_hrp', 'mmar_agg_type']].rename(columns={'mmar_all_hrp' : 'mmar'})
mmar_hrp['plaque_type'] = 'hrp'
mmar_lrp = raw_data.pd_mmar_max_lrp[['confirm_idc', 'mmar_all_lrp', 'mmar_agg_type']].rename(columns={'mmar_all_lrp' : 'mmar'})
mmar_lrp['plaque_type'] = 'lrp'
mmar_all = raw_data.pd_mmar_max[['confirm_idc', 'mmar_all', 'mmar_agg_type']].rename(columns={'mmar_all' : 'mmar'})
mmar_all['plaque_type'] = 'all'

df_descriptive = pd.concat([mmar_hrp, mmar_lrp, mmar_all])
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
mmar_hrp = raw_data.pd_mmar_min_hrp[['confirm_idc', 'mmar_all_hrp', 'mmar_agg_type']].rename(columns={'mmar_all_hrp' : 'mmar'})
mmar_hrp['plaque_type'] = 'hrp'
mmar_lrp = raw_data.pd_mmar_min_lrp[['confirm_idc', 'mmar_all_lrp', 'mmar_agg_type']].rename(columns={'mmar_all_lrp' : 'mmar'})
mmar_lrp['plaque_type'] = 'lrp'
mmar_all = raw_data.pd_mmar_min[['confirm_idc', 'mmar_all', 'mmar_agg_type']].rename(columns={'mmar_all' : 'mmar'})
mmar_all['plaque_type'] = 'all'

df_descriptive = pd.concat([mmar_hrp, mmar_lrp, mmar_all])
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
df['is_n_hrp'] = df['mmar_all_n_hrp'] > 0
print(classification_report(df['macelr_event_confirm'], df['is_n_hrp']))

# In[6] HAZARD 
q_cutoff = .75

cutoff_thresh_mean = df['mmar_all_mean_hrp'].quantile([q_cutoff])[q_cutoff]
cutoff_thresh_max = df['mmar_all_max_hrp'].quantile([q_cutoff])[q_cutoff]
cutoff_thresh_sum = df['mmar_all_sum_hrp'].quantile([q_cutoff])[q_cutoff]

# ARBITRARY CUTOFFS - GIVES GOOD RESULTS FOR MMAR_HRP

# UPPER Q3
cutoff_thresh_mean = 25.16762 
cutoff_thresh_max = 39.17635
cutoff_thresh_sum = 41.98734

# MEDIAN
cutoff_thresh_mean = 8.092689 + cutoff_thresh_mean
cutoff_thresh_max = 19.71345 + cutoff_thresh_max
cutoff_thresh_sum = 19.71345 + cutoff_thresh_sum

cutoff_thresh_mean = 10
cutoff_thresh_max = 15
cutoff_thresh_sum = 15

print('========= HRP LESIONS =========')
plt.figure() 
df_dummy = pd.DataFrame()
df_dummy['outcome_event'] = df['mi_event']
df_dummy['outcome_time'] = df['mi_time']
df_dummy['mmar'] = df['mmar_all_mean_hrp']
df_dummy['hrp'] = df['mmar_all_n_hrp'].fillna(0)
df_dummy['SSS'] = df['segment_stenosis_score_confirm']
# df_dummy['bmi'] = df['bmi_confirm'].fillna(0)
# df_dummy['age'] = df['age_confirm'].fillna(0)
# df_dummy['sex'] = df['sex_confirm'].fillna(0)
# df_dummy['htn'] = df['htn_confirm'].fillna(0)
# df_dummy['dm'] = df['dm_confirm'].fillna(0)
# df_dummy['chol'] = df['chol_confirm'].fillna(0)
# df_dummy['mmar_max_hrp_cutoff'] = df['mmar_all_max_hrp'] > cutoff_thresh_max
# df_dummy['mmar_mean_hrp_cutoff'] = df['mmar_all_mean_hrp'] > cutoff_thresh_mean
# df_dummy['hrp'] = df['mmar_all_n_hrp'] > 
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

# In[ ] KMS ANALYSIS
q_cutoff = .75

cutoff_thresh_mean = df['mmar_all_mean_hrp'].quantile([q_cutoff])[q_cutoff]
cutoff_thresh_max = df['mmar_all_max_hrp'].quantile([q_cutoff])[q_cutoff]
cutoff_thresh_sum = df['mmar_all_sum_hrp'].quantile([q_cutoff])[q_cutoff]

print('========= HRP LESIONS =========')
plt.figure() 
df_dummy = pd.DataFrame()
df_dummy['outcome_event'] = df['mi_event']
df_dummy['outcome_time'] = df['mi_time']
df_dummy['mmar_hrp_cutoff'] = df['mmar_all_max_hrp'] > cutoff_thresh_max

kmf = KaplanMeierFitter()
i1 = df_dummy['mmar_hrp_cutoff'] == True
i2 = df_dummy['mmar_hrp_cutoff'] == False
kmf.fit(durations = df_dummy['outcome_time'][i1], event_observed = df_dummy['outcome_event'][i1], label = 'MMAR > CUTOFF')
a1 = kmf.plot()
kmf.fit(df_dummy['outcome_time'][i2], df_dummy['outcome_event'][i2], label = 'MMAR < CUTOFF')
kmf.plot(ax=a1)

# In[ ] Relative Risk - HRP
q_cutoff = .75

cutoff_thresh_mean = df['mmar_all_mean_hrp'].quantile([q_cutoff])[q_cutoff]
cutoff_thresh_max = df['mmar_all_max_hrp'].quantile([q_cutoff])[q_cutoff]
cutoff_thresh_sum = df['mmar_all_sum_hrp'].quantile([q_cutoff])[q_cutoff]




# calculating risk ratio
exp = 'mmar_mean_cutoff'
cutoff = cutoff_thresh_mean

df['mmar_mean_cutoff'] = df['mmar_all_mean_hrp'] > cutoff_thresh_mean
df['mmar_sum_cutoff'] = df['mmar_all_sum_hrp'] > cutoff_thresh_sum
df['mmar_max_cutoff'] = df['mmar_all_max_hrp'] > cutoff_thresh_max

rr = RiskRatio()
rr.fit(df, exposure=exp, outcome='mi_event')

# calculating p-value
est= rr.results['RiskRatio'][1]
std = rr.results['SD(RR)'][1]
z_score = np.log(est)/std
p_value = norm.sf(abs(z_score))*2

print('Exposure: {exp}'.format(exp=exp))
print('Cutoff: {cutoff:0.2f}'.format(cutoff=cutoff))
print('Relative Risk: {rr:0.2f}±{std:0.2f} (p-value {pval:0.2f})'.format(rr=est, std=std, pval=p_value))

# In[ ] Relative Risk
q_cutoff = .75
outcome = 'mi_event'
df['mmar_mean_cutoff_lrp'] = df['mmar_all_mean_lrp'] > df['mmar_all_mean_lrp'].quantile([q_cutoff])[q_cutoff]
df['mmar_sum_cutoff_lrp'] = df['mmar_all_sum_lrp'] > df['mmar_all_sum_lrp'].quantile([q_cutoff])[q_cutoff]
df['mmar_max_cutoff_lrp'] = df['mmar_all_max_lrp'] > df['mmar_all_max_lrp'].quantile([q_cutoff])[q_cutoff]

df['mmar_mean_cutoff_hrp'] = df['mmar_all_mean_hrp'] > df['mmar_all_mean_hrp'].quantile([q_cutoff])[q_cutoff]
df['mmar_sum_cutoff_hrp'] = df['mmar_all_sum_hrp'] > df['mmar_all_sum_hrp'].quantile([q_cutoff])[q_cutoff]
df['mmar_max_cutoff_hrp'] = df['mmar_all_max_hrp'] > df['mmar_all_max_hrp'].quantile([q_cutoff])[q_cutoff]

df_relative_risk = pd.DataFrame(columns=['lbl', 'rr', 'std', 'pval'])
df_relative_risk = df_relative_risk.append(pd.Series(prc.relative_risk(df, 'mmar_mean_cutoff_lrp', outcome), index=df_relative_risk.columns), ignore_index=True)
df_relative_risk = df_relative_risk.append(pd.Series(prc.relative_risk(df, 'mmar_sum_cutoff_lrp', outcome), index=df_relative_risk.columns), ignore_index=True)
df_relative_risk = df_relative_risk.append(pd.Series(prc.relative_risk(df, 'mmar_max_cutoff_lrp', outcome), index=df_relative_risk.columns), ignore_index=True)

df_relative_risk = df_relative_risk.append(pd.Series(prc.relative_risk(df, 'mmar_mean_cutoff_hrp', outcome), index=df_relative_risk.columns), ignore_index=True)
df_relative_risk = df_relative_risk.append(pd.Series(prc.relative_risk(df, 'mmar_sum_cutoff_hrp', outcome), index=df_relative_risk.columns), ignore_index=True)
df_relative_risk = df_relative_risk.append(pd.Series(prc.relative_risk(df, 'mmar_max_cutoff_hrp', outcome), index=df_relative_risk.columns), ignore_index=True)

viz.rr_boxplot(df_relative_risk)

# In[ ] Odds Ratio
df_odds_ratio = pd.DataFrame(columns=['lbl', 'or', 'pval'])

q_cutoff = .75
outcome = 'mi_event'

exp = 'mmar_mean_cutoff_hrp'
df_crosstab = pd.crosstab(df[exp], df['mi_event'])
df_odds_ratio = df_odds_ratio.append(pd.Series([exp, stats.fisher_exact(df_crosstab)[0], stats.fisher_exact(df_crosstab)[1] ], index=df_odds_ratio.columns), ignore_index=True)

exp = 'mmar_max_cutoff_hrp'
df_crosstab = pd.crosstab(df[exp], df['mi_event'])
df_odds_ratio = df_odds_ratio.append(pd.Series([exp, stats.fisher_exact(df_crosstab)[0], stats.fisher_exact(df_crosstab)[1] ], index=df_odds_ratio.columns), ignore_index=True)

exp = 'mmar_sum_cutoff_hrp'
df_crosstab = pd.crosstab(df[exp], df['mi_event'])
df_odds_ratio = df_odds_ratio.append(pd.Series([exp, stats.fisher_exact(df_crosstab)[0], stats.fisher_exact(df_crosstab)[1] ], index=df_odds_ratio.columns), ignore_index=True)

exp = 'mmar_mean_cutoff_lrp'
df_crosstab = pd.crosstab(df[exp], df['mi_event'])
df_odds_ratio = df_odds_ratio.append(pd.Series([exp, stats.fisher_exact(df_crosstab)[0], stats.fisher_exact(df_crosstab)[1] ], index=df_odds_ratio.columns), ignore_index=True)

exp = 'mmar_max_cutoff_lrp'
df_crosstab = pd.crosstab(df[exp], df['mi_event'])
df_odds_ratio = df_odds_ratio.append(pd.Series([exp, stats.fisher_exact(df_crosstab)[0], stats.fisher_exact(df_crosstab)[1] ], index=df_odds_ratio.columns), ignore_index=True)

exp = 'mmar_sum_cutoff_lrp'
df_crosstab = pd.crosstab(df[exp], df['mi_event'])
df_odds_ratio = df_odds_ratio.append(pd.Series([exp, stats.fisher_exact(df_crosstab)[0], stats.fisher_exact(df_crosstab)[1] ], index=df_odds_ratio.columns), ignore_index=True)

viz.table_basic(df_odds_ratio)

# In[ ] AUC Analysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score
xx = df['mmar_all_mean_hrp']
X = df['mmar_mean_cutoff_hrp']
y = df['mi_event']

# print(roc_auc_score(y, X))
# print(roc_auc_score(df['mi_event'], df['mmar_all_mean_hrp']))

print(precision_score(y, X, average='macro'))

