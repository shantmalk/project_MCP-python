# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 10:17:51 2020

@author: smDesktop
"""

import lib_prj
import pandas as pd
# ADD ADDT LIBRARIES AS NEEDED

def run(path_wr=''):
    '''
    Basic routine for visualizing processing status of patients for CONFIRM study
    
    INPUTS
        path_wr     [STR | Directory where visualization data can be saved *OPTIONAL*; if not specified, no data will be written]
    '''
    
    lib_prj.visualize.print_label('routineTemplate')
    
    # ------------------------------- PARSE -------------------------------- #
    pd_qsel_data = lib_prj.parse.qsel_parse(lib_prj.paths.PATH_DB, lib_prj.paths.PATH_TEMPLATE_JSON.format('JSONFILENAME'), 'QSELKEY') 
    
    
    # ------------------------------ PROCESS ------------------------------- #
    # Manipulate  pd_qsel_data as needed
    
    
    # ------------------------------ VISUALIZE ----------------------------- #
    # Visualization of pd_qsel_data
    
    # ----------------------------- WRITE FILE ----------------------------- #
    # Save visualization to file
    if len(path_wr) > 0:
        pass
    
    
if __name__ == '__main__':
   pd_test = run()