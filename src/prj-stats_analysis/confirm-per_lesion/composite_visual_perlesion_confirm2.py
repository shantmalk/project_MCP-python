# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 13:52:22 2021

@author: smalk
"""



OUTCOME_EVENT = 'mi_event'
OUTCOME_TIME = 'mi_time'
GROUP = 'is_hrp'
AGG_FUNC = ['max', 'min', 'sum', 'mean']
PARAMETER = 'mmar'


# In[ ] PRE-PROCESS DATA
import raw_data
import pandas as pd
from lib_prj.process import mk_df_agg

df_main = raw_data.PD_MMAR

# In[ ] VISUALIZE - SETUP
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
m_fig = plt.figure()
gs = GridSpec(4, 3, figure=m_fig)

# In[ ] VISUALIZE - ROW 1 - CATPLOTS (SEABORN) - [1x3]
from lib_prj.visualize import swarmplot
subplt_title = 'MEAN MMAR - ALL'
c_ax = m_fig.add_subplot(gs[0,0])
setup_dict = {
    'ax' : c_ax,
    'data' : df_main,
    'x' : OUTCOME_EVENT, 'y' : PARAMETER,
    # 'hue' : OUTCOME_EVENT,
    }
c_ax = swarmplot(setup_dict)
c_ax.set_title(subplt_title, fontweight='bold')

subplt_title = 'MEAN MMAR - STRATIFIED BY HRP'
c_ax = m_fig.add_subplot(gs[0,1])   
setup_dict = {
    'ax' : c_ax,
    'data' : df_main,
    'x' : OUTCOME_EVENT, 'y' : PARAMETER,
    'hue' : GROUP,
    }
c_ax = swarmplot(setup_dict)
c_ax.set_title(subplt_title, fontweight='bold')

subplt_title = 'MEAN MMAR - STRATIFIED BY VESSEL'
c_ax = m_fig.add_subplot(gs[0,2])
setup_dict = {
    'ax' : c_ax,
    'data' : df_main,
    'x' : OUTCOME_EVENT, 'y' : PARAMETER,
    'hue' : 'main_vessel_id',
    }
c_ax = swarmplot(setup_dict)
c_ax.set_title(subplt_title, fontweight='bold')

# In[ ] VISUALIZE - ROW 2 - ROC (MATPLOTLIB) - [1x3]
from lib_prj.visualize import roc_plot

labels = {'mmar' : 'MMAR (%)',
          'mmar_hrp' : 'MMAR (%) <HRP>',
          'mmar_lrp' : 'MMAR (%) <LRP>',
          }
roc_plot(df_main, OUTCOME_EVENT, labels, m_fig.add_subplot(gs[1,0]))

df_main['mmar_composite'] = (df_main['mmar'] * df_main['plaquevolume_lesion'] * df_main['fibrousvolume_lesion'] * df_main['lesion_length'] * df_main['vesselvolume_lesion'] * df_main['vesselwallremodelingindex'] ) / (df_main['peak_va'] * df_main['lumenvolume_lesion'])
labels = {'mmar_composite' : 'MMAR composite (%)',
          'plaquevolume_lesion' : 'Plaque Volume',
          'fibrousvolume_lesion' : 'Fibrous Plaque Volume',
          'lesion_length' : 'Lesion Length',
          'plaqueburdenmean_lesion' : 'Plaque Burden',
          'vesselwallremodelingindex' : 'Remodeling Index',
          }
roc_plot(df_main.loc[df_main['is_hrp'] == 1], OUTCOME_EVENT, labels, m_fig.add_subplot(gs[1,1]))



labels = {'mmar' : 'MMAR (%)',
          'mmar_hrp' : 'MMAR (%) <HRP>',
          'mmar_lrp' : 'MMAR (%) <LRP>',
          'is_hrp' : 'HRP'
          }
roc_plot(df_main, OUTCOME_EVENT, labels, m_fig.add_subplot(gs[1,2]))

# # AGG FUNC = MAX
# afunc = 'max'
# col_tmplt = 'mmar_all_{AGGFUNC}{PTYPE}'
# labels = {col_tmplt.format(AGGFUNC=afunc, PTYPE='_hrp') : 'MMAR (%) <HRP>',
#            col_tmplt.format(AGGFUNC=afunc, PTYPE='_lrp') : 'MMAR (%) <LRP>',
#            col_tmplt.format(AGGFUNC=afunc, PTYPE='') : 'MMAR (%) <ALL>',
#           }
# roc_plot(df_main, OUTCOME_EVENT, labels, m_fig.add_subplot(gs[1,2]))

# In[ ] VISUALIZE - CONTIGENCY TABLE
from scipy.stats import fisher_exact

hrp_tab = pd.crosstab(df_main['is_hrp'], df_main[OUTCOME_EVENT])
print('ODDS RATIO - HRP')
print(fisher_exact(hrp_tab))

mmar_tab = pd.crosstab(df_main['mmar'] > df_main['mmar'].quantile(.25), df_main[OUTCOME_EVENT])
print('ODDS RATIO - MMAR')
print(fisher_exact(mmar_tab))

mmar_tab = pd.crosstab(df_main['mmar_hrp'] > df_main['mmar'].quantile(.25), df_main[OUTCOME_EVENT])
print('ODDS RATIO - MMAR_HRP')
print(fisher_exact(mmar_tab))

# In[ ] VISUALIZE - ROW 3 - TABLES (MATPLOTLIB) - [1x3]
from lib_prj.visualize import table_mmar_confirm
import numpy as np
from functools import reduce

# table_mmar_confirm(mk_df_agg(raw_data, df_main, 'mean', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=m_fig.add_subplot(gs[2,0]))
# table_mmar_confirm(mk_df_agg(raw_data, df_main, 'max', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=m_fig.add_subplot(gs[2,1]))
# table_mmar_confirm(mk_df_agg(raw_data, df_main, 'sum', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=m_fig.add_subplot(gs[2,2]))

# In[ ] Kaplan-Mier Survival
from lifelines import KaplanMeierFitter
from lib_prj.visualize import kmsurvival_mmar_confirm

# kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_mean', m_fig.add_subplot(gs[3,0]), .85, 'MMAR<ALL> > {CUTOFF:0.2f}')
# kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_max', m_fig.add_subplot(gs[3,1]), .85, 'MMAR<ALL> > {CUTOFF:0.2f}')
# kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_sum', m_fig.add_subplot(gs[3,2]), .85, 'MMAR<ALL> > {CUTOFF:0.2f}')


# In[ ] Kaplan-Mier Survival
from lifelines import KaplanMeierFitter
from lib_prj.visualize import kmsurvival_mmar_confirm

# kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_mean_hrp', m_fig.add_subplot(gs[4,0]), .85, 'MMAR<HRP> > {CUTOFF:0.2f}')
# kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_max_hrp', m_fig.add_subplot(gs[4,1]), .85, 'MMAR<HRP> > {CUTOFF:0.2f}')
# kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_sum_hrp', m_fig.add_subplot(gs[4,2]), .85, 'MMAR<HRP> > {CUTOFF:0.2f}')

# In[ ] Kaplan-Mier Survival
from lifelines import KaplanMeierFitter
from lib_prj.visualize import kmsurvival_mmar_confirm

# kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_mean_lrp', m_fig.add_subplot(gs[5,0]), .85, 'MMAR<LRP> > {CUTOFF:0.2f}')
# kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_max_lrp', m_fig.add_subplot(gs[5,1]), .85, 'MMAR<LRP> > {CUTOFF:0.2f}')
# kmsurvival_mmar_confirm(df_main, OUTCOME_EVENT, OUTCOME_TIME, 'mmar_all_sum_lrp', m_fig.add_subplot(gs[5,2]), .85, 'MMAR<LRP> > {CUTOFF:0.2f}')


