# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 21:36:04 2020

@author: smalk
"""


# In[0] Import
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import metrics
from numpy import mean
from numpy import std
from sklearn.metrics import brier_score_loss
import scipy.stats as stats


import lib_prj.process as prc
import lib_prj.visualize as viz
import params
import ml_raw_data

# In[1] Raw data
cols = params.COLUMNS
blacklist = params.BLACKLIST
outcome = 'macelr_event_confirm'

df = ml_raw_data.PD_COMBINED

# In[2] Clean data
updated_cols = prc.clean_df(df, cols, blacklist)

# In[3] Feature selection
ft = prc.information_gain_df(df, updated_cols, outcome)
ft = ft[ft['entropy'] > 0]
# prc.view_features_variance(ft, 'FEATURE SELECTION - ' + outcome)


# In[4] Build model - split data into testing and training sets
stat_method = 'OddsRatio'



table = df.groupby(outcome).sum().values
oddsratio, pvalue = stats.fisher_exact(table)

# In[6] Build model - view metrics of algorithm

# METRICS OF ASSESSMENT:
metric_str = '{METHOD:<10} | {METRIC:<15} | {VAL:.3f}'

print(metric_str.format(METHOD=stat_method, METRIC='ODDSRATIO', VAL=oddsratio))
print(metric_str.format(METHOD=stat_method, METRIC='PVALUE', VAL=pvalue))


# In[7] Build model - view ROC

df_test = testing.copy()

df_test['ml_output'] = model.predict_proba(df_test[ft['feature']])[:, 1]
# df_test['ml_output'] = model.predict(df_test[features['feature']])

figure_label = 'MODEL - ADABOOST - PER-PATIENT\n(using test cohort)'

predictor_var = {'ml_output' : 'Machine Learning',
          'mmar_total_max' : 'MMAR Max',
          'mmar_total_min' : 'MMAR Min',
          'mmar_total_sum' : 'MMAR Sum',
          'mmar_total_mean' : 'MMAR Mean',
          'segment_involvement_score_confir' : 'SIS',
          'segment_stenosis_score_confirm' : 'SSS',
          'fram_risk_confirm' : 'FRS',
          'duke_jeopardy_confirm' : 'DUKE',}

figure_fname_label = figure_label.lower().replace(' ', '').replace('\n', '').replace('(', '__').replace(')', '__')
fig, roc_tbl = viz.roc_plot(df_test, outcome, predictor_var)
fig.title(figure_label)