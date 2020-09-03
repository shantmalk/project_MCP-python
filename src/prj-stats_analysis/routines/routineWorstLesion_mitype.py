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
    This script analyzes all lesions found for patients in the CONFIRM study.
    Comparison is done between the MCP mass of "culprit" lesions and "non-culprit" lesions for STEMI, NSTEMI, UA, and IND groups
    
    INPUTS
        path_wr     [STR | Directory where visualization data can be saved *OPTIONAL*; if not specified, no data will be written]
    '''
    
    lib_prj.visualize.print_label('routineMIType_worstlesion')
    
    # ------------------------------- PARSE -------------------------------- #
    fpath_json = lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_culprit_lesion_char')
    fkey_json = 'mi_lesion_mass_qc'
    
    fpath_json_tmp = lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_culprit_lesion_char')
    fkey_json_tmp = 'mi_lesion_mass_qc_lad'
    
    
    # pd_qsel_data = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, fpath_json, fkey_json) 
    pd_qsel_data = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, fpath_json_tmp, fkey_json_tmp) 
    pd_qsel_data = pd_qsel_data.replace(r'^\s*$', '0', regex=True)
    
    # ------------------------------ PROCESS ------------------------------- #
    # Manipulate  pd_qsel_data as needed
    
    # Add dummy variables - mi_type
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
    
    # Add dummy variables - lesion_worst
    pd_qsel_data['lesion_type_worst'] = np.where(pd_qsel_data['lesion_worst'] == 1, 1, 0)    # MI
    pd_qsel_data['lesion_type_not_worst'] = np.where(pd_qsel_data['lesion_worst'] == 0, 1, 0)   # No MI
    
    conds = [
        (pd_qsel_data['lesion_worst'] == 1),
        (pd_qsel_data['lesion_worst'] == 0),
        ]
    vals = ['Culprit Lesions', 'Non-Culprit Lesions']
    
    pd_qsel_data['lesion_worst_str'] = np.select(conds, vals)
    
    
    # Perform ANOVA analysis
    stats_anova_mass_lv_g = lib_prj.process.stats_anova(pd_qsel_data, ['lesion_type_worst', 'lesion_type_not_worst', ], 'mass_lv_g')
    stats_anova_mass_mcp_g = lib_prj.process.stats_anova(pd_qsel_data, ['lesion_type_worst', 'lesion_type_not_worst', ], 'mass_mcp_g')
    stats_anova_mass_mcp_perc = lib_prj.process.stats_anova(pd_qsel_data, ['lesion_type_worst', 'lesion_type_not_worst', ], 'mass_mcp_perc')
    
    anova_grps = ['mi_type_stemi', 'mi_type_nstemi', 'mi_type_uangina']
    for ii in range(len(anova_grps)):
        # stats_anova_mass_lv_g = lib_prj.process.stats_anova(pd_qsel_data.loc[anova_grps[ii] == 1], ['lesion_type_worst', 'lesion_type_not_worst', ], 'mass_lv_g')
        # stats_anova_mass_mcp_g = lib_prj.process.stats_anova(pd_qsel_data.loc[anova_grps[ii] == 1], ['lesion_type_worst', 'lesion_type_not_worst', ], 'mass_mcp_g')
        # stats_anova_mass_mcp_perc = lib_prj.process.stats_anova(pd_qsel_data.loc[anova_grps[ii] == 1], ['lesion_type_worst', 'lesion_type_not_worst', ], 'mass_mcp_perc')
        print('==============================================================')
        print('ANOVA -------- LV Mass ----------- ' + anova_grps[ii])
        print(lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps[ii]] == 1], ['lesion_type_worst', 'lesion_type_not_worst', ], 'mass_lv_g'))
        print()
        print('ANOVA -------- MCP Mass (g) ------ ' + anova_grps[ii])
        print(lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps[ii]] == 1], ['lesion_type_worst', 'lesion_type_not_worst', ], 'mass_mcp_g'))
        print()
        print('ANOVA -------- MCP Mass (%) ------ ' + anova_grps[ii])
        print(lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps[ii]] == 1], ['lesion_type_worst', 'lesion_type_not_worst', ], 'mass_mcp_perc'))
        print()
    # Make pivot table
    pd_qsel_pivot_totals = pd.pivot_table(pd_qsel_data, index=['mi_type_str', 'lesion_worst', ], aggfunc=len, values=['confirm_idc_str'])
    pd_qsel_pivot_totals.columns = ['total_lesions']
    pd_qsel_pivot_totals.reset_index(inplace=True)
    
    pd_qsel_pivot_mean = pd.pivot_table(pd_qsel_data, index=['mi_type_str', 'lesion_worst', ], aggfunc="mean", values=['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc'])
    pd_qsel_pivot_mean.columns = [x + '_mean' for x in ['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc']]
    pd_qsel_pivot_mean.reset_index(inplace=True)
    
    pd_qsel_pivot_std = pd.pivot_table(pd_qsel_data, index=['mi_type_str', 'lesion_worst', ], aggfunc=np.std, values=['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc'])
    pd_qsel_pivot_std.columns = [x + '_std' for x in ['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc']]
    pd_qsel_pivot_std.reset_index(inplace=True)
    
    # Merge pivot tables
    pd_qsel_pivot_list = [pd_qsel_pivot_totals, pd_qsel_pivot_mean, pd_qsel_pivot_std]
    # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    pd_qsel_pivot = reduce(lambda left,right: pd.merge(left, right, on=['mi_type_str', 'lesion_worst', ],how='outer',), pd_qsel_pivot_list)   
    
    # ------------------------------ VISUALIZE ----------------------------- #
    # Visualization of pd_qsel_data
    
    # TABLES:
        
    # Print per-patient data for debugging
    # print(tabulate(pd_qsel_data, headers='keys', tablefmt='psql'))
    # Print mean data
    print(tabulate(pd_qsel_pivot, headers='keys', tablefmt='psql'))
    # Print ANOVA tables
    # print('\nANOVA - LV Mass (g)')
    # print(stats_anova_mass_lv_g)
    # print('\nANOVA - MCP Mass (g)')
    # print(stats_anova_mass_mcp_g)
    # print('\nANOVA - MCP Mass (%)')
    # print(stats_anova_mass_mcp_perc)
    
    # FIGURES:
    lib_prj.paths.make_directory(path_wr) 
    
    pd_qsel_data = pd_qsel_data.sort_values(by='mi_type')
    args_plotly = {
        'x' : 'mi_type_str',
        'points' : 'all',
        'color' : 'lesion_worst_str',
        'labels' : {'lesion_worst_str' : 'Lesion Type'},
        }
    
    # ------------------------------- PLOT 1 ------------------------------- #
    # LV Mass for this study is not necessary.
    
    # args_plotly['y'] = ['mass_lv_g']
    # args_plotly['title'] = 'Box Plot - LV Mass'
    
    # fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    # fig.update_yaxes(title='Mass (g)')
    
    # # Save file if path specified
    # if len(path_wr) > 0:   
    #     plot_url = plot(fig, filename=path_wr + 'boxplot_mitype_lv_mass.html')
    # else:
    #     lib_prj.visualize.plot_plotly(fig, args_plotly['y'][0] + '.html')
    
    
    # ------------------------------- PLOT 2 ------------------------------- #
    args_plotly['y'] = ['mass_mcp_g']
    args_plotly['title'] = 'Box Plot - MCP Mass of Culprit versus Non-Culprit Lesions'

    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title='Mass (g)')
    
    # Save file if path specified
    if len(path_wr) > 0:   
        plot_url = plot(fig, filename=path_wr + 'boxplot_mitype_mcp_mass.html')
    else:
        lib_prj.visualize.plot_plotly(fig, args_plotly['y'][0] + '.html')
    
    # ------------------------------- PLOT 3 ------------------------------- #
    args_plotly['y'] = ['mass_mcp_perc']
    args_plotly['title'] = 'Box Plot - MCP Mass Percent of Culprit versus Non-Culprit Lesions'
    
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title='Mass Percent (%)')
    
    # Save file if path specified
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