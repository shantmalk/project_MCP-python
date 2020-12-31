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

from plotly.offline import plot

import lib_prj.process as prc
import lib_prj.visualize as viz
import params
import ml_raw_data

# In[1] Raw data
cols = params.COLUMNS
blacklist = params.BLACKLIST
df = ml_raw_data.PD_COMBINED

# In[3] Select parameters - SEE PARAMS.PY
params = prc.clean_df(df, cols, blacklist)

# In[4] Select outcome
outcome = 'macelr_event_confirm'

# In[5] View data

args_plotly = {
    'y' : 'mmar_lad_mean',
    'x' : outcome,
    'points' : 'all',
    'color' : outcome,
    'labels' : {'Outcome', outcome},
    'title' : 'MULTIVARIATEREG - Basic'
    }
fig = viz.boxplot_plotly(df, args_plotly, '')
plot(fig)