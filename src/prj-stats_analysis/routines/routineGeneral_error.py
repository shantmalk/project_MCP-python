# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 18:50:54 2020

@author: smDesktop
"""

import lib_prj
import pandas as pd
import numpy as np
from tabulate import tabulate


def run(path_wr=''):
    '''
    Basic routine for visualizing processing status of patients for CONFIRM study
    '''
    
    lib_prj.visualize.print_label('routineGeneral_error')
    
    # ------------------------------- PARSE -------------------------------- #
    pd_qsel_error = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, lib_prj.paths.PATH_TEMPLATE_JSON.format('qsel_general'), 'status_err_per_patient')
    
    # ------------------------------ PROCESS ------------------------------- #
    
    # Remove columns that aren't pertinent
    pd_qsel_error = pd_qsel_error.drop(['id_number', 'notes'], axis=1)
    
    # Sort by error
    pd_qsel_error = pd_qsel_error.sort_values(by='msg_err')

    
    # ------------------------------ VISUALIZE ----------------------------- #
    
    # View pivot table in console
    print('TABLE - Error Patients')
    print(tabulate(pd_qsel_error, headers='keys', tablefmt='psql'))
    
    # ADD:  Output to file here in future
    if len(path_wr) > 0:
        pass

if __name__ == '__main__':
    run( )