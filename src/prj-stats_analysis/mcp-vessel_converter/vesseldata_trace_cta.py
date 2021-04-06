# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:04:42 2021

@author: smalk
"""
from vesseldata_csv2json import read_csv2json
from pydicom import dcmread
import os
import json
import requests
import pyodbc
import pd

def json_parse(path_qsel_json, kname):
    with open(path_qsel_json, encoding='utf-8-sig') as json_file:
        data_json = json.load(json_file)
    return data_json[kname]

def qsel_parse(path_db, path_qsel_json, kname):
    qsel = json_parse(path_qsel_json, kname)['qsel']
    path_db_frmt = r'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={PATH};'.format(PATH=path_db)
    conn = pyodbc.connect(path_db_frmt)
    return pd.read_sql_query(qsel, conn)

def write_db_trace(patient_name, series_id, series_UID):
    db_path = 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY/DATABASE/db_CONFIRM'
    db_tbl = 'tblInfoCTA-test'
    


def parse_studyUID(path_dcm):
    files_dcm = [os.path.join(path_dcm, ff) for ff in os.listdir(path_dcm) if ff.endswith('.dcm')]
    tmp_dcm = dcmread(files_dcm[0])
    return tmp_dcm[0x0020, 0x000d].value

def parse_seriesUID(tag, criteria, tag_return, study_uid):
    pacs_level_field = 'Series'
    find_params = {
        'Level' : '{}'.format(pacs_level_field),
        'Query' : {
            '{}'.format(tag) : '{}'.format(criteria),
            'StudyInstanceUID' : '{}'.format(study_uid),
            }
        }
    
    r = requests.post('http://128.200.49.26:8042/tools/find', data=json.dumps(find_params))
    
    if len(r.json()):
        orthanc_id = r.json()[0]
        tmp_query = requests.get('http://128.200.49.26:8042/series/' + orthanc_id)
        return tmp_query.json()['MainDicomTags'][tag_return]
    else:
        return ''
        
        
def trace_cta(vessel_data:dict, patient_name, path_lv_dcm):
    db_path = ''
    
    # PARSE PATIENTNAME
    dcm_PatientName = patient_name
    
    # PARSE STUDYID
    dcm_StudyUID = parse_studyUID(path_lv_dcm)
    
    # PARSE SERIES_ID
    dcm_SeriesDescription = vessel_data['Series_ID']
    
    # PARSE SERIESINSTANCEUID
    dcm_SeriesInstanceUID = parse_seriesUID('SeriesDescription', dcm_SeriesDescription, 'SeriesInstanceUID', dcm_StudyUID)
    
    # INDEX DATA IN DATABASE
    write_db_trace(dcm_PatientName, dcm_SeriesDescription, dcm_SeriesInstanceUID)
    


if __name__ == '__main__':
    path_dcm = 'C:/Users/smalk/Desktop/MCP_STUDY/STUDY/CONFIRM/confirm_789-GSHADMAN/SEGMENT_dcm/LV_dcm'
    path_tmp = 'C:/Users/smalk/Desktop/research/prj-mcp/code-py/src/prj-stats_analysis/mcp-vessel_converter/mrca-csa.json'
    with open(path_tmp) as jfile:
        vessel_dict = json.load(jfile)
        
    trace_cta(vessel_dict, 'confirm_789', path_dcm)