# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 18:55:07 2020

@author: smalk
"""

import ml_feature_selection
import ml_raw_data
import pandas as pd

df = ml_raw_data.PD_COMBINED
features = ml_feature_selection.FEATURES[:10] # limit to top 10 for now.
ml_feature_selection.view_features_variance(features, ml_feature_selection.OUTCOME, '')

# In[ ] AdaBoost Classifier (ensembe classifier?)
# SEE:  https://scikit-learn.org/stable/modules/ensemble.html

# from sklearn.model_selection import cross_val_score
# from sklearn.datasets import load_iris
# from sklearn.ensemble import AdaBoostClassifier

# X, y = load_iris(return_X_y=True)
# clf = AdaBoostClassifier(n_estimators=100)
# scores = cross_val_score(clf, X, y, cv=5)
# print(scores.mean())

# In[ ] AdaBoost Classifier with confirm data
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



# SPLIT DATA INTO TRAINING AND TESTING
training_f = .33
outcome_var = ml_feature_selection.OUTCOME

testing, training = train_test_split(df, test_size=training_f, random_state=0, stratify=df[outcome_var])

training_x = training[features['index']]
training_y = training[outcome_var]

testing_x = testing[features['index']]
testing_y = testing[outcome_var]

model = AdaBoostClassifier(random_state=1,
                           n_estimators=40,
                           learning_rate=1,
                           )
model.fit(training_x, training_y)
pred_probability = model.predict_proba(testing_x)
# y_pred = model.predict(testing_x)
# print('Accuracy: ', metrics.accuracy_score(testing_y, y_pred))

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=5, random_state=1)
n_scores = cross_val_score(model, testing_x, testing_y, scoring='accuracy', cv=cv)
print('Accuracy: %.3f (%.3f)' % (mean(n_scores), std(n_scores)))

loss = brier_score_loss(testing_y, pred_probability[:, 1])
print('Brier Score: %.3f' % loss)

# In[] ROC-AUC ANALYSIS - USING ONLY TEST DATA
import lib_prj
df_test = testing.copy()
df_test['fram_risk_confirm'] = df_test['fram_risk_confirm'].fillna(df['fram_risk_confirm'].mean())

df_test['ml_output'] = model.predict_proba(df_test[features['index']])[:, 1]
figure_label = 'Figure 2E'
predictor_var = ['ml_output',
                 'mmar_total_max',
                 'mmar_total_min',
                 'mmar_total_sum',
                 'mmar_total_mean',
                 'segment_involvement_score_confir',
                 'segment_stenosis_score_confirm',
                 'fram_risk_confirm',
                 'duke_jeopardy_confirm',
                 ]
labels = {'ml_output' : 'Machine Learning',
          'mmar_total_max' : 'MMAR Max',
          'mmar_total_min' : 'MMAR Min',
          'mmar_total_sum' : 'MMAR Sum',
          'mmar_total_mean' : 'MMAR Mean',
          'segment_involvement_score_confir' : 'SIS',
          'segment_stenosis_score_confirm' : 'SSS',
          'fram_risk_confirm' : 'FRS',
          'duke_jeopardy_confirm' : 'DUKE',}
# figure_fname_label = figure_label.lower().replace(' ', '')
# fig, roc_tbl = lib_prj.visualize.roc_plot(df_test, outcome_var, predictor_var, labels)

# In[] ROC-AUC ANALYSIS - USING ALL DATA
import lib_prj
df_test = df.copy()
df_test['fram_risk_confirm'] = df_test['fram_risk_confirm'].fillna(df['fram_risk_confirm'].mean())

df_test['ml_output'] = model.predict_proba(df_test[features['index']])[:, 1]
# df_test['ml_output'] = model.predict(df_test[features['index']])
figure_label = 'Per-Patient'
predictor_var = {'ml_output' : 'Machine Learning',
                 'mmar_total_max' : 'MMAR Max',
                 'mmar_total_min' : 'MMAR Min',
                 'mmar_total_sum' : 'MMAR Sum',
                 'mmar_total_mean' : 'MMAR Mean',
                 'segment_involvement_score_confir' : 'SIS',
                 'segment_stenosis_score_confirm' : 'SSS',
                 'fram_risk_confirm' : 'FRS',
                 'duke_jeopardy_confirm' : 'DUKE',}

figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = lib_prj.visualize.roc_plot(df_test, outcome_var, predictor_var)
fig.title(figure_label)