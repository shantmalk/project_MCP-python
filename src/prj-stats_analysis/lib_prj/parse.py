# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:00:57 2020

@author: smDesktop
"""

import json
import pandas as pd
import pyodbc

def json_parse(path_qsel_json, kname):
    with open(path_qsel_json, encoding='utf-8-sig') as json_file:
        data_json = json.load(json_file)
    return data_json[kname]

def qsel_parse(path_db, path_qsel_json, kname):
    qsel = json_parse(path_qsel_json, kname)['qsel']
    
    path_db_frmt = r'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={PATH};'.format(PATH=path_db)
    conn = pyodbc.connect(path_db_frmt)
    return pd.read_sql_query(qsel, conn)


if __name__ == '__main__':
    PATH_TEMPLATE_JSON = 'C:/Users/smDesktop/Desktop/research/prj-mcp/code-py/src/prj-stats_analysis/qsel_json/{}.json'
    PATH_DB = 'C:/Users/smDesktop/Desktop/research/prj-mcp/data/database/db_CONFIRM-merged.accdb'
    assert(json_parse(PATH_TEMPLATE_JSON.format('qsel_basic'), 'basic1') == {'key' : 1, 'qsel' : ''})
    assert(json_parse(PATH_TEMPLATE_JSON.format('qsel_basic'), 'basic2') == {'key' : 2, 'qsel' : ''})