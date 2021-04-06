# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 17:14:24 2021

@author: smalk
"""
import csv
from collections import defaultdict as dd
import json
import os


def dict2json(filename, dd):
    with open(filename, 'w') as outfile:
        json.dump(dd, outfile)


def csv2list(path_csv):
    with open(path_csv, newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        
        ls_csv = [ ]
        
        for row in reader:
            ls_csv.append(row)
    return ls_csv

def csv2dict(path_csv):
    ls_csv = csv2list(path_csv)
    dd_csv = dd()    
    dd_csv[ls_csv[0][0]] = ls_csv[1][0]
    dd_csv[ls_csv[0][1]] = ls_csv[1][1]
    return dd_csv, ls_csv


def csv2json_ctrlns(path_csv, root=''):
    
    vessel_delim = 'Vessel_Label'
    vessel_sum_delim = 'Vessel_Label'
    aniso_delim = 'anisotropy'
    vessel_data_delim = 'Slice_Num'
    
    [dd_csv, ls_csv] = csv2dict(path_csv)
    
    ls_csv_dd = [ ] 
    ls_csv = ls_csv[3:]
    
    idx_vessel_start = [ii for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == vessel_delim)]
    idx_vessel_sum_start = [ii for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == vessel_sum_delim)]
    idx_vessel_sum_end = [ii for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == aniso_delim)]
    idx_aniso_start = [ii for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == aniso_delim)]
    idx_aniso_end = [ii + 3 for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == aniso_delim)]
    idx_vessel_data_start = [ii for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == vessel_data_delim)]
    idx_vessel_data_start = idx_vessel_data_start[::2]
    idx_vessel_data_end = [ii for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == vessel_data_delim)]
    idx_vessel_data_end = idx_vessel_data_end[1::2]
    
    for idx_vessel in idx_vessel_start:
        cur_idx_sum = [(_ii, _jj-2) for _ii, _jj in zip(idx_vessel_sum_start, idx_vessel_sum_end) if _ii >= idx_vessel and _jj >= idx_vessel][0]
        cur_idx_ansio = [(_ii, _jj-2) for _ii, _jj in zip(idx_aniso_start, idx_aniso_end) if _ii >= idx_vessel and _jj >= idx_vessel][0]
        cur_idx_vessel_data = [(_ii, _jj-1) for _ii, _jj in zip(idx_vessel_data_start, idx_vessel_data_end) if _ii >= idx_vessel and _jj >= idx_vessel][0]
        dd_vessel = dd()
        
        # ADD VESSEL SUMMARY DATA
        for ii in range(len(ls_csv[cur_idx_sum[0]])):
            if ii < len(ls_csv[cur_idx_sum[1]]):
                dd_vessel[ls_csv[cur_idx_sum[0]][ii]] = ls_csv[cur_idx_sum[1]][ii]
            else:
                dd_vessel[ls_csv[cur_idx_sum[0]][ii]] = ''
        
        # ADD ANISO DATA
        for ii in range(len(ls_csv[cur_idx_ansio[0]])):
            if ii < len(ls_csv[cur_idx_ansio[1]]):
                dd_vessel[ls_csv[cur_idx_ansio[0]][ii]] = [_v.strip() for _v in ls_csv[cur_idx_ansio[1]]]
            else:
                dd_vessel[ls_csv[cur_idx_ansio[0]][ii]] = ''
                
        # ADD VESSEL DATA
        for ii in range(len(ls_csv[cur_idx_vessel_data[0]])):
            dd_vessel[ls_csv[cur_idx_vessel_data[0]][ii]] = [float(_r[ii]) for _r in ls_csv[cur_idx_vessel_data[0] + 1 : cur_idx_vessel_data[1]]]              
        
        
        # WRITE AS JSON FILE
        vessel_path = dd_vessel['Vessel_Label'].lower().replace('.', '_') + '-centerline.json'
        vessel_path = os.path.join(root, vessel_path)
        dict2json(vessel_path, dd_vessel)        
        
        ls_csv_dd.append(dd_vessel)
        
    return ls_csv_dd


def csv2json_csa(path_csv, root=''):
    def FloatOrZero(value):
        try:
            return float(value)
        except:
            return 0.0
        
    vessel_delim = 'Vessel_Label'
    vessel_sum_delim = 'Vessel_Label'
    vessel_data_delim = 'Slice_Num'
    
    [dd_csv, ls_csv] = csv2dict(path_csv)
    
    ls_csv_dd = [ ] 
    ls_csv = ls_csv[3:]
    
    idx_vessel_start = [ii for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == vessel_delim)]
    idx_vessel_sum_start = [ii for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == vessel_sum_delim)]
    idx_vessel_sum_end = [ii for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == vessel_data_delim)]
    idx_vessel_data_start = [ii for ii in range(len(ls_csv)) if (len(ls_csv[ii]) > 0 and ls_csv[ii][0] == vessel_data_delim)]    
    idx_vessel_data_end = idx_vessel_data_start[1:] 
    idx_vessel_data_end.append(len(ls_csv)+3) # ADD HERE.. IT WORKS, TRUST.
    
    for idx_vessel in idx_vessel_start:
        cur_idx_sum = [(_ii, _jj-2) for _ii, _jj in zip(idx_vessel_sum_start, idx_vessel_sum_end) if _ii >= idx_vessel and _jj >= idx_vessel][0]
        cur_idx_vessel_data = [(_ii, _jj-6) for _ii, _jj in zip(idx_vessel_data_start, idx_vessel_data_end) if _ii >= idx_vessel and _jj >= idx_vessel][0]
        dd_vessel = dd()
        
        # ADD VESSEL SUMMARY DATA
        for ii in range(len(ls_csv[cur_idx_sum[0]])):
            if ii < len(ls_csv[cur_idx_sum[1]]):
                dd_vessel[ls_csv[cur_idx_sum[0]][ii]] = ls_csv[cur_idx_sum[1]][ii]
            else:
                dd_vessel[ls_csv[cur_idx_sum[0]][ii]] = ''
                
        # ADD VESSEL DATA
        for ii in range(len(ls_csv[cur_idx_vessel_data[0]])):
            dd_vessel[ls_csv[cur_idx_vessel_data[0]][ii]] = [FloatOrZero(_r[ii]) for _r in ls_csv[cur_idx_vessel_data[0] + 1 : cur_idx_vessel_data[1]]]              
        
        # WRITE AS JSON FILE
        vessel_path = dd_vessel['Vessel_Label'].lower().replace('.', '_') + '-csa.json'
        vessel_path = os.path.join(root, vessel_path)
        dict2json(vessel_path, dd_vessel)        
        
        ls_csv_dd.append(dd_vessel)
        
    return ls_csv_dd

def read_csv2json(path_csv, root=''):
    if isCSVFileCenterline(path_csv):
        return csv2json_ctrlns(path_csv, root)
    else:
        return csv2json_csa(path_csv, root)

def isCSVFileCenterline(path_vessel_csv):
    tmp_list = csv2list(path_vessel_csv)
    return tmp_list[6][0] == 'anisotropy'


    
    
    

if __name__ == '__main__':
    read_csv2json('C:/Users/smalk/Desktop/MCP_STUDY/STUDY/CONFIRM/confirm_789-GSHADMAN/vessels/Confirm 7891588877810.153-GSHADMAN.csv')
    read_csv2json('C:/Users/smalk/Desktop/MCP_STUDY/STUDY/CONFIRM/confirm_789-GSHADMAN/vessels/Confirm 7891588877850.525-GSHADMAN.csv')
    
    