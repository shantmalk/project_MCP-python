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
    # ax.grid(linewidth=grid_width, axis=grid_ax, color=grid_color)
    return ax


def make_color_map(ls):
    color_map = dict()
    viridis = cm.get_cmap('viridis', len(ls))
    for ii in range(len(ls)):
        color_map[ls[ii]] = viridis.colors[ii]
    return color_map

# In[ ] SCCT BRANCH-BY-BRANCH
from lib_prj.visualize import linear_regression_plot
from lib_prj.visualize import get_line_from_axis
import numpy as np
import seaborn as sns
import raw_data_samp1
import raw_data_samp10
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import cm





pd_scct_1 = raw_data_samp1.pd_scct
pd_scct_10 = raw_data_samp10.pd_scct

pd_comb = pd_scct_1.merge(pd_scct_10, how='left', on=['confirm_idc', 'id_vessel'])

np_id_vessels = pd_comb['id_vessel'].unique()
vessel_cm = make_color_map(list(np_id_vessels))
pd_comb['vessel_cm'] = pd_comb['id_vessel'].map(vessel_cm)

# sns.set_theme()
# plt.style.use('fivethirtyeight')

m_fig = plt.figure(figsize=(10,6))
c_ax = plt.axes()
for ii in np_id_vessels:
    setup_dict = {
        'ax' : c_ax,
        'data' : pd_comb[pd_comb['id_vessel'] == ii],
        'x' : 'mass_mcp_perc_1', 'y' : 'mass_mcp_perc_10',
        'color' : vessel_cm[ii],
        # 'color' : "dodgerblue",
       }
    c_ax = linear_regression_plot(setup_dict)
sns.lineplot(x=[0, 50], y=[0, 50], linewidth=2, ax=c_ax)
# STYLIZE
c_ax.set_ylabel('Mass (%) [10]', fontname='arial', fontweight='bold', fontsize=20)
c_ax.set_xlabel('Mass (%) [1]', fontname='arial', fontweight='bold', fontsize=20)
c_ax.set_xlim([-1, 50])
c_ax.set_ylim([-1, 50])
# plt.setp(c_ax.get_xticklabels(), fontname='arial', fontsize=25, fontweight='bold', rotation=45)
# plt.setp(c_ax.get_yticklabels(), fontname='arial', fontsize=25, fontweight='bold', )
plt.tight_layout()

# MODIFY AXIS GRID
c_ax = _set_ax(c_ax)

# In[ ] TABLE 1 - MASS COMPARISON
from lib_prj.visualize import table_scct_confirm
# import numpy as np
# from functools import reduce

m_fig = plt.figure()
c_ax = plt.axes()
xx = pd_scct_1[['id_vessel', 'mass_mcp_perc_1']].rename(columns={'mass_mcp_perc_1': 'mmar'})
tbl = table_scct_confirm(xx, ['id_vessel'], ax=c_ax, lbls = [ 'Vessel ID', 'N', 'Mass Percent (%)'])

# In[ ] TABLE 1 - MASS COMPARISON
from lib_prj.visualize import table_scct_confirm
# import numpy as np
# from functools import reduce

m_fig = plt.figure()
c_ax = plt.axes()
xx = pd_scct_10[['id_vessel', 'mass_mcp_perc_10']].rename(columns={'mass_mcp_perc_10': 'mmar'})
tbl = table_scct_confirm(xx, ['id_vessel'], ax=c_ax, lbls = [ 'Vessel ID', 'N', 'Mass Percent (%)'])

# In[ ] TABLE 1 - MASS COMPARISON
from lib_prj.visualize import table_scct_confirm
# import numpy as np
# from functools import reduce

m_fig = plt.figure()
c_ax = plt.axes()
pd_comb['diff'] = pd_comb['mass_mcp_perc_10'] - pd_comb['mass_mcp_perc_1']
xx = pd_comb[['id_vessel', 'diff']].rename(columns={'diff': 'mmar'})
tbl = table_scct_confirm(xx, ['id_vessel'], ax=c_ax, lbls = [ 'Vessel ID', 'N', 'Mass Percent (%)'])
