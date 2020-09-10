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
    icalesionverified FIELD USED TO SELECT CULPRIT LESION IN MI GROUP
    WORST_LESION FIELD USED TO SELECT POSSIBLE CULPRIT LESION IN NON-MI GROUP
    
    INPUTS
        path_wr     [STR | Directory where visualization data can be saved *OPTIONAL*; if not specified, no data will be written]
    '''
    
    path_analysis_png = lib_prj.paths.PATH_ANALYSIS + 'results-09052020-figs/png/'
    path_analysis_html = lib_prj.paths.PATH_ANALYSIS + 'results-09052020-figs/html/'
    lib_prj.visualize.print_label('routineAim1')
    
    # ------------------------------- PARSE -------------------------------- #
    
    # NON-MI GROUP
    fpath_json = lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_mi_versus_nomi')
    fkey_json = 'nomi_lesionworst_matched'
    
    pd_qsel_data_nomi = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, fpath_json, fkey_json)
    pd_qsel_data_nomi = pd_qsel_data_nomi.replace(r'^\s*$', '0', regex=True)
    pd_qsel_data_nomi = pd_qsel_data_nomi.rename(columns={'lesion_worst': 'lesion_sel'})
    
    # MI GROUP
    fpath_json = lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_mi_versus_nomi')
    fkey_json = 'mi_icalesionverified_matched'
    
    pd_qsel_data_mi = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, fpath_json, fkey_json)
    pd_qsel_data_mi = pd_qsel_data_mi.replace(r'^\s*$', '0', regex=True)
    pd_qsel_data_mi = pd_qsel_data_mi.rename(columns={'lesion_culprit_ica_ct' : 'lesion_sel'})
    
    # MERGE GROUPS
    pd_qsel_data = pd.concat([pd_qsel_data_nomi, pd_qsel_data_mi])
    
    # ------------------------------ PROCESS ------------------------------- #
    # Manipulate  pd_qsel_data as needed
    
    # Add dummy variables
    pd_qsel_data['mi_type_stemi'] = np.where(pd_qsel_data['mi_type'] == "1", 1, 0)    # STEMI
    pd_qsel_data['mi_type_nstemi'] = np.where(pd_qsel_data['mi_type'] == "2", 1, 0)   # NSTEMI
    pd_qsel_data['mi_type_uangina'] = np.where(pd_qsel_data['mi_type'] == "4", 1, 0)  # UNSTABLE ANGINA (CHEST PAIN W/O TROPONIN)
    pd_qsel_data['mi_type_unknown'] = np.where(pd_qsel_data['mi_type'] == "3", 1, 0)  # UNKNOWN MI TYPE
    pd_qsel_data['mi_type_none'] = np.where(pd_qsel_data['mi_event'] == 0, 1, 0)   # NO MI
    pd_qsel_data['mi_type_mi'] = np.where(pd_qsel_data['mi_event'] == 1, 1, 0) # MI
    
    pd_qsel_data['lesion_lad'] = np.where(pd_qsel_data['id_main_vessel'] == 'lad', 1, 0)
    pd_qsel_data['lesion_lcx'] = np.where(pd_qsel_data['id_main_vessel'] == 'lcx', 1, 0)
    pd_qsel_data['lesion_rca'] = np.where(pd_qsel_data['id_main_vessel'] == 'rca', 1, 0)
    
    conds = [
        (pd_qsel_data['mi_event'] == 1),
        (pd_qsel_data['mi_event'] == 0),
        ]
    vals = ['MI', 'No MI']
    
    pd_qsel_data['mi_type_str'] = np.select(conds, vals)
    
    
    # -------------- Calculate p-values, per-vessel grouping --------------- #
    pd_p_val_lv_mass = ddict()
    pd_p_val_mass_mcp_g = ddict()
    pd_p_val_mass_mcp_perc = ddict()
    
    # TODO:  Functionalize block
    #
    # BLOCK START
    anova_grps_a = ['lesion_lad', 'lesion_lcx', 'lesion_rca', ]
    anova_grps_b = ['mi_type_mi', 'mi_type_none', ]
    for ii in range(len(anova_grps_a)):
        pd_p_val_lv_mass[anova_grps_a[ii]] = lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps_a[ii]] == 1], anova_grps_b, 'mass_lv_g')
        pd_p_val_mass_mcp_g[anova_grps_a[ii]] = lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps_a[ii]] == 1], anova_grps_b, 'mass_mcp_g')
        pd_p_val_mass_mcp_perc[anova_grps_a[ii]] = lib_prj.process.stats_anova(pd_qsel_data.loc[pd_qsel_data[anova_grps_a[ii]] == 1], anova_grps_b, 'mass_mcp_perc')
        
        print('================================== {:^20} =================================='.format(anova_grps_a[ii]))
        print('ANOVA -------- LV Mass ----------- ')
        print(pd_p_val_lv_mass[anova_grps_a[ii]])
        print()
        print('ANOVA -------- MCP Mass (g) ------ ')
        print(pd_p_val_mass_mcp_g[anova_grps_a[ii]])
        print()
        print('ANOVA -------- MCP Mass (%) ------ ')
        print(pd_p_val_mass_mcp_perc[anova_grps_a[ii]])
        print()
    # BLOCK END
    
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
    lib_prj.visualize.table_pvalues({'lesions_all' : pd_anova_all_lesions_mcp_mass_g}, path_analysis_png + 'p_val-figure2a.png')
    lib_prj.visualize.table_pvalues({'lesions_all' : pd_anova_all_lesions_mcp_mass_perc}, path_analysis_png + 'p_val-figure2b.png')
    lib_prj.visualize.table_pvalues(pd_p_val_mass_mcp_g, path_analysis_png + 'p_val-figure2c.png')
    lib_prj.visualize.table_pvalues(pd_p_val_mass_mcp_perc, path_analysis_png + 'p_val-figure2d.png')
    
    # TODO:  FUNCTIONALIZE PIVOT TABLE BLOCKS
    # ---------------------------- Pivot Table 1 --------------------------- #
    pivot_groups = ['mi_type_str', 'id_main_vessel']
    # Make pivot table
    pd_qsel_pivot_totals = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc=len, values=['confirm_idc_str'])
    pd_qsel_pivot_totals.columns = ['total_lesions']
    pd_qsel_pivot_totals.reset_index(inplace=True)
    
    pd_qsel_pivot_mean = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc="mean", values=['mass_mcp_perc', 'mass_mcp_g', 'omlddistance', 'plaquecomposition', 'lesion_length', 'lumenvolume_lesion', 'lumenareastenosis', 'lumenminimaldiameter', 'lumendiameterstenosis', 'plaquevolume_lesion'])
    pd_qsel_pivot_mean.columns = [x + '_mean' for x in ['mass_mcp_perc', 'mass_mcp_g', 'omlddistance', 'plaquecomposition', 'lesion_length', 'lumenvolume_lesion', 'lumenareastenosis', 'lumenminimaldiameter', 'lumendiameterstenosis', 'plaquevolume_lesion']]
    pd_qsel_pivot_mean.reset_index(inplace=True)
    
    pd_qsel_pivot_std = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc=np.std, values=['mass_mcp_perc', 'mass_mcp_g', 'omlddistance', 'plaquecomposition', 'lesion_length', 'lumenvolume_lesion', 'lumenareastenosis', 'lumenminimaldiameter', 'lumendiameterstenosis', 'plaquevolume_lesion'])
    pd_qsel_pivot_std.columns = [x + '_std' for x in ['mass_mcp_perc', 'mass_mcp_g', 'omlddistance', 'plaquecomposition', 'lesion_length', 'lumenvolume_lesion', 'lumenareastenosis', 'lumenminimaldiameter', 'lumendiameterstenosis', 'plaquevolume_lesion']]
    pd_qsel_pivot_std.reset_index(inplace=True)
    
    # Merge pivot tables
    pd_qsel_pivot_list = [pd_qsel_pivot_totals, pd_qsel_pivot_mean, pd_qsel_pivot_std]
    # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    pd_qsel_pivot = reduce(lambda left,right: pd.merge(left, right, on=pivot_groups,how='outer',), pd_qsel_pivot_list) 
    print(tabulate(pd_qsel_pivot, headers='keys', tablefmt='psql'))
    lib_prj.visualize.table_basic(pd_qsel_pivot.sort_values(by=['id_main_vessel', 'mi_type_str']), path_analysis_png + 'table2b.png', ['w', '#f1f1f2', '#f1f1f2', 'w',])
    
    # ---------------------------- Pivot Table 2 --------------------------- #   
    pivot_groups = ['mi_type_str',]
    # Make pivot table
    pd_qsel_pivot_totals = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc=len, values=['confirm_idc_str'])
    pd_qsel_pivot_totals.columns = ['total_lesions']
    pd_qsel_pivot_totals.reset_index(inplace=True)
    
    pd_qsel_pivot_mean = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc="mean", values=['mass_mcp_perc', 'mass_mcp_g', 'omlddistance', 'plaquecomposition', 'lesion_length', 'lumenvolume_lesion', 'lumenareastenosis', 'lumenminimaldiameter', 'lumendiameterstenosis', 'plaquevolume_lesion'])
    pd_qsel_pivot_mean.columns = [x + '_mean' for x in ['mass_mcp_perc', 'mass_mcp_g', 'omlddistance', 'plaquecomposition', 'lesion_length', 'lumenvolume_lesion', 'lumenareastenosis', 'lumenminimaldiameter', 'lumendiameterstenosis', 'plaquevolume_lesion']]
    pd_qsel_pivot_mean.reset_index(inplace=True)
    
    pd_qsel_pivot_std = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc=np.std, values=['mass_mcp_perc', 'mass_mcp_g', 'omlddistance', 'plaquecomposition', 'lesion_length', 'lumenvolume_lesion', 'lumenareastenosis', 'lumenminimaldiameter', 'lumendiameterstenosis', 'plaquevolume_lesion'])
    pd_qsel_pivot_std.columns = [x + '_std' for x in ['mass_mcp_perc', 'mass_mcp_g', 'omlddistance', 'plaquecomposition', 'lesion_length', 'lumenvolume_lesion', 'lumenareastenosis', 'lumenminimaldiameter', 'lumendiameterstenosis', 'plaquevolume_lesion']]
    pd_qsel_pivot_std.reset_index(inplace=True)
    
    # Merge pivot tables
    pd_qsel_pivot_list = [pd_qsel_pivot_totals, pd_qsel_pivot_mean, pd_qsel_pivot_std]
    # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    pd_qsel_pivot = reduce(lambda left,right: pd.merge(left, right, on=pivot_groups,how='outer',), pd_qsel_pivot_list) 
    print(tabulate(pd_qsel_pivot, headers='keys', tablefmt='psql'))
    lib_prj.visualize.table_basic(pd_qsel_pivot, path_analysis_png + 'table2a.png')
    
    # ------------------------------ VISUALIZE ----------------------------- #

    
    # FIGURES:
    lib_prj.paths.make_directory(path_wr) 

    pd_qsel_data['mass_mcp_perc_mld'] = pd_qsel_data['mass_mcp_perc'] / pd_qsel_data['lumenminimaldiameter']
    pd_qsel_data['mass_mcp_perc_lumenvolume_lesion'] = pd_qsel_data['mass_mcp_perc'] * pd_qsel_data['lumenvolume_lesion']
    pd_qsel_data['mass_mcp_perc_lesion_length'] = pd_qsel_data['mass_mcp_perc'] * pd_qsel_data['lesion_length']
    pd_qsel_data['mass_mcp_perc_plaquevolume_lesion'] = pd_qsel_data['mass_mcp_perc'] * pd_qsel_data['plaquevolume_lesion']
    
    # ------------------------------- PLOT 3 -------------------------------- #
    figure_label = 'Figure 3'
    outcome_var = 'mi_event'
    predictor_var = ['mass_mcp_perc', 'mass_mcp_g', 'omlddistance', 'plaquecomposition', 'lesion_length', 'lumenvolume_lesion', 'lumenareastenosis', 'lumenminimaldiameter', 'lumendiameterstenosis', 'plaquevolume_lesion']
    
    figure_fname_label = figure_label.lower().replace(' ', '')
    fig = lib_prj.visualize.roc_plot(pd_qsel_data, outcome_var, predictor_var)
    fig.title(figure_label)
    fig.savefig(path_analysis_png + figure_fname_label + '.png', bbox_inches='tight')
    fig.show()
    
    # ------------------------------- PLOT 3 -------------------------------- #
    figure_label = 'Figure 3_combined'
    outcome_var = 'mi_event'
    predictor_var = ['mass_mcp_perc_mld', 'mass_mcp_perc_lumenvolume_lesion',  'mass_mcp_perc_lesion_length', 'mass_mcp_perc_plaquevolume_lesion']
    
    figure_fname_label = figure_label.lower().replace(' ', '')
    fig = lib_prj.visualize.roc_plot(pd_qsel_data, outcome_var, predictor_var)
    fig.title(figure_label)
    fig.savefig(path_analysis_png + figure_fname_label + '.png', bbox_inches='tight')
    fig.show()
if __name__ == '__main__':
   pd_test = run()