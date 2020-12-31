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

# In[1] Raw data
cols = params.COLUMNS
blacklist = params.BLACKLIST
outcome = 'macelr_event_confirm'

df = ml_raw_data.PD_COMBINED
df_lesion = ml_raw_data.PD_LESION

# In[2] Clean data
updated_cols = prc.clean_df(df, cols, blacklist)

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
          # 'mmar_total_mean' : 'MMAR<sub>MEAN</sub>',
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

# In[4] CONFUSION MATRIX
# (tn, fp, fn, tp)
(tn, fp, fn, tp) = confusion_matrix(df_lesion['lesion_culprit_ica_ct'], df_lesion['is_hrp']).ravel()

# In[5] CLASSIFICATION REPORT
print(classification_report(df_lesion['lesion_culprit_ica_ct'], df_lesion['is_hrp']))
df['is_n_hrp'] = df['mmar_total_n'] > 3
print(classification_report(df['macelr_event_confirm'], df['is_n_hrp']))

# In[6] HAZARD RATIO
df_dummy = pd.DataFrame()
df_dummy['outcome_event'] = df['mi_event']
df_dummy['outcome_time'] = df['mi_time']
df_dummy['mmar_sum_cutoff'] = df['mmar_total_sum'] > 50
df_dummy['mmar_max_cutoff'] = df['mmar_total_max'] > 50
df_dummy['mmar_mean_cutoff'] = df['mmar_total_mean'] > 20
# df_dummy['is_n_hrp'] = df['is_n_hrp']

cph = CoxPHFitter()
cph.fit(df_dummy, 'outcome_time', event_col='outcome_event')
cph.print_summary()
cph.plot()