# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 13:52:22 2021

@author: smalk
"""



OUTCOME_EVENT = 'lesion_culprit_ica_ct'
OUTCOME_TIME = 'mi_time'
GROUP = 'plaque_type'
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
gs = GridSpec(2, 4, figure=m_fig, hspace=.5)

# In[ ] VISUALIZE - ROW 1 - COUNT - LESION TYPES - COUNTPLOT - [1x3]
from lib_prj.visualize import histplot
subplot_row = 0
subplt_title = ''

c_ax = m_fig.add_subplot(gs[subplot_row,0])
setup_dict = {
    'ax' : c_ax,
    'data' : df_main,
    'x' : 'is_hrp', 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)
c_ax.set_title('# of lesions - All')

c_ax = m_fig.add_subplot(gs[subplot_row,1])
setup_dict = {
    'ax' : c_ax,
    'data' : df_main.loc[df_main['main_vessel_id'] == 'lad'],
    'x' : 'is_hrp', 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)
c_ax.set_title('# of lesions - LAD')

c_ax = m_fig.add_subplot(gs[subplot_row,2])
setup_dict = {
    'ax' : c_ax,
    'data' : df_main.loc[df_main['main_vessel_id'] == 'lcx'],
    'x' : 'is_hrp', 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)
c_ax.set_title('# of lesions - LCx')

c_ax = m_fig.add_subplot(gs[subplot_row,3])
setup_dict = {
    'ax' : c_ax,
    'data' : df_main.loc[df_main['main_vessel_id'] == 'rca'],
    'x' : 'is_hrp', 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)
c_ax.set_title('# of lesions - RCA')



# In[ ] VISUALIZE - ROW 2 - PLAQUE TYPE DISTRIBUTION - LAD - COUNTPLOT - [1x3]
from lib_prj.visualize import histplot
subplot_row = 1

c_ax = m_fig.add_subplot(gs[subplot_row,0])
setup_dict = {
    'ax' : c_ax,
    'data' : df_main,
    'x' : 'lesion_worst', 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)

c_ax = m_fig.add_subplot(gs[subplot_row,1])
setup_dict = {
    'ax' : c_ax,
    'data' : df_main.loc[df_main['main_vessel_id'] == 'lad'],
    'x' : 'lesion_worst', 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)


c_ax = m_fig.add_subplot(gs[subplot_row,2])
setup_dict = {
    'ax' : c_ax,
    'data' : df_main.loc[df_main['main_vessel_id'] == 'lcx'],
    'x' : 'lesion_worst', 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)

c_ax = m_fig.add_subplot(gs[subplot_row,3])
setup_dict = {
    'ax' : c_ax,
    'data' : df_main.loc[df_main['main_vessel_id'] == 'rca'],
    'x' : 'lesion_worst', 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)

# In[ ] VISUALIZE - ROW 3 - PLAQUE TYPE DISTRIBUTION - LCX - COUNTPLOT - [1x3]
from lib_prj.visualize import histplot
subplt_title = 'LESION - {AGGFUNC} - HRP'
afunc = 'count_lcx'
cur_agg = mk_df_agg(raw_data, df_main, afunc, [OUTCOME_EVENT, OUTCOME_TIME])
cur_agg = cur_agg.loc[cur_agg['plaque_type'] == 'hrp']
c_ax = m_fig.add_subplot(gs[2,0])
setup_dict = {
    'ax' : c_ax,
    'data' : cur_agg,
    'x' : PARAMETER, 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)
c_ax.set_title(subplt_title.format(AGGFUNC=afunc.upper()), fontweight='bold')

subplt_title = 'LESION - {AGGFUNC} - LRP'
cur_agg = mk_df_agg(raw_data, df_main, afunc, [OUTCOME_EVENT, OUTCOME_TIME])
cur_agg = cur_agg.loc[cur_agg['plaque_type'] == 'lrp']
c_ax = m_fig.add_subplot(gs[2,1])
setup_dict = {
    'ax' : c_ax,
    'data' : cur_agg,
    'x' : PARAMETER, 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)
c_ax.set_title(subplt_title.format(AGGFUNC=afunc.upper()), fontweight='bold')

subplt_title = 'LESION - {AGGFUNC} - ALL'
cur_agg = mk_df_agg(raw_data, df_main, afunc, [OUTCOME_EVENT, OUTCOME_TIME])
cur_agg = cur_agg.loc[cur_agg['plaque_type'] == 'all']
c_ax = m_fig.add_subplot(gs[2,2])
setup_dict = {
    'ax' : c_ax,
    'data' : cur_agg,
    'x' : PARAMETER, 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)
c_ax.set_title(subplt_title.format(AGGFUNC=afunc.upper()), fontweight='bold')

# In[ ] VISUALIZE - ROW 4 - PLAQUE TYPE DISTRIBUTION - RCA - COUNTPLOT - [1x3]
from lib_prj.visualize import histplot
subplt_title = 'LESION - {AGGFUNC} - HRP'
afunc = 'count_rca'
cur_agg = mk_df_agg(raw_data, df_main, afunc, [OUTCOME_EVENT, OUTCOME_TIME])
cur_agg = cur_agg.loc[cur_agg['plaque_type'] == 'hrp']
c_ax = m_fig.add_subplot(gs[3,0])
setup_dict = {
    'ax' : c_ax,
    'data' : cur_agg,
    'x' : PARAMETER, 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)
c_ax.set_title(subplt_title.format(AGGFUNC=afunc.upper()), fontweight='bold')

subplt_title = 'LESION - {AGGFUNC} - LRP'
cur_agg = mk_df_agg(raw_data, df_main, afunc, [OUTCOME_EVENT, OUTCOME_TIME])
cur_agg = cur_agg.loc[cur_agg['plaque_type'] == 'lrp']
c_ax = m_fig.add_subplot(gs[3,1])
setup_dict = {
    'ax' : c_ax,
    'data' : cur_agg,
    'x' : PARAMETER, 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)
c_ax.set_title(subplt_title.format(AGGFUNC=afunc.upper()), fontweight='bold')

subplt_title = 'LESION - {AGGFUNC} - ALL'
cur_agg = mk_df_agg(raw_data, df_main, afunc, [OUTCOME_EVENT, OUTCOME_TIME])
cur_agg = cur_agg.loc[cur_agg['plaque_type'] == 'all']
c_ax = m_fig.add_subplot(gs[3,2])
setup_dict = {
    'ax' : c_ax,
    'data' : cur_agg,
    'x' : PARAMETER, 'hue' : OUTCOME_EVENT}
c_ax = histplot(setup_dict)
c_ax.set_title(subplt_title.format(AGGFUNC=afunc.upper()), fontweight='bold')

# In[ ] VISUALIZE - ROW 5 - PLAQUE TYPE DISTRIBUTION - TABLES - [1x3]
from lib_prj.visualize import table_lesion_confirm
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
m_fig = plt.figure()
gs = GridSpec(3, 3, figure=m_fig, hspace=.5)
table_lesion_confirm(mk_df_agg(raw_data, df_main, 'count', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=m_fig.add_subplot(gs[0,:]), lbls =['plaque_type', 'mi_event', 'n_patients', 'n_lesions'])
table_lesion_confirm(mk_df_agg(raw_data, df_main, 'count_lad', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=m_fig.add_subplot(gs[1,0]), lbls =['plaque_type', 'mi_event', 'n_patients', 'n_lesions_lad'])
table_lesion_confirm(mk_df_agg(raw_data, df_main, 'count_lcx', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=m_fig.add_subplot(gs[1,1]), lbls = ['plaque_type', 'mi_event', 'n_patients', 'n_lesions_lcx'])
table_lesion_confirm(mk_df_agg(raw_data, df_main, 'count_rca', [OUTCOME_EVENT, OUTCOME_TIME]), [GROUP, OUTCOME_EVENT], ax=m_fig.add_subplot(gs[1,2]), lbls = ['plaque_type', 'mi_event', 'n_patients', 'n_lesions_rca'])

# In[ ] VISUALIZE - ROW 3 - - [1x3]


# In[ ] VISUALIZE - ROW 4 - DESCRIPTIVE TABLES - [1x3]

# In[ ] FORMAT FINAL FIGURE
m_fig.tight_layout()
# m_fig.subplots_adjust(top=0.9) 