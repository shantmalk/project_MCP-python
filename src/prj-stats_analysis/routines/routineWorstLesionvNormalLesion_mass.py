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
    
    lib_prj.visualize.print_label('routineWorstLesionvNormalLesion_mass')
    
    # ------------------------------- PARSE -------------------------------- #
    
    # TODO:  Streamline parameters to qsel_parse to be qsel_parse(FILENAME, KEY) - Implicit PATH_DB since it is a global variable anyways
    # Maybe leave as is, its probably better to have EXPLICIT definition of a file path rather than define it within the function.
    fpath_json = lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_culprit_lesion_char')
    fkey_json_noqc = 'mi_lesion_mass'
    fkey_json_qc = 'mi_lesion_mass_qc' # JSON QUERY WITH QUALITY-CONTROL FILTERING ENABLED - REMOVES PATIENT DATA WITH INVALID MCP CALCULATIONS
    # pd_qsel_data = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, fpath_json, fkey_json) 
    
    pd_qsel_data = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, fpath_json, fkey_json_qc)
    
    # ------------------------------ PROCESS ------------------------------- #
    # Manipulate  pd_qsel_data as needed
    
    # Add dummy variables
    pd_qsel_data['lesion_type_worst'] = np.where(pd_qsel_data['lesion_worst'] == 1, 1, 0)    # MI
    pd_qsel_data['lesion_type_not_worst'] = np.where(pd_qsel_data['lesion_worst'] == 0, 1, 0)   # No MI
    
    conds = [
        (pd_qsel_data['lesion_worst'] == 1),
        (pd_qsel_data['lesion_worst'] == 0),
        ]
    vals = ['Culprit Lesions', 'Non-Culprit Lesions']
    
    pd_qsel_data['lesion_worst_str'] = np.select(conds, vals)
    
    # Sort data for intuitive viewing
    pd_qsel_data = pd_qsel_data.sort_values(by='lesion_worst',ascending=False)
    
    # Perform ANOVA analysis
    # stats_anova_mass_lv_g = lib_prj.process.stats_anova(pd_qsel_data, ['mi_type_stemi', 'mi_type_nstemi', 'mi_type_uangina', 'mi_type_unknown'], 'SumOfmass_lv_g')
    stats_anova_mass_mcp_g = lib_prj.process.stats_anova(pd_qsel_data, ['lesion_type_worst', 'lesion_type_not_worst',], 'mass_mcp_g')
    stats_anova_mass_mcp_perc = lib_prj.process.stats_anova(pd_qsel_data, ['lesion_type_worst', 'lesion_type_not_worst',], 'mass_mcp_perc')
    
    
    # Make pivot table
    pd_qsel_pivot_totals = pd.pivot_table(pd_qsel_data, index='lesion_worst_str', aggfunc=len, values=['confirm_idc_str'])
    pd_qsel_pivot_totals.columns = ['total_lesions']
    pd_qsel_pivot_totals.reset_index(inplace=True)
    
    pd_qsel_pivot_mean = pd.pivot_table(pd_qsel_data, index='lesion_worst_str', aggfunc="mean", values=['mass_mcp_g', 'mass_mcp_perc'])
    pd_qsel_pivot_mean.columns = [x + '_mean' for x in ['mass_mcp_g', 'mass_mcp_perc']]
    pd_qsel_pivot_mean.reset_index(inplace=True)
    
    pd_qsel_pivot_std = pd.pivot_table(pd_qsel_data, index='lesion_worst_str', aggfunc=np.std, values=['mass_mcp_g', 'mass_mcp_perc'])
    pd_qsel_pivot_std.columns = [x + '_std' for x in ['mass_mcp_g', 'mass_mcp_perc']]
    pd_qsel_pivot_std.reset_index(inplace=True)
    
    # Merge pivot tables
    pd_qsel_pivot_list = [pd_qsel_pivot_totals, pd_qsel_pivot_mean, pd_qsel_pivot_std]
    # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    pd_qsel_pivot = reduce(lambda left,right: pd.merge(left, right, on=['lesion_worst_str'],how='outer',), pd_qsel_pivot_list)   
    
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
        
    # TODO:  FIGURE OUT HOW TO EDIT THE HOVER DATA - THIS WILL BE VERY HELPFUL
    lib_prj.paths.make_directory(path_wr)    
    args_plotly = {
        'x' : 'lesion_worst_str',
        'points' : 'all',
        'color' : 'lesion_worst_str',
        'labels' : {'lesion_worst_str' : 'Lesion Type'},
        'hover_name' : 'confirm_idc_str',
        'hover_data' : {
                        'lesion_worst_str' : True,
                        }
        }
    
    
    # ------------------------------- PLOT 1 ------------------------------- #
    # args_plotly['y'] = ['mass_lv_g']
    # args_plotly['title'] = 'Box Plot - LV Mass'
    
    # fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    # fig.update_yaxes(title='Mass (g)')
    # if len(path_wr) > 0:   
    #     plot_url = plot(fig, filename=path_wr + 'boxplot_mitype_lv_mass.html')
    # else:
    #     lib_prj.visualize.plot_plotly(fig, args_plotly['y'][0] + '.html')
    
    # ------------------------------- PLOT 2 ------------------------------- #
    args_plotly['y'] = ['mass_mcp_g']
    args_plotly['title'] = 'Box Plot - Culprit Versus Non-Culprit Lesion - MCP Total MAAR'

    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title='Mass (g)')
    if len(path_wr) > 0:   
        plot_url = plot(fig, filename=path_wr + 'boxplot_mitype_mcp_mass.html')
    else:
        lib_prj.visualize.plot_plotly(fig, args_plotly['y'][0] + '.html')
    
    # ------------------------------- PLOT 3 ------------------------------- #
    args_plotly['y'] = ['mass_mcp_perc']
    args_plotly['title'] = 'Box Plot - Culprit Versus Non-Culprit Lesion - MCP Total MAAR Percent'
    
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title='Mass Percent (%)')
    if len(path_wr) > 0:   
        plot_url = plot(fig, filename=path_wr + 'boxplot_mitype_mcp_perc_mass.html')
    else:
        lib_prj.visualize.plot_plotly(fig, args_plotly['y'][0] + '.html')
            
    # ----------------------------- WRITE FILE ----------------------------- #
    
    # Save visualization to file
    # if len(path_wr) > 0:
    #     pass
    
    
if __name__ == '__main__':
   pd_test = run()