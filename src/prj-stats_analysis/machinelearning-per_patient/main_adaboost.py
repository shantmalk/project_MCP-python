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
prc.view_features_variance(ft, 'FEATURE SELECTION - ' + outcome)


# In[4] Build model - split data into testing and training sets
stat_method = 'AdaBoost'
training_f = .33

testing, training = train_test_split(df, test_size=training_f, random_state=0, stratify=df[outcome])

training_x = training[ft['feature']]
training_y = training[outcome]

testing_x = testing[ft['feature']]
testing_y = testing[outcome]

model = AdaBoostClassifier(random_state=1,
                           n_estimators=100,
                           learning_rate=1,
                           )

model.fit(training_x, training_y)
pred_probability = model.predict_proba(testing_x)

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=5, random_state=1)
n_scores = cross_val_score(model, testing_x, testing_y, scoring='accuracy', cv=cv)
loss = brier_score_loss(testing_y, pred_probability[:, 1])

# In[6] Build model - view metrics of algorithm

# METRICS OF ASSESSMENT:
metric_str = '{METHOD:<10} | {METRIC:<15} | {VAL:.3f}'

print(metric_str.format(METHOD=stat_method, METRIC='ACCURACY[MEAN]', VAL=mean(n_scores)))
print(metric_str.format(METHOD=stat_method, METRIC='ACCURACY[STD]', VAL=std(n_scores)))
print(metric_str.format(METHOD=stat_method, METRIC='BRIER_SCORE', VAL=loss))

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