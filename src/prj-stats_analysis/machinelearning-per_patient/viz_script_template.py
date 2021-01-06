# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 13:52:22 2021

@author: smalk
"""





OUTCOME_EVENT = 'mi_event'
OUTCOME_TIME = 'mi_time'
GROUP = 'plaque_type'
AGG_FUNC = ['max', 'min', 'sum', 'mean']
PARAMETER = 'mmar'


# In[ ] PRE-PROCESS DATA
import raw_data
import pandas as pd
from lib_prj.process import mk_df_agg

df_main = raw_data.PD_COMBINED
# df_main['mi_stemi'] = df_main['mi_type'] == 1

# In[ ] VISUALIZE - SETUP
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
m_fig = plt.figure()
gs = GridSpec(4, 3, figure=m_fig)

# In[ ] VISUALIZE - ROW 1 - CATPLOTS (SEABORN) - [1x3]
from lib_prj.visualize import swarmplot
subplt_title = 'AGGREGATED MMAR - {AGGFUNC}'

# AGG FUNC = MEAN
afunc = 'mean'
c_ax = m_fig.add_subplot(gs[0,0])
setup_dict = {
    'ax' : c_ax,
    'data' : mk_df_agg(raw_data, df_main, afunc, [OUTCOME_EVENT, OUTCOME_TIME]),
    'x' : GROUP, 'y' : PARAMETER,
    'hue' : OUTCOME_EVENT,
    }
c_ax = swarmplot(setup_dict)
c_ax.set_title(subplt_title.format(AGGFUNC=afunc.upper()), fontweight='bold')

# AGG FUNC = MAX
afunc = 'max'
c_ax = m_fig.add_subplot(gs[0,1])
setup_dict = {
    'ax' : c_ax,
    'data' : mk_df_agg(raw_data, df_main, afunc, [OUTCOME_EVENT, OUTCOME_TIME]),
    'x' : GROUP, 'y' : PARAMETER,
    'hue' : OUTCOME_EVENT,
    }
c_ax = swarmplot(setup_dict)
c_ax.set_title(subplt_title.format(AGGFUNC=afunc.upper()), fontweight='bold')

# AGG FUNC = SUM
afunc = 'sum'
c_ax = m_fig.add_subplot(gs[0,2])
setup_dict = {
    'ax' : c_ax,
    'data' : mk_df_agg(raw_data, df_main, afunc, [OUTCOME_EVENT, OUTCOME_TIME]),
    'x' : GROUP, 'y' : PARAMETER,
    'hue' : OUTCOME_EVENT,
    }
c_ax = swarmplot(setup_dict)
c_ax.set_title(subplt_title.format(AGGFUNC=afunc.upper()), fontweight='bold')


# In[ ] VISUALIZE - ROW 2 - ROC (MATPLOTLIB) - [1x3]
from lib_prj.visualize import roc_plot

# AGG FUNC = MEAN
afunc = 'mean'
col_tmplt = 'mmar_all_{AGGFUNC}{PTYPE}'
labels = {col_tmplt.format(AGGFUNC=afunc, PTYPE='_hrp') : 'MMAR (%) <HRP>',
           col_tmplt.format(AGGFUNC=afunc, PTYPE='_lrp') : 'MMAR (%) <LRP>',
           col_tmplt.format(AGGFUNC=afunc, PTYPE='') : 'MMAR (%) <ALL>',
          }
roc_plot(df_main, OUTCOME_EVENT, labels, m_fig.add_subplot(gs[1,0]))

# AGG FUNC = SUM
afunc = 'sum'
col_tmplt = 'mmar_all_{AGGFUNC}{PTYPE}'
labels = {col_tmplt.format(AGGFUNC=afunc, PTYPE='_hrp') : 'MMAR (%) <HRP>',
           col_tmplt.format(AGGFUNC=afunc, PTYPE='_lrp') : 'MMAR (%) <LRP>',
           col_tmplt.format(AGGFUNC=afunc, PTYPE='') : 'MMAR (%) <ALL>',
          }
roc_plot(df_main, OUTCOME_EVENT, labels, m_fig.add_subplot(gs[1,1]))

# AGG FUNC = MAX
afunc = 'max'
col_tmplt = 'mmar_all_{AGGFUNC}{PTYPE}'
labels = {col_tmplt.format(AGGFUNC=afunc, PTYPE='_hrp') : 'MMAR (%) <HRP>',
           col_tmplt.format(AGGFUNC=afunc, PTYPE='_lrp') : 'MMAR (%) <LRP>',
           col_tmplt.format(AGGFUNC=afunc, PTYPE='') : 'MMAR (%) <ALL>',
          }
roc_plot(df_main, OUTCOME_EVENT, labels, m_fig.add_subplot(gs[1,2]))

# In[ ] VISUALIZE - ROW 3 - TABLES (MATPLOTLIB) - [1x3]
from lib_prj.visualize import table_mmar_confirm
import numpy as np
from functools import reduce

table_mmar_confirm(mk_df_agg(raw_data, df_main, 'mean', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=m_fig.add_subplot(gs[2,0]))
table_mmar_confirm(mk_df_agg(raw_data, df_main, 'max', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=m_fig.add_subplot(gs[2,1]))
table_mmar_confirm(mk_df_agg(raw_data, df_main, 'sum', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=m_fig.add_subplot(gs[2,2]))


# In[ ] Kaplan-Mier Survival
from lifelines import KaplanMeierFitter
from lib_prj.visualize import kmsurvival_mmar_confirm

kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_mean_hrp', m_fig.add_subplot(gs[3,0]), .85)
kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_max_hrp', m_fig.add_subplot(gs[3,1]), .85)
kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_sum_hrp', m_fig.add_subplot(gs[3,2]), .85)
