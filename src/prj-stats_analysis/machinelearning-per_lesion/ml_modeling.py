# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 18:55:07 2020

@author: smalk
"""

import ml_feature_selection
import ml_raw_data
import pandas as pd

df = ml_raw_data.PD_COMBINED

# df = df[df['mi_event'] == 1]
features = ml_feature_selection.FEATURES # limit to top 10 for now.
# ml_feature_selection.view_features_variance(features, ml_feature_selection.OUTCOME, '')

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

# In[ ]


# SPLIT DATA INTO TRAINING AND TESTING
training_f = .10
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

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=5, random_state=1)
n_scores = cross_val_score(model, testing_x, testing_y, scoring='accuracy', cv=cv)
print('Accuracy: %.3f (%.3f)' % (mean(n_scores), std(n_scores)))

loss = brier_score_loss(testing_y, pred_probability[:, 1])
print('Brier Score: %.3f' % loss)


# In[ ] Add some additional variables
df['mmar_vessel_vol'] = df['mass_mcp_perc'] * df['vesselvolume_lesion']


# In[] ROC-AUC ANALYSIS - USING ONLY TEST DATA
import lib_prj
df_test = testing.copy()

df_test['ml_output'] = model.predict_proba(df_test[features['index']])[:, 1]
# df_test['ml_output'] = model.predict(df_test[features['index']])
figure_label = 'Figure 2E'
predictor_var = ['ml_output',
                 'mass_mcp_perc',
                 'mass_mcp_g',
                 'vesselvolume_lesion',
                 'lumenvolume_lesion',
                 'lumenminimaldiameter',
                 'lesion_worst',
                 ]
labels = {'ml_output' : 'Machine Learning',
          'mass_mcp_perc' : 'MMAR(%)',
          'mass_mcp_g' : 'MMAR(g)',
          'vesselvolume_lesion' : 'Lesion vessel vol.',
          'lumenvolume_lesion' : 'Lesion lumen vol.',
          'lumenminimaldiameter' : 'MLD',
          'lesion_worst' : 'MIN(MLA)',
          }
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = lib_prj.visualize.roc_plot(df_test, outcome_var, predictor_var, labels)

# In[] ROC-AUC ANALYSIS - USING ALL DATA
import lib_prj
df_test = df.copy()

df_test['ml_output'] = model.predict_proba(df_test[features['index']])[:, 1]
# df_test['ml_output'] = model.predict(df_test[features['index']])
figure_label = 'Figure 2E'
predictor_var = ['ml_output',
                 'mass_mcp_perc',
                 'mass_mcp_g',
                 'vesselvolume_lesion',
                 'lumenvolume_lesion',
                 'lumenminimaldiameter',
                 'lesion_worst',
                 'mmar_vessel_vol',
                 'vesselwallremodelingindex',
                 'omlddistance',
                 ]
labels = {'ml_output' : 'Machine Learning',
          'mass_mcp_perc' : 'MMAR(%)',
          'mass_mcp_g' : 'MMAR(g)',
          'vesselvolume_lesion' : 'Lesion vessel vol.',
          'lumenvolume_lesion' : 'Lesion lumen vol.',
          'lumenminimaldiameter' : 'MLD',
          'lesion_worst' : 'MIN(MLA)',
          'mmar_vessel_vol' : 'MMAR / Vessel Volume',
          'vesselwallremodelingindex' : 'Remodeling index',
          'omlddistance' : 'Distance to MLD'}

figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = lib_prj.visualize.roc_plot(df_test, outcome_var, predictor_var, labels)