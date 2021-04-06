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







# In[ ] SCCT BRANCH-BY-BRANCH
from lib_prj.visualize import swarmplot
from lib_prj.visualize import get_line_from_axis
import numpy as np
import seaborn as sns
import raw_data
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from confirm_idc_list import confirm_idc_allowed as idc_allowed

df_scct = raw_data.PD_SCCT
df_scct = df_scct.loc[df_scct['confirm_idc'].isin(idc_allowed)]
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



