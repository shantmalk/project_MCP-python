# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 23:57:01 2020

@author: smalk
"""

import raw_data_cre
import lib_prj
from plotly.offline import plot

# In[ ] Visualize basic MCP parameters
pd_mmar = raw_data_cre.PD_MMAR

fig_title = 'MMAR-LV'
args_plotly = {
    'x' : 'id_main_vessel',
    'y' : 'mass_mcp_perc_lv',
    'points' : 'all',   
    'color' : 'id_main_vessel',
    'title' : fig_title,
    }
fig = lib_prj.visualize.boxplot_plotly(pd_mmar, args_plotly, '')
fig.update_yaxes(title='MMAR (%)')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=fig_title.replace('-', '_') + '.html')

# In[ ] Visualize basic MCP parameters
pd_mmar = raw_data_cre.PD_MMAR

fig_title = 'MMAR-REGIONAL'
args_plotly = {
    'x' : 'id_main_vessel',
    'y' : 'mass_mcp_perc_reg',
    'points' : 'all',   
    'color' : 'id_main_vessel',
    'title' : fig_title,
    }
fig = lib_prj.visualize.boxplot_plotly(pd_mmar, args_plotly, '')
fig.update_yaxes(title='MMAR (%)')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=fig_title.replace('-', '_') + '.html')

# In[ ] Visualize basic CRE-PERFUSION parameters
pd_combined = raw_data_cre.PD_COMBINED

fig_title = 'CRE-MPI_SDS'
args_plotly = { 
    'x' : 'id_main_vessel',
    'y' : 'mpi_sds_percent_vessel',
    'points' : 'all',   
    'color' : 'id_main_vessel',
    'title' : fig_title,
    }
fig = lib_prj.visualize.boxplot_plotly(pd_combined, args_plotly, '')
fig.update_yaxes(title='SDS')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=fig_title.replace('-', '_') + '.html')

# In[ ] Visualize basic CRE-PERFUSION parameters
pd_combined = raw_data_cre.PD_COMBINED

fig_title = 'CRE-MPI_SSS'
args_plotly = { 
    'x' : 'id_main_vessel',
    'y' : 'mpi_sss_percent_vessel',
    'points' : 'all',   
    'color' : 'id_main_vessel',
    'title' : fig_title,
    }
fig = lib_prj.visualize.boxplot_plotly(pd_combined, args_plotly, '')
fig.update_yaxes(title='SSS')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=fig_title.replace('-', '_') + '.html')

# In[ ] Visualize correspondence between MMAR and MPI

fig_title = 'MMAR vs SDS'
args_plotly = { 
    'x' : 'mpi_sds_percent_vessel',
    'y' : 'mass_mcp_perc_reg',
    'title' : fig_title,
    'trendline' : 'ols',
    }
fig = lib_prj.visualize.scatter_plotly(pd_combined, args_plotly, '')
plot_url = plot(fig, filename=fig_title.replace('-', '_') + '.html')

# In[ ] Visualize correspondence between MMAR and MPI

# pd_filt = pd_combined.loc[(pd_combined['id_main_vessel'] == 'lad') & (pd_combined['vess_maxles_lumenareasten'] > 50)]
fig_title = 'MMAR vs SSS'
args_plotly = { 
    'x' : 'mpi_sss_percent_vessel',
    'y' : 'mass_mcp_perc_reg',
    'color' : 'id_main_vessel',
    'title' : fig_title,
    'trendline' : 'ols',
    }
fig = lib_prj.visualize.scatter_plotly(pd_combined, args_plotly, '')
plot_url = plot(fig, filename=fig_title.replace('-', '_') + '.html')

# In[ ] Visualize correspondence between MMAR and FFR

# pd_filt = pd_combined.loc[(pd_combined['id_main_vessel'] == 'lad') & (pd_combined['vess_maxles_lumenareasten'] > 50)]
pd_filt = pd_combined.loc[(pd_combined['ffrct_val'] > 0) or (pd_combined['ffrct_val'] != 'NA')]
fig_title = 'MMAR vs FFR'
args_plotly = { 
    'x' : 'ffrct_val',
    'y' : 'mass_mcp_perc_lv',
    'color' : 'id_main_vessel',
    'title' : fig_title,
    'trendline' : 'ols',
    }
fig = lib_prj.visualize.scatter_plotly(pd_filt, args_plotly, '')
plot_url = plot(fig, filename=fig_title.replace('-', '_') + '.html')

# In[ ] Visualize basic CRE-VESSEL parameters
pd_combined = raw_data_cre.PD_COMBINED

fig_title = 'CRE-FFRCT'
args_plotly = { 
    'x' : 'id_main_vessel',
    'y' : 'ffrct_val',
    'points' : 'all',   
    'color' : 'id_main_vessel',
    'title' : fig_title,
    }
fig = lib_prj.visualize.boxplot_plotly(pd_combined, args_plotly, '')
fig.update_yaxes(title='FFR<sub>CT</sub>')
fig.update_xaxes(title='')
plot_url = plot(fig, filename=fig_title.replace('-', '_') + '.html')