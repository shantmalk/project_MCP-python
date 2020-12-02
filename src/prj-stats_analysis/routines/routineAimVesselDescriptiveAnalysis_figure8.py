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
    
    lib_prj.visualize.print_label('routineAimVesselDescriptiveAnalysis')
    
    # ------------------------------- PARSE -------------------------------- #
    
    fpath_json = lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_vessels')
    fkey_json = 'vessel_general'
    
    pd_qsel_data = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, fpath_json, fkey_json)
    pd_qsel_data = pd_qsel_data.replace(r'^\s*$', '0', regex=True)
    
    # ------------------------------ PROCESS ------------------------------- #
    # Manipulate  pd_qsel_data as needed
    
    pd_qsel_data['tree_lad'] = np.where(pd_qsel_data['id_vessel'] == 'lad', 1, 0)
    pd_qsel_data['tree_lcx'] = np.where(pd_qsel_data['id_vessel'] == 'lcx', 1, 0)
    pd_qsel_data['tree_rca'] = np.where(pd_qsel_data['id_vessel'] == 'rca', 1, 0)
    
    
    # -------------- Calculate p-values, per-vessel grouping --------------- #    
    anova_grps = ['tree_lad', 'tree_lcx', 'tree_rca']

    pd_p_val_avg_csa = lib_prj.process.stats_anova(pd_qsel_data, anova_grps, 'terminal_br_avg_csa_mm')
    pd_p_val_avg_diam = lib_prj.process.stats_anova(pd_qsel_data, anova_grps, 'terminal_br_avg_diameter_mm')
    pd_p_val_depth = lib_prj.process.stats_anova(pd_qsel_data, anova_grps, 'terminal_br_depth')

    
    
    # ------------------------- Save p-value tables ------------------------ #
    lib_prj.visualize.table_pvalues({'mean_csa' : pd_p_val_avg_csa}, path_analysis_png + 'p_val-figure8a.png')
    lib_prj.visualize.table_pvalues({'mean_diameter' : pd_p_val_avg_diam}, path_analysis_png + 'p_val-figure8b.png')
    lib_prj.visualize.table_pvalues({'depth' : pd_p_val_depth}, path_analysis_png + 'p_val-figure8c.png')
    
    
    # ---------------------------- Pivot Table 1 --------------------------- #
    pivot_groups = ['id_vessel']
    params = ['terminal_br_avg_csa_mm', 'terminal_br_avg_diameter_mm', 'terminal_br_depth']
    # Make pivot table
    pd_qsel_pivot_totals = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc=len, values=['id_vessel_comb'])
    pd_qsel_pivot_totals.columns = ['n']
    pd_qsel_pivot_totals.reset_index(inplace=True)
    
    pd_qsel_pivot_mean = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc="mean", values=params)
    pd_qsel_pivot_mean.columns = [x + '_mean' for x in params]
    pd_qsel_pivot_mean.reset_index(inplace=True)
    
    pd_qsel_pivot_std = pd.pivot_table(pd_qsel_data, index=pivot_groups, aggfunc=np.std, values=params)
    pd_qsel_pivot_std.columns = [x + '_std' for x in params]
    pd_qsel_pivot_std.reset_index(inplace=True)
    
    # Merge pivot tables
    pd_qsel_pivot_list = [pd_qsel_pivot_totals, pd_qsel_pivot_mean, pd_qsel_pivot_std]
    # (this is prefered to using "concat" because "merge" will combine the mi_type columns, instead of including this column multiple times)
    pd_qsel_pivot = reduce(lambda left,right: pd.merge(left, right, on=pivot_groups,how='outer',), pd_qsel_pivot_list) 
    print(tabulate(pd_qsel_pivot.sort_values(by=['id_vessel']), headers='keys', tablefmt='psql'))
    
    lib_prj.visualize.table_basic(pd_qsel_pivot.sort_values(by=['id_vessel']), path_analysis_png + 'table8a.png', [ '#f1f1f2', 'w','#f1f1f2','w',], ['Vessel', 'N', 'Mean CSA (mm^2)', 'Mean Diam. (mm)', 'Depth'])
    
    
    # ------------------------------ VISUALIZE ----------------------------- #

    
    # FIGURES:
    lib_prj.paths.make_directory(path_wr) 

    # ------------------------- FIGURE 2A-B PARAMS ------------------------- #
    pd_qsel_data = pd_qsel_data.sort_values(by=['id_vessel'])
    args_plotly = {
        'x' : 'id_vessel',
        'points' : 'all',
        'color' : 'id_vessel',
        'labels' : {'id_vessel' : 'Main Vessel'},
        }
    
    # ------------------------------ FIGURE 8A ----------------------------- #
    figure_label = 'Figure 8A'
    y_data = 'terminal_br_avg_csa_mm'
    y_label = 'Mean CSA (mm^2)'
    title =  figure_label + ': Mean CSA of terminal branches in LAD, LCx and RCA trees'
    
    figure_fname_label = figure_label.lower().replace(' ', '')
    args_plotly['y'] = ['terminal_br_avg_csa_mm']#, 'plaquecomposition', 'lumenminimaldiameter']
    args_plotly['title'] = ''
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title=y_label)
    fig.update_layout(showlegend=False)
    fig.update_layout(yaxis=dict(range=[0, 75]))
    
    # Save file if path specified
    plot_url = plot(fig, filename=path_analysis_html + figure_fname_label + '.html')
    fig.write_image(path_analysis_png + figure_fname_label + '.png')
    
    # ------------------------------ FIGURE 8B ----------------------------- #
    figure_label = 'Figure 8B'
    y_data = 'terminal_br_avg_diameter_mm'
    y_label = 'Mean Diameter (mm)'
    title =  figure_label + ': Mean diameter of terminal branches in LAD, LCx and RCA trees'
    
    figure_fname_label = figure_label.lower().replace(' ', '')
    args_plotly['y'] = ['terminal_br_avg_diameter_mm']#, 'plaquecomposition', 'lumenminimaldiameter']
    args_plotly['title'] = ''
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title=y_label)
    fig.update_layout(showlegend=False)
    
    # Save file if path specified
    plot_url = plot(fig, filename=path_analysis_html + figure_fname_label + '.html')
    fig.write_image(path_analysis_png + figure_fname_label + '.png')
    
    # ------------------------------ FIGURE 8C ----------------------------- #
    figure_label = 'Figure 8C'
    y_data = 'terminal_br_depth'
    y_label = 'Mean Depth'
    title =  figure_label + ': Mean depth of LAD, LCx and RCA trees'
    
    figure_fname_label = figure_label.lower().replace(' ', '')
    args_plotly['y'] = ['terminal_br_depth']#, 'plaquecomposition', 'lumenminimaldiameter']
    args_plotly['title'] = ''
    fig = lib_prj.visualize.boxplot_plotly(pd_qsel_data, args_plotly, '')
    fig.update_yaxes(title=y_label)
    fig.update_layout(showlegend=False)
    
    # Save file if path specified
    plot_url = plot(fig, filename=path_analysis_html + figure_fname_label + '.html')
    fig.write_image(path_analysis_png + figure_fname_label + '.png')
    
    
if __name__ == '__main__':
   pd_test = run()