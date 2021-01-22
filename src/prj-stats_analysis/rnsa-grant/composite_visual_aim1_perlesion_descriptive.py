# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 13:52:22 2021

@author: smalk
"""


from lib_prj.visualize import kdeplot
OUTCOME_EVENT = 'mi_type'
OUTCOME_TIME = 'mi_time'
GROUP = 'plaque_type'
AGG_FUNC = ['max', 'min', 'sum', 'mean']
PARAMETER = 'mmar'

def kdeplot_wrapper(df, plaque_param, outcome, s_ax, row):
    t_pos = (0.5, 0.70)
    subplt_title = '{PTYPE} - {PARAM}'
    plaque_type = 'hrp'
    
    c_ax = s_ax[row, 0]
    c_ax.set_title(subplt_title.format(PARAM=plaque_param.upper(), PTYPE=plaque_type.upper()), fontweight='bold', position=t_pos)
    setup_dict = {
        'ax' : c_ax,
        'data' : df.loc[df_main['is_hrp'] == 1],
        'x' :  plaque_param,
        # 'y' : 'lumenareastenosis',
        'hue' : outcome,
        }
    c_ax = kdeplot(setup_dict)
    
    
    plaque_type = 'lrp'
    c_ax = s_ax[row, 1]
    c_ax.set_title(subplt_title.format(PARAM=plaque_param.upper(), PTYPE=plaque_type.upper()), fontweight='bold', position=t_pos)
    setup_dict = {
        'ax' : c_ax,
        'data' : df.loc[df_main['is_hrp'] == 0],
        'x' :  plaque_param,
        # 'y' : 'lumenareastenosis',
        'hue' : outcome,
        }
    c_ax = kdeplot(setup_dict)
    
    plaque_type = 'all'
    c_ax = s_ax[row, 2]
    c_ax.set_title(subplt_title.format(PARAM=plaque_param.upper(), PTYPE=plaque_type.upper()), fontweight='bold', position=t_pos)
    setup_dict = {
        'ax' : c_ax,
        'data' : df,
        'x' :  plaque_param,
        # 'y' : 'lumenareastenosis',
        'hue' : outcome,
        }
    kdeplot(setup_dict)



# In[ ] PRE-PROCESS DATA
import raw_data_per_lesion
import pandas as pd
from lib_prj.process import mk_df_agg

df_main = raw_data_per_lesion.PD_MMAR
df_main['mi_type'] = df_main['mi_type'].fillna(0)
# df_main['mi_stemi'] = df_main['mi_type'] == 1

# In[ ] VISUALIZE - SETUP
import matplotlib.pyplot as plt
# USE SUBPLOTS TO SHARE AXIS
m_fig, s_ax = plt.subplots(8,3, sharey='row', sharex='row')

# In[ ] VISUALIZE - ROW 1 - DESCRIPTIVE WITH KDEPLOTS (SEABORN) - [1x3]
kdeplot_wrapper(df_main, 'omlddistance', OUTCOME_EVENT, s_ax, 0)
kdeplot_wrapper(df_main, 'lesion_length', OUTCOME_EVENT, s_ax, 1)
kdeplot_wrapper(df_main, 'lumenvolume_lesion', OUTCOME_EVENT, s_ax, 2)
kdeplot_wrapper(df_main, 'lesion_length', OUTCOME_EVENT, s_ax, 3)
kdeplot_wrapper(df_main, 'plaquevolume_lesion', OUTCOME_EVENT, s_ax, 4)
kdeplot_wrapper(df_main, 'vesselvolume_lesion', OUTCOME_EVENT, s_ax, 5)
# kdeplot_wrapper(df_main, 'lumenvolume_lesion', OUTCOME_EVENT, s_ax, 6)
kdeplot_wrapper(df_main, 'lumenvolume_lesion', OUTCOME_EVENT, s_ax, 6)
kdeplot_wrapper(df_main, 'mmar', OUTCOME_EVENT, s_ax, 7)

# In[ ] Format final figure
# m_fig.tight_layout(pad=0.25)
# m_fig.tight_layout(pad=.00125)
# m_fig.tight_layout()