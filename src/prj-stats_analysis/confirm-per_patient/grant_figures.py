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

def _set_ax(ax, grid_ax='y'):
    # MODIFY AXIS GRID
    grid_width = '3'
    spine_width = '4.5'
    spine_color = [171/255, 161/255, 148/255]
    grid_color = spine_color
    # grid_color = [216/255, 221/255, 222/255]
    # spine_color = grid_color
    ax.spines["top"].set_visible(True)
    ax.spines["top"].set_linewidth(spine_width)
    ax.spines["top"].set_color(spine_color)
    
    ax.spines["bottom"].set_visible(True)
    ax.spines["bottom"].set_linewidth(spine_width)
    ax.spines["bottom"].set_color(spine_color)
    
    ax.spines["left"].set_visible(True)
    ax.spines["left"].set_linewidth(spine_width)
    ax.spines["left"].set_color(spine_color)
    
    ax.spines["right"].set_visible(True)
    ax.spines["right"].set_linewidth(spine_width)
    ax.spines["right"].set_color(spine_color)
    
    # c_ax.spines['bottom'].set_visible(True)
    # c_ax.spines['left'].set_visible(True)
    # c_ax.spines['right'].set_visible(True)
    ax.grid(linewidth=grid_width, axis=grid_ax, color=grid_color)
    return ax



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

# MODIFY AXIS GRID
c_ax = _set_ax(c_ax)

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
c_ax.set_ylabel('Proportion (-) MACE', fontname='arial', fontweight='bold', fontsize=30)
plt.setp(c_ax.get_legend().get_texts(), fontsize=25) # for legend text
plt.tight_layout()
# MODIFY AXIS GRID
c_ax = _set_ax(c_ax, 'both')



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
# MODIFY AXIS GRID
c_ax = _set_ax(c_ax, 'both')



# # In[ ] TEST ROC...
# import sklearn.metrics as metrics
# fpr, tpr, threshold = metrics.roc_curve(df_main['mmar_all_mean'], df_main[OUTCOME_EVENT])

# In[ ] POWER ANALYSIS
from statsmodels.stats.power import TTestIndPower

effect_size = 0.7

# KANG STUDY:  VARIABLES
N_mace_pos = 29
MEAN_mace_pos = 37.3
STD_mace_pos = 11.9

N_mace_neg = 635
MEAN_mace_neg = 30.5
STD_mace_neg = 12.1

STD_pooled = 16.1

effect_size_kang = (MEAN_mace_pos - MEAN_mace_neg) / STD_pooled
alpha = 0.05
power = 0.9

power_params_out = '''
Power Analysis Parameters:
    Alpha: {alpha:0.2f}
    Power:  {power:0.2f}
    Effect Size (Kang et al.): {effect_size:0.2f}
'''.format(alpha=alpha, power=power, effect_size=effect_size_kang)

p_analysis = TTestIndPower()
plt.style.use('fivethirtyeight')
sample_size = np.round(p_analysis.solve_power(effect_size=effect_size_kang, alpha=alpha, power=power))
print(power_params_out)
print('Required sample size: {sz:0.2f}'.format(sz=sample_size))


fig = TTestIndPower().plot_power(dep_var='nobs', nobs=np.arange(10,200),
                                 # effect_size=np.array([0.2,  0.43, 0.5, 0.8]),
                                 effect_size=np.array([0.43]),
                                 alpha=alpha,
                                 title='')

sns.scatterplot(x=[sample_size], y=[power], s=100, color=[(140/255, 39/255, 30/255)], label = 'Estimated Observations = %i' % sample_size)
plt.plot([sample_size, sample_size], [0, power], color=[140/255, 39/255, 30/255], linewidth=2, linestyle='dashed')
plt.plot([0, sample_size], [power, power], color=[140/255, 39/255, 30/255], linewidth=2, linestyle='dashed')

c_ax = plt.gca()
plt.setp(c_ax.get_xticklabels(), fontname='arial', fontsize=16, fontweight='bold')
plt.setp(c_ax.get_yticklabels(), fontname='arial', fontsize=16, fontweight='bold')
c_ax.set_ylabel('Power (1 - ' + r'$\beta$)', fontname='arial', fontweight='bold', fontsize=20)
c_ax.set_xlabel('Number of Observations', fontname='arial', fontweight='bold', fontsize=20)
c_ax.set_title('Power of variable effect sizes\n' + r'($\alpha = %0.2f$)' % alpha, fontname='arial', fontweight='bold', fontsize=20)
plt.legend(loc='lower left')
c_ax.get_legend().get_texts()[0].set_text('Effect Size$_{Kang}$ = %0.2f' % effect_size_kang)
plt.setp(c_ax.get_legend().get_texts(), fontsize=10)
plt.tight_layout()

# MODIFY AXIS GRID
c_ax = _set_ax(c_ax, 'both')

# In[ ] SCCT BRANCH-BY-BRANCH
from lib_prj.visualize import swarmplot
from lib_prj.visualize import get_line_from_axis
import numpy as np
import seaborn as sns

df_scct = raw_data.PD_SCCT
df_scct = df_scct.loc[df_scct['mass_mcp_perc'] > -1]
df_scct = df_scct.loc[df_scct['id_vessel'] != 'an_rca1']

# sns.set_theme()
# plt.style.use('fivethirtyeight')

m_fig = plt.figure(figsize=(10,6))
c_ax = plt.axes()
setup_dict = {
    'ax' : c_ax,
    'data' : df_scct.sort_values(by='id_vessel', ascending=True),
    'x' : 'id_vessel', 'y' : 'mass_mcp_perc',
    # 'hue' : OUTCOME_EVENT,
    'color' : "dodgerblue",
    # 'orient' : 'v ',
   }
c_ax = swarmplot(setup_dict)

# STYLIZE
c_ax.set_ylabel('', fontname='arial', fontweight='bold', fontsize=45)
c_ax.set_xlabel('Percent LV Mass (%)', fontname='arial', fontweight='bold', fontsize=30)
plt.setp(c_ax.get_xticklabels(), fontname='arial', fontsize=25, fontweight='bold', rotation=45)
plt.setp(c_ax.get_yticklabels(), fontname='arial', fontsize=25, fontweight='bold', )
plt.tight_layout()

# MODIFY AXIS GRID
c_ax = _set_ax(c_ax)

# In[ ] TABLE 1 - MASS COMPARISON
from lib_prj.visualize import table_scct_confirm
# import numpy as np
# from functools import reduce

m_fig = plt.figure()
c_ax = plt.axes()
xx = df_scct[['id_vessel', 'mass_mcp_perc']].rename(columns={'mass_mcp_perc': 'mmar'})
tbl = table_scct_confirm(xx, ['id_vessel'], ax=c_ax, lbls = [ 'Vessel ID', 'N', 'Mass Percent (%)'])


# In[ ] COMPARE TROPONIN
from lib_prj.visualize import linear_regression_plot
import raw_data
x_col = 'peak_tn'
# x_col = 'upperlimit_tn'
# x_col = 'ckmb_peak'

y_col = 'mass_mcp_perc'

df_redcap = raw_data.PD_REDCAP
df_redcap['peak_tn'] = df_redcap['peak_tn'].astype('float')
df_redcap['trop_pos'] = df_redcap['trop_pos'].astype('bool')
df_redcap['ckmb_pos'] = df_redcap['ckmb_pos'].astype('bool')
df_redcap = df_redcap.loc[~(df_redcap[y_col].isna())]
df_redcap = df_redcap.loc[df_redcap['readjudication_level'].astype('float') == 2]
# df_redcap['peak_tn_mod'] = df_redcap['peak_tn'] / df_redcap['upperlimit_tn'].astype('float') * 100

# df_redcap = df_redcap.loc[df_redcap['trop_pos'] == True]
# df_redcap = df_redcap.loc[df_redcap[x_col] > 0]
# df_redcap = df_redcap.loc[df_redcap[y_col] > 0]


m_fig = plt.figure()
c_ax = plt.axes()

setup_dict = {
    'ax' : c_ax,
    'data' : df_redcap,
    'x' : x_col, 'y' : y_col,
    # 'hue' : OUTCOME_EVENT,
    # 'color' : "dodgerblue",
   }
c_ax = linear_regression_plot(setup_dict)

# STYLIZE
# c_ax.set_xlabel('', fontname='arial', fontweight='bold', fontsize=45)
# c_ax.set_ylabel('Percent LV Mass (%)', fontname='arial', fontweight='bold', fontsize=45)
# plt.setp(c_ax.get_xticklabels(), fontname='arial', fontsize=40, fontweight='bold', rotation=45)
# plt.setp(c_ax.get_yticklabels(), fontname='arial', fontsize=40, fontweight='bold', )
# plt.tight_layout()

# In[ ] ROC
# AGG FUNC = MAX
from lib_prj.visualize import roc_plot
m_fig = plt.figure(figsize=(10,6))
c_ax = plt.axes()



labels = {'mass_mcp_perc' : '$MMAR$',
          }
rr, rr_pd = roc_plot(df_redcap, 'trop_pos', labels, c_ax)
plt.tight_layout()
# MODIFY AXIS GRID
c_ax = _set_ax(c_ax, 'both')
