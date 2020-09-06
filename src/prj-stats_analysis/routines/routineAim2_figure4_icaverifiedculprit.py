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
from collections import defaultdict as ddict


def run(path_wr=''):
    '''
    RESULTS ANALYSIS
    WORST_LESION FIELD USED TO SELECT CULPRIT LESION IN MI GROUP
    WORST_LESION FIELD USED TO SELECT POSSIBLE CULPRIT LESION IN NON-MI GROUP
    
    INPUTS
        path_wr     [STR | Directory where visualization data can be saved *OPTIONAL*; if not specified, no data will be written]
    '''
    
    path_analysis_png = lib_prj.paths.PATH_ANALYSIS + 'results-09052020-figs/png/'
    path_analysis_html = lib_prj.paths.PATH_ANALYSIS + 'results-09052020-figs/html/'
    
    lib_prj.visualize.print_label('routineAim2')
    
    # ------------------------------- PARSE -------------------------------- #
    
    fpath_json = lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_mi_versus_nomi')
    fkey_json = 'mi_all_lesions_unmatched'
    
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
    pd_qsel_data['mi_type_mi'] = np.where(pd_qsel_data['mi_event'] == 1, 1, 0) # MI
    
    pd_qsel_data['lesion_culprit'] = np.where(pd_qsel_data['lesion_culprit_ica_ct'] == '1', 1, 0)
    pd_qsel_data['lesion_nonculprit'] = np.where(pd_qsel_data['lesion_culprit_ica_ct'] == '1', 0, 1)
    
    pd_qsel_data['lesion_lad'] = np.where(pd_qsel_data['id_main_vessel'] == 'lad', 1, 0)
    pd_qsel_data['lesion_lcx'] = np.where(pd_qsel_data['id_main_vessel'] == 'lcx', 1, 0)
    pd_qsel_data['lesion_rca'] = np.where(pd_qsel_data['id_main_vessel'] == 'rca', 1, 0)
    
    conds = [
        (pd_qsel_data['mi_type'] == '1'),
        (pd_qsel_data['mi_type'] == '2'),
        (pd_qsel_data['mi_type'] == '3'),  
        (pd_qsel_data['mi_type'] == '4'),
        (pd_qsel_data['mi_event'] == 0),
        ]
    
    vals = ['STEMI', 'NSTEMI', 'IND', 'UA', 'No MI']
    pd_qsel_data['mi_type_str'] = np.select(conds, vals)
    
    pd_qsel_data['lesion_culprit_str'] = np.where(pd_qsel_data['lesion_culprit_ica_ct'] == '1', 'Culprit', 'Non-Culprit')
    
    
    # -------------- Calculate p-values, per-vessel grouping --------------- #
    pd_p_val_lv_mass = ddict()
    pd_p_val_mass_mcp_g = ddict()
    pd_p_val_mass_mcp_perc = ddict()
    
    anova_grps_b = ['lesion_culprit', 'lesion_nonculprit']
    anova_grps_a = ['mi_type_stemi', 'mi_type_nstemi', 'mi_type_uangina']
    for ii in range(len(anova_grps_a)):
        pd_p_val_lv_mass[anova_grps_a[ii]] = lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps_a[ii]] == 1], anova_grps_b, 'mass_lv_g')
        pd_p_val_mass_mcp_g[anova_grps_a[ii]] = lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps_a[ii]] == 1], anova_grps_b, 'mass_mcp_g')
        pd_p_val_mass_mcp_perc[anova_grps_a[ii]] = lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps_a[ii]] == 1], anova_grps_b, 'mass_mcp_perc')
        
        print('================================== {:^20} =================================='.format(anova_grps_a[ii]))
        print('ANOVA -------- LV Mass ----------- ')
        print(lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps_a[ii]] == 1], anova_grps_b, 'mass_lv_g'))
        print()
        print('ANOVA -------- MCP Mass (g) ------ ')
        print(lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps_a[ii]] == 1], anova_grps_b, 'mass_mcp_g'))
        print()
        print('ANOVA -------- MCP Mass (%) ------ ')
        print(lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps_a[ii]] == 1], anova_grps_b, 'mass_mcp_perc'))
        print()
    
    # -------------- Calculate p-values, all-vessel grouping --------------- #
    print('================================== {:^20} =================================='.format('All Lesions'))
    print('ANOVA -------- LV Mass ----------- ')
    pd_anova_all_lesions_mass_lv_g = lib_prj.process.stats_anova(pd_qsel_data, anova_grps_b, 'mass_lv_g')
    print(pd_anova_all_lesions_mass_lv_g)
    print()
    print('ANOVA -------- MCP Mass (g) ------ ')
    pd_anova_all_lesions_mcp_mass_g = lib_prj.process.stats_anova(pd_qsel_data, anova_grps_b, 'mass_mcp_g')
    print(pd_anova_all_lesions_mcp_mass_g)
    print()
    print('ANOVA -------- MCP Mass (%) ------ ')
    pd_anova_all_lesions_mcp_mass_perc = lib_prj.process.stats_anova(pd_qsel_data, anova_grps_b, 'mass_mcp_perc')
    print(pd_anova_all_lesions_mcp_mass_perc)
    print()
    
    # ------------------------- Save p-value tables ------------------------ #
    lib_prj.visualize.table_pvalues({'lesions_all' : pd_anova_all_lesions_mcp_mass_g}, path_analysis_png + 'p_val-figure4a.png')
    lib_prj.visualize.table_pvalues({'lesions_all' : pd_anova_all_lesions_mcp_mass_perc}, path_analysis_png + 'p_val-figure4b.png')
    lib_prj.visualize.table_pvalues(pd_p_val_mass_mcp_g, path_analysis_png + 'p_val-figure4c.png')
    lib_prj.visualize.table_pvalues(pd_p_val_mass_mcp_perc, path_analysis_png + 'p_val-figure4d.png')
    
    # ---------------------------- Pivot Table 1 --------------------------- #
    pivot_groups = ['mi_type_str', 'lesion_culprit_str']
    # Make pivot table
    pd_qsel_pivot_totals = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc=len, values=['confirm_idc_str'])
    pd_qsel_pivot_totals.columns = ['total_lesions']
    pd_qsel_pivot_totals.reset_index(inplace=True)
    
    pd_qsel_pivot_mean = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc="mean", values=['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc'])
    pd_qsel_pivot_mean.columns = [x + '_mean' for x in ['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc']]
    pd_qsel_pivot_mean.reset_index(inplace=True)
    
    pd_qsel_pivot_std = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc=np.std, values=['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc'])
    pd_qsel_pivot_std.columns = [x + '_std' for x in ['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc']]
    pd_qsel_pivot_std.reset_index(inplace=True)
    
    # Merge pivot tables
    pd_qsel_pivot_list = [pd_qsel_pivot_totals, pd_qsel_pivot_mean, pd_qsel_pivot_std]
    # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    pd_qsel_pivot = reduce(lambda left,right: pd.merge(left, right, on=pivot_groups,how='outer',), pd_qsel_pivot_list) 
    print(tabulate(pd_qsel_pivot.sort_values(by=['mi_type_str', 'lesion_culprit_str']), headers='keys', tablefmt='psql'))
    lib_prj.visualize.table_basic(pd_qsel_pivot.sort_values(by=['mi_type_str', 'lesion_culprit_str']), path_analysis_png + 'table4b.png', ['w', '#f1f1f2', '#f1f1f2', 'w',])
    
    # ---------------------------- Pivot Table 2 --------------------------- #
    pivot_groups = ['lesion_culprit_str',]
    # Make pivot table
    pd_qsel_pivot_totals = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc=len, values=['confirm_idc_str'])
    pd_qsel_pivot_totals.columns = ['total_lesions']
    pd_qsel_pivot_totals.reset_index(inplace=True)
    
    pd_qsel_pivot_mean = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc="mean", values=['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc'])
    pd_qsel_pivot_mean.columns = [x + '_mean' for x in ['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc']]
    pd_qsel_pivot_mean.reset_index(inplace=True)
    
    pd_qsel_pivot_std = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc=np.std, values=['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc'])
    pd_qsel_pivot_std.columns = [x + '_std' for x in ['mass_lv_g', 'mass_mcp_g', 'mass_mcp_perc']]
    pd_qsel_pivot_std.reset_index(inplace=True)
    
    # Merge pivot tables
    pd_qsel_pivot_list = [pd_qsel_pivot_totals, pd_qsel_pivot_mean, pd_qsel_pivot_std]
    # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    pd_qsel_pivot = reduce(lambda left,right: pd.merge(left, right, on=pivot_groups,how='outer',), pd_qsel_pivot_list) 
    print(tabulate(pd_qsel_pivot, headers='keys', tablefmt='psql'))
    lib_prj.visualize.table_basic(pd_qsel_pivot, path_analysis_png + 'table4a.png')
    # ------------------------------ VISUALIZE ----------------------------- #

    
    # FIGURES:
    lib_prj.paths.make_directory(path_wr) 
    
    
    
    
    # ------------------------- FIGURE 2A-B PARAMS ------------------------- #
    pd_qsel_data = pd_qsel_data.sort_values(by=['lesion_culprit_str', 'mi_type'])
    args_plotly = {
        'x' : 'lesion_culprit_str',
        'points' : 'all',
        'color' : 'lesion_culprit_str',
        'labels' : {'lesion_culprit_str' : 'Lesion Type'},
        }
    
    # ------------------------------ FIGURE 2A ----------------------------- #
    figure_label = 'Figure 4A'
    y_data = 'mass_mcp_g'
    y_label = 'Mass Percent (g)'
    title =  figure_label + ': Box plot of MAAR<sub>MCP (abs)</sub> of culprit and non-culprit lesions'
    
    figure_fname_label = figure_label.lower().replace(' ', '')
    args_plotly['y'] = [y_data]
    args_plotly['title'] = title
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title=y_label)
    
    fig.update_layout(showlegend=False)
    
    # Save file if path specified
    plot_url = plot(fig, filename=path_analysis_html + figure_fname_label + '.html')
    fig.write_image(path_analysis_png + figure_fname_label + '.png')
    
    # ------------------------------- PLOT 2B ------------------------------- #
    figure_label = 'Figure 4B'
    y_data = 'mass_mcp_perc'
    y_label = 'Mass Percent (%)'
    title =  figure_label + ': Box plot of MAAR<sub>MCP (rel)</sub> of culprit and non-culprit lesions'
    
    figure_fname_label = figure_label.lower().replace(' ', '')
    args_plotly['y'] = [y_data]
    args_plotly['title'] = title
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title=y_label)
    
    fig.update_layout(showlegend=False)
    
    # Save file if path specified
    plot_url = plot(fig, filename=path_analysis_html + figure_fname_label + '.html')
    fig.write_image(path_analysis_png + figure_fname_label + '.png')
    
    
    # ------------------------- FIGURE 2C-D PARAMS ------------------------- #
    pd_qsel_data = pd_qsel_data.sort_values(by='mi_type')
    args_plotly = {
        'x' : 'mi_type_str',
        'points' : 'all',
        'color' : 'lesion_culprit_str',
        'labels' : {'lesion_culprit_str' : 'Lesion Type'},
        }
    
    # ------------------------------ FIGURE 2C ----------------------------- #
    figure_label = 'Figure 4C'
    y_data = 'mass_mcp_g'
    y_label = 'Mass Percent (g)'
    x_label = 'MI Type' 
    title =  figure_label + ': Box plot of MAAR<sub>MCP (abs)</sub> of culprit and non-culprit lesions'
    
    
    figure_fname_label = figure_label.lower().replace(' ', '')
    args_plotly['y'] = [y_data]
    args_plotly['title'] = title
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title=y_label)
    fig.update_xaxes(title=x_label)
    # Save file if path specified
    plot_url = plot(fig, filename=path_analysis_html + figure_fname_label + '.html')
    fig.write_image(path_analysis_png + figure_fname_label + '.png')
    
    # ------------------------------- PLOT 2D ------------------------------- #
    figure_label = 'Figure 4D'
    y_data = 'mass_mcp_perc'
    y_label = 'Mass Percent (%)'
    x_label = 'MI Type'
    title =  figure_label + ': Box plot of MAAR<sub>MCP (rel)</sub> of culprit and non-culprit lesions'
    
    
    figure_fname_label = figure_label.lower().replace(' ', '')
    args_plotly['y'] = [y_data]
    args_plotly['title'] = title
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title=y_label)
    fig.update_xaxes(title=x_label)
    # Save file if path specified
    plot(fig, filename=path_analysis_html + figure_fname_label + '.html')
    fig.write_image(path_analysis_png + figure_fname_label + '.png')
        
if __name__ == '__main__':
   pd_test = run()