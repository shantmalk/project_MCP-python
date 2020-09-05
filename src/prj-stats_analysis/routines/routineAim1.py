# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 11:04:15 2020

@author: smDesktop
"""


import lib_prj
import pandas as pd
# ADD ADDT LIBRARIES AS NEEDED
import numpy as np
from tabulate import tabulate
from functools import reduce
from plotly.offline import plot


def run(path_wr=''):
    '''
    Basic routine for visualizing processing status of patients for CONFIRM study
    
    INPUTS
        path_wr     [STR | Directory where visualization data can be saved *OPTIONAL*; if not specified, no data will be written]
    '''
    
    lib_prj.visualize.print_label('routineMIType_worstlesion')
    
    # ------------------------------- PARSE -------------------------------- #
    fpath_json = lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_mi_versus_nomi')
    fkey_json = 'worstlesion_unmatched'
    
    pd_qsel_data = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, fpath_json, fkey_json)
    pd_qsel_data = pd_qsel_data.replace(r'^\s*$', '0', regex=True)
    
    # ------------------------------ PROCESS ------------------------------- #
    # Manipulate  pd_qsel_data as needed
    
    # Add dummy variables
    pd_qsel_data['mi_type_stemi'] = np.where(pd_qsel_data['mi_type'] == "1", 1, 0)    # STEMI
    pd_qsel_data['mi_type_nstemi'] = np.where(pd_qsel_data['mi_type'] == "2", 1, 0)   # NSTEMI
    pd_qsel_data['mi_type_uangina'] = np.where(pd_qsel_data['mi_type'] == "4", 1, 0)  # UNSTABLE ANGINA (CHEST PAIN W/O TROPONIN)
    pd_qsel_data['mi_type_unknown'] = np.where(pd_qsel_data['mi_type'] == "3", 1, 0)  # UNKNOWN MI TYPE
    pd_qsel_data['mi_type_none'] = np.where(pd_qsel_data['mi_event'] == 0, 1, 0)   # NO MI
    
    conds = [
        (pd_qsel_data['mi_type'] == '1'),
        (pd_qsel_data['mi_type'] == '2'),
        (pd_qsel_data['mi_type'] == '3'),
        (pd_qsel_data['mi_type'] == '4'),
        (pd_qsel_data['mi_event'] == 0),
        ]
    vals = ['STEMI', 'NSTEMI', 'IND', 'UA', 'No MI']
    
    pd_qsel_data['mi_type_str'] = np.select(conds, vals)
    
    # Perform ANOVA analysis
    stats_anova_mass_lv_g = lib_prj.process.stats_anova(pd_qsel_data, ['mi_type_stemi', 'mi_type_nstemi', 'mi_type_uangina', 'mi_type_unknown', 'mi_type_none'], 'mass_lv_g')
    stats_anova_mass_mcp_g = lib_prj.process.stats_anova(pd_qsel_data, ['mi_type_stemi', 'mi_type_nstemi', 'mi_type_uangina', 'mi_type_unknown', 'mi_type_none'], 'mass_mcp_g')
    stats_anova_mass_mcp_perc = lib_prj.process.stats_anova(pd_qsel_data, ['mi_type_stemi', 'mi_type_nstemi', 'mi_type_uangina', 'mi_type_unknown', 'mi_type_none'], 'mass_mcp_perc')
    
    
    # Make pivot table
    pd_qsel_pivot_totals = pd.pivot_table(pd_qsel_data, index='mi_event', aggfunc=len, values=['id_vessel_study'])
    pd_qsel_pivot_totals.columns = ['total_patients']
    pd_qsel_pivot_totals.reset_index(inplace=True)
    
    pd_qsel_pivot_mean = pd.pivot_table(pd_qsel_data, index='mi_event', aggfunc="mean", values=['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc'])
    pd_qsel_pivot_mean.reset_index(inplace=True)
    
    pd_qsel_pivot_std = pd.pivot_table(pd_qsel_data, index='mi_event', aggfunc=np.std, values=['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc'])
    pd_qsel_pivot_std.columns = [x + '_std' for x in ['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc']]
    pd_qsel_pivot_std.reset_index(inplace=True)
    
    # Merge pivot tables
    pd_qsel_pivot_list = [pd_qsel_pivot_totals, pd_qsel_pivot_mean, pd_qsel_pivot_std]
    # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    pd_qsel_pivot = reduce(lambda left,right: pd.merge(left, right, on=['mi_event'],how='outer',), pd_qsel_pivot_list)   
    
    # ------------------------------ VISUALIZE ----------------------------- #
    # Visualization of pd_qsel_data
    
    # TABLES:
        
    # Print per-patient data for debugging
    print(tabulate(pd_qsel_data, headers='keys', tablefmt='psql'))
    # Print mean data
    print(tabulate(pd_qsel_pivot, headers='keys', tablefmt='psql'))
    # Print ANOVA tables
    print('\nANOVA - LV Mass (g)')
    print(stats_anova_mass_lv_g)
    print('\nANOVA - MCP Mass (g)')
    print(stats_anova_mass_mcp_g)
    print('\nANOVA - MCP Mass (%)')
    print(stats_anova_mass_mcp_perc)
    
    # FIGURES:
    lib_prj.paths.make_directory(path_wr) 
    
    pd_qsel_data = pd_qsel_data.sort_values(by='mi_type')
    args_plotly = {
        'x' : 'mi_event',
        'points' : 'all',
        'color' : 'mi_event',
        'labels' : {'mi_type_str' : 'MI Type'},
        }
    
    path_analysis_png = lib_prj.paths.PATH_ANALYSIS_FIG_PNG
    path_analysis_html = lib_prj.paths.PATH_ANALYSIS_FIG_HTML
    
    # ------------------------------ FIGURE 2A ----------------------------- #
    args_plotly['y'] = ['mass_mcp_g']
    args_plotly['title'] = 'Figure 2A: Box plot of MAAR<sub>MCP (abs)</sub> of MI and no MI groups'

    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title='Mass (g)')
    
    # Save file if path specified
    plot_url = plot(fig, filename=path_analysis_html + 'figure2a.html')
    fig.write_image(path_analysis_png + 'figure2a.png')
    
    
    # ------------------------------- PLOT 2B ------------------------------- #
    args_plotly['y'] = ['mass_mcp_perc']
    args_plotly['title'] = 'Figure 2B: Box plot of MAAR<sub>MCP (rel)</sub> of MI and no MI groups'
    
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title='Mass Percent (%)')
    
    # Save file if path specified
    plot_url = plot(fig, filename=path_analysis_html + 'figure2b.html')
    fig.write_image(path_analysis_png + 'figure2b.png')
        
    
    
if __name__ == '__main__':
   pd_test = run()