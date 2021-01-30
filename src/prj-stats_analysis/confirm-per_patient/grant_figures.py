# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 14:57:41 2021

@author: smalk
"""

OUTCOME_EVENT = 'mace_event_confirm'
OUTCOME_TIME = 'mi_time'
GROUP = 'plaque_type'
AGG_FUNC = ['max', 'min', 'sum', 'mean']
PARAMETER = 'mmar'


# In[ ] PRE-PROCESS DATA
import raw_data
import pandas as pd
from lib_prj.process import mk_df_agg

df_main = raw_data.PD_COMBINED

# In[ ] VISUALIZE - SETUP
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# In[ ] FIGURE 1 - MASS COMPARISON
from lib_prj.visualize import swarmplot
from lib_prj.visualize import get_line_from_axis
import numpy as np
import seaborn as sns


# sns.set_theme()
plt.style.use('fivethirtyeight')
subplt_title = 'AGGREGATED MMAR - {AGGFUNC}'

df_main['mi_event_str'] = np.where(df_main[OUTCOME_EVENT] == 1, '+MACE', '-MACE')



# AGG FUNC = MEAN
afunc = 'mean'
m_fig = plt.figure(figsize=(10,6))
c_ax = plt.axes()
setup_dict = {
    'ax' : c_ax,
    'data' : mk_df_agg(raw_data, df_main, afunc, ['mi_event_str', OUTCOME_TIME]),
    'x' : GROUP, 'y' : PARAMETER,
    'hue' : 'mi_event_str',
   }
c_ax = swarmplot(setup_dict)

# STYLIZE
# c_ax.set_title(subplt_title.format(AGGFUNC=afunc.upper()), fontweight='bold')
c_ax.set_xlabel('Lesion Type', fontname='arial', fontweight='bold', fontsize=45)
c_ax.set_ylabel('MMAR (%)', fontname='arial', fontweight='bold', fontsize=45)
plt.setp(c_ax.get_xticklabels(), fontname='arial', fontsize=40, fontweight='bold')
plt.setp(c_ax.get_yticklabels(), fontname='arial', fontsize=40, fontweight='bold')
plt.tight_layout()


# LEGEND
# c_ax.legend(loc='upper left')
# lbls = c_ax.get_legend().get_texts()

# c= 0 
# for ii in lbls:
#     if c > 1:
#         ii.set_text('_nolabel_')
#         ii._visible = False
#         ii.set_alpha(100)
#         # ii.draw = False
#     c += 1
    

# plt.setp(c_ax.get_legend().get_texts(), fontsize='22') # for legend text
# c_ax.legend(fontsize='x-large', title_fontsize='40')

# In[ ] TABLE 1 - MASS COMPARISON
from lib_prj.visualize import table_mmar_confirm
# import numpy as np
# from functools import reduce

m_fig = plt.figure()
c_ax = plt.axes()
tbl = table_mmar_confirm(mk_df_agg(raw_data, df_main, 'mean', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=c_ax, lbls = ['Lesion Type', 'MACE', 'N', 'MMAR (%)', 'p-value'])

# In[ ] Kaplan-Mier Survival
from lifelines import KaplanMeierFitter
from lib_prj.visualize import kmsurvival_mmar_confirm

m_fig = plt.figure(figsize=(10,6))
c_ax = plt.axes()
kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_mean_hrp', c_ax, .75, '$MMAR_{{HRP}}$ > {CUTOFF:0.2f}%')
plt.setp(c_ax.get_xticklabels(), fontname='arial', fontsize=25, fontweight='bold')
plt.setp(c_ax.get_yticklabels(), fontname='arial', fontsize=25, fontweight='bold')
c_ax.set_xlabel('Time (days after CCTA)', fontname='arial', fontweight='bold', fontsize=30)
c_ax.set_ylabel(' Proportion (-) MACE', fontname='arial', fontweight='bold', fontsize=30)
plt.setp(c_ax.get_legend().get_texts(), fontsize=25) # for legend text
plt.tight_layout()

# In[ ] ROC
# AGG FUNC = MAX
from lib_prj.visualize import roc_plot
m_fig = plt.figure(figsize=(10,6))
c_ax = plt.axes()

# df_main['mmar_lrp_hrp'] = (df_main['mmar_all_max_hrp'] - df_main['mmar_all_max_lrp']) / df_main['mmar_all_max_lrp']
df_main['mmar_lrp_hrp'] = df_main['mmar_all_max_hrp'] * df_main['mmar_all_max_lrp']

afunc = 'max'
col_tmplt = 'mmar_all_{AGGFUNC}{PTYPE}'
labels = {'mmar_all_max' : '$MMAR_{{ALL}}$',
          col_tmplt.format(AGGFUNC=afunc, PTYPE='_hrp') : '$MMAR_{{HRP}}$',
          col_tmplt.format(AGGFUNC=afunc, PTYPE='_lrp') : '$MMAR_{{LRP}}$',
          'mmar_lrp_hrp' : '$MMAR_{{HRP/LRP}}$'
          }
rr, rr_pd = roc_plot(df_main, OUTCOME_EVENT, labels, c_ax)
plt.tight_layout()

# # In[ ] TEST ROC...
# import sklearn.metrics as metrics
# fpr, tpr, threshold = metrics.roc_curve(df_main['mmar_all_mean'], df_main[OUTCOME_EVENT])