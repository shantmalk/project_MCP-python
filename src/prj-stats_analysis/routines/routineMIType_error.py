# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 18:50:54 2020

@author: smDesktop
"""

import lib_prj
import pandas as pd
import numpy as np
from tabulate import tabulate

PATH_TEMPLATE_JSON = 'C:/Users/smDesktop/Desktop/research/prj-mcp/code-py/src/prj-stats_analysis/qsel_json/{}.json'
PATH_DB = 'C:/Users/smDesktop/Desktop/research/prj-mcp/data/database/db_CONFIRM-merged.accdb'

def print_label( ):
    print('--------------------------------------------------------------------------')
    print('routineMIType_error')
    print()

def run( ):
    '''
    Basic routine for visualizing processing status of patients for CONFIRM study
    '''
    
    print_label()
    
    # ------------------------------- PARSE -------------------------------- #
    pd_qsel_error_raw = lib_prj.parse.qsel_parse(PATH_DB, PATH_TEMPLATE_JSON.format('qsel_mitype'), 'status_err_per_patient')
    
    # ------------------------------ PROCESS ------------------------------- #
   

    
    # ------------------------------ VISUALIZE ----------------------------- #
    
    # View pivot table in console
    print('TABLE - Error Patients')
    print(tabulate(pd_qsel_error_raw, headers='keys', tablefmt='psql'))
    
    # ADD:  Output to file here in future

if __name__ == '__main__':
    run( )