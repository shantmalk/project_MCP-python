# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:01:54 2020

@author: smDesktop
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols

def filt_dummy_var(pd_data, dummy_col, cond=1):
    pd_filt = pd_data[pd_data[dummy_col] == cond]
    pd_filt.reset_index(inplace=True)
    return pd_filt

def stats_anova(pd_data, idx_cols, var_col):
    pd_comb_data = pd.concat([filt_dummy_var(pd_data, dcol)[var_col] for dcol in idx_cols], axis=1)
    pd_comb_data.columns = idx_cols
    pd_melt = pd.melt(pd_comb_data.reset_index(), id_vars=['index'], value_vars=idx_cols)
    pd_melt.columns = ['index', 'idx_cols', 'value']
    model = ols('value ~ C(idx_cols)', data=pd_melt).fit()
    return sm.stats.anova_lm(model, typ=2)