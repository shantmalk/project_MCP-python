# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 19:25:14 2021

@author: smalk
"""

from vesseldata_csv2json import read_csv2json
import re
import os



def convert_patient(path_patient, dir_vessel_csv='vessels', dir_vessel_json='vessels-vitrea-json', dir_lv_dcm='SEGMENT_dcm/LV_dcm'):
    
    # STATUS TEMPLATE FOR ELEGANT STATUS UPDATING
    status_tmplt = 'CSV2JSON:  {ORIG_PATH: <45} | {CSV_FOLDER: <10} | {JSON_FOLDER: <15} | {STATUS: <15}'
    
    # SETUP VESSEL PATHS
    path_vessel_csv = os.path.join(path_patient, dir_vessel_csv)
    path_vessel_json = os.path.join(path_patient, dir_vessel_json)
    path_lv_dcm = os.path.join(path_patient, dir_lv_dcm)
    
    # MAKE SURE PATH_VESSEL_CSV EXISTS AND IS NOT EMPTY
    if not os.path.exists(path_vessel_csv):
        print(status_tmplt.format(ORIG_PATH=path_patient, CSV_FOLDER=dir_vessel_csv, JSON_FOLDER=dir_vessel_json, STATUS='FAILED - Missing folder'))
        return 0
    
    # MAKE SURE PATH_VESSEL_JSON EXISTS
    if not os.path.exists(path_vessel_json):
        os.mkdir(path_vessel_json)
        
    
    # FOR CSV FILES IN PATH_VESSEL_CSV -> CHANGE TO JSON FILES IN PATH_VESSEL_JSON
    path_files_csv = [ os.path.join(path_vessel_csv, ff) for ff in os.listdir(path_vessel_csv) if ff.endswith('.csv')]
    for fpath in path_files_csv:
        vessel_data_dd = read_csv2json(fpath, path_vessel_json)
        print(status_tmplt.format(ORIG_PATH=path_patient, CSV_FOLDER=dir_vessel_csv, JSON_FOLDER=dir_vessel_json, STATUS='CONVERTED CSV -> JSON'))
    
    if os.path.exists(path_lv_dcm):
        pass
    # ADD AUXILLARY PROCESSING METHODS HERE...
    
    # AUX PROCESSING - INDEX
    # PROBABLY EASIER TO USE MATLAB FOR THIS...
    # trace_cta(vessel_data_dd)
    
    # SNIPPET TO FIX A MISTAKE IN DOWNLOADING CSV DATA...
    os.rename(path_vessel_csv, path_vessel_csv.replace('vessels-cleerly-json', 'vessels-vitrea-csv'))
    return 1

def convert_csv_files(path_vessel_csv, path_vessel_json):
    
    # STATUS TEMPLATE FOR ELEGANT STATUS UPDATING
    status_tmplt = 'CSV2JSON:  {ORIG_PATH: <75} | {JSON_PATH: <75} | {STATUS: <15}'
    
    # MAKE SURE PATH_VESSEL_CSV EXISTS AND IS NOT EMPTY
    if not os.path.exists(path_vessel_csv):
        print(status_tmplt.format(ORIG_PATH=path_vessel_csv, JSON_PATH=path_vessel_json, STATUS='FAILED - Missing folder'))
        return 0
    
    # MAKE SURE PATH_VESSEL_JSON EXISTS
    if not os.path.exists(path_vessel_json):
        os.mkdir(path_vessel_json)
        
    
    # FOR CSV FILES IN PATH_VESSEL_CSV -> CHANGE TO JSON FILES IN PATH_VESSEL_JSON
    path_files_csv = [os.path.join(path_vessel_csv, ff) for ff in os.listdir(path_vessel_csv) if ff.endswith('.csv')]
    for fpath in path_files_csv:
        vessel_data_dd = read_csv2json(fpath, path_vessel_json)
        print(status_tmplt.format(ORIG_PATH=path_vessel_csv, JSON_PATH=path_vessel_json, STATUS='CONVERTED CSV -> JSON'))
    return 1
    


if __name__ == '__main__':
    # TEST_PATH_PATIENT = 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY/CONFIRM/confirm_789-GSHADMAN'
    # convert_patient(TEST_PATH_PATIENT)
    
    
    # ----------------------- Per-Patient conversion ----------------------- #
    STUDY_PATH = 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY/CONFIRM'
    path_patients = [os.path.join(STUDY_PATH, ff) for ff in os.listdir(STUDY_PATH) if (re.match(re.compile('confirm_([0-9])*'), ff) and os.path.isdir(os.path.join(STUDY_PATH, ff)))]
    
    for ppatient in path_patients:
        try:
            convert_patient(ppatient, dir_vessel_csv='vessels-cleerly-json')
        except:
            print('ERROR: ' + ppatient)
    
    # -------------------------- Bulk conversion --------------------------- #
    # convert_csv_files('C:/Users/smalk/Desktop/MCP_STUDY/STUDY/VITREA_VESSELS_CSV', 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY/VITREA_VESSELS_JSON')