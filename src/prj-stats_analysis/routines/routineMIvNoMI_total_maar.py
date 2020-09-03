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
    
    lib_prj.visualize.print_label('routineMIvNoMI_total_maar')
    
    # ------------------------------- PARSE -------------------------------- #
    
    # TODO:  Streamline parameters to qsel_parse to be qsel_parse(FILENAME, KEY) - Implicit PATH_DB since it is a global variable anyways
    fpath_json = lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_mitype')
    fkey_json = 'total_maar_unmatched'
    
    
    fpath_json_tmp = lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_general')
    fkey_json_tmp = 'tmp_query'
    pd_qsel_data = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, fpath_json_tmp, fkey_json_tmp) 
    
    # ------------------------------ PROCESS ------------------------------- #
    # Manipulate  pd_qsel_data as needed
    
    # Add dummy variables
    pd_qsel_data['mi_type_mi'] = np.where(pd_qsel_data['mi_event'] == 1, 1, 0)    # MI
    pd_qsel_data['mi_type_no_mi'] = np.where(pd_qsel_data['mi_event'] == 0, 1, 0)   # No MI
    
    conds = [
        (pd_qsel_data['mi_event'] == 1),
        (pd_qsel_data['mi_event'] == 0),
        ]
    vals = ['MI', 'No MI']
    
    pd_qsel_data['mi_type_str'] = np.select(conds, vals)
    
    # Sort data for intuitive viewing
    pd_qsel_data = pd_qsel_data.sort_values(by='mi_event',ascending=False)
    
    # Perform ANOVA analysis
    # stats_anova_mass_lv_g = lib_prj.process.stats_anova(pd_qsel_data, ['mi_type_stemi', 'mi_type_nstemi', 'mi_type_uangina', 'mi_type_unknown'], 'SumOfmass_lv_g')
    stats_anova_mass_mcp_g = lib_prj.process.stats_anova(pd_qsel_data, ['mi_type_mi', 'mi_type_no_mi',], 'SumOfmass_mcp_g')
    stats_anova_mass_mcp_perc = lib_prj.process.stats_anova(pd_qsel_data, ['mi_type_mi', 'mi_type_no_mi',], 'SumOfmass_mcp_perc')
    
    
    # Make pivot table
    pd_qsel_pivot_totals = pd.pivot_table(pd_qsel_data, index='mi_type_str', aggfunc=len, values=['confirm_idc_str'])
    pd_qsel_pivot_totals.columns = ['total_patients']
    pd_qsel_pivot_totals.reset_index(inplace=True)
    
    pd_qsel_pivot_mean = pd.pivot_table(pd_qsel_data, index='mi_type_str', aggfunc="mean", values=['SumOfmass_mcp_g', 'SumOfmass_mcp_perc'])
    pd_qsel_pivot_mean.columns = [x + '_mean' for x in ['SumOfmass_mcp_g', 'SumOfmass_mcp_perc']]
    pd_qsel_pivot_mean.reset_index(inplace=True)
    
    pd_qsel_pivot_std = pd.pivot_table(pd_qsel_data, index='mi_type_str', aggfunc=np.std, values=['SumOfmass_mcp_g', 'SumOfmass_mcp_perc'])
    pd_qsel_pivot_std.columns = [x + '_std' for x in ['SumOfmass_mcp_g', 'SumOfmass_mcp_perc']]
    pd_qsel_pivot_std.reset_index(inplace=True)
    
    # Merge pivot tables
    pd_qsel_pivot_list = [pd_qsel_pivot_totals, pd_qsel_pivot_mean, pd_qsel_pivot_std]
    # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    pd_qsel_pivot = reduce(lambda left,right: pd.merge(left, right, on=['mi_type_str'],how='outer',), pd_qsel_pivot_list)   
    
    # ------------------------------ VISUALIZE ----------------------------- #
    # Visualization of pd_qsel_data
    
    # TABLES:
        
    # Print per-patient data for debugging
    print(tabulate(pd_qsel_data, headers='keys', tablefmt='psql'))
    # Print mean data
    print(tabulate(pd_qsel_pivot, headers='keys', tablefmt='psql'))
    # Print ANOVA tables
    # print('\nANOVA - LV Mass (g)')
    # print(stats_anova_mass_lv_g)
    print('\nANOVA - MCP Mass (g)')
    print(stats_anova_mass_mcp_g)
    print('\nANOVA - MCP Mass (%)')
    print(stats_anova_mass_mcp_perc)
    
    # FIGURES:

    lib_prj.paths.make_directory(path_wr)    
    args_plotly = {
        'x' : 'mi_type_str',
        'points' : 'all',
        'color' : 'mi_type_str',
        'labels' : {'mi_type_str' : 'MI Type'},
        }
    
    
    # ------------------------------- PLOT 1 ------------------------------- #
    args_plotly['y'] = ['mass_lv_g']
    args_plotly['title'] = 'Box Plot - LV Mass'
    
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title='Mass (g)')
    if len(path_wr) > 0:   
        plot_url = plot(fig, filename=path_wr + 'boxplot_mitype_lv_mass.html')
    else:
        lib_prj.visualize.plot_plotly(fig, args_plotly['y'][0] + '.html')
    
    # ------------------------------- PLOT 2 ------------------------------- #
    args_plotly['y'] = ['SumOfmass_mcp_g']
    args_plotly['title'] = 'Box Plot - MCP Total MAAR'

    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title='Mass (g)')
    if len(path_wr) > 0:   
        plot_url = plot(fig, filename=path_wr + 'boxplot_mitype_mcp_mass.html')
    else:
        lib_prj.visualize.plot_plotly(fig, args_plotly['y'][0] + '.html')
    
    # ------------------------------- PLOT 3 ------------------------------- #
    args_plotly['y'] = ['SumOfmass_mcp_perc']
    args_plotly['title'] = 'Box Plot - MCP Total MAAR Percent'
    
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title='Mass Percent (%)')
    if len(path_wr) > 0:   
        plot_url = plot(fig, filename=path_wr + 'boxplot_mitype_mcp_perc_mass.html')
    else:
        lib_prj.visualize.plot_plotly(fig, args_plotly['y'][0] + '.html')
    
    # ------------------------------- PLOT 4 ------------------------------- #
    args_plotly['y'] = ['CountOfid_vessel_study']
    args_plotly['title'] = 'Box Plot - Number of Lesions'
    args_plotly['points'] = None
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title='# of Lesions')
    if len(path_wr) > 0:   
        plot_url = plot(fig, filename=path_wr + 'boxplot_mitype_nlesions.html')
    else:
        lib_prj.visualize.plot_plotly(fig, args_plotly['y'][0] + '.html')
        
    # ----------------------------- WRITE FILE ----------------------------- #
    
    # Save visualization to file
    # if len(path_wr) > 0:
    #     pass
    
    
if __name__ == '__main__':
   pd_test = run()