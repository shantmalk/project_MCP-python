import lib_prj
import pandas as pd
import numpy as np
from tabulate import tabulate

PATH_TEMPLATE_JSON = 'C:/Users/smDesktop/Desktop/research/prj-mcp/code-py/src/prj-stats_analysis/qsel_json/{}.json'
PATH_DB = 'C:/Users/smDesktop/Desktop/research/prj-mcp/data/database/db_CONFIRM-merged.accdb'

def print_label( ):
    print('--------------------------------------------------------------------------')
    print('routineMIType_status')
    print()

def run( ):
    '''
    Basic routine for visualizing processing status of patients for CONFIRM study
    '''
    
    print_label()
    
    # ------------------------------- PARSE -------------------------------- #
    pd_qsel_phase1_raw = lib_prj.parse.qsel_parse(PATH_DB, PATH_TEMPLATE_JSON.format('qsel_mitype'), 'status_prc_phase1')
    pd_qsel_phase2_raw = lib_prj.parse.qsel_parse(PATH_DB, PATH_TEMPLATE_JSON.format('qsel_mitype'), 'status_prc_phase2')
    pd_qsel_phase3_raw = lib_prj.parse.qsel_parse(PATH_DB, PATH_TEMPLATE_JSON.format('qsel_mitype'), 'status_prc_phase3')
    
    # ------------------------------ PROCESS ------------------------------- #
    # Add phase column to each dataframe
    pd_qsel_phase1_raw['phase'] = 'phase1'
    pd_qsel_phase2_raw['phase'] = 'phase2'
    pd_qsel_phase3_raw['phase'] = 'phase3'
    
    # Merge dataframes
    pd_qsel_raw = pd.concat([pd_qsel_phase1_raw, pd_qsel_phase2_raw, pd_qsel_phase3_raw])
    
    # Replace null value with 0
    pd_qsel_raw = pd_qsel_raw.fillna(0)
    
    # Create new columns for visualization
    pd_qsel_raw['prc_matlab'] = np.where(pd_qsel_raw['status_patient_obj'] == 1, 1, 0)
    pd_qsel_raw['prc_vitrea'] = np.where((pd_qsel_raw['status_lv'] == 1) & (pd_qsel_raw['status_vessels'] == 1), 1, 0)
    pd_qsel_raw['err_matlab'] = np.where((pd_qsel_raw['prc_matlab'] == 0) & (pd_qsel_raw['prc_vitrea'] == 1), 1, 0)
    
    # Make pivot tables
    pd_qsel_pivot = pd.pivot_table(pd_qsel_raw, index='phase', aggfunc=np.sum, values=['prc_vitrea', 'prc_matlab', 'err_matlab'])
    pd_qsel_pivot.reset_index(inplace=True)
    pd_qsel_pivot_totals = pd.pivot_table(pd_qsel_raw, index='phase', aggfunc=len, values=['prc_vitrea'])
    pd_qsel_pivot_totals.columns = ['total']
    pd_qsel_pivot_totals.reset_index(inplace=True)
    pd_qsel_pivot = pd.merge(pd_qsel_pivot_totals, pd_qsel_pivot)
    
    # ------------------------------ VISUALIZE ----------------------------- #
    
    # View pivot table in console
    print('TABLE - Processed Patients (by phase)')
    print(tabulate(pd_qsel_pivot, headers='keys', tablefmt='psql'))
    
    # ADD:  Output to file here in future

if __name__ == '__main__':
   pd_test = run()