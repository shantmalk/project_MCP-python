# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 09:53:13 2020

@author: smDesktop
"""
import os
import errno


# ------------------------------ GLOBAL PATHS ------------------------------ #
PATH_ROOT = 'C:/Users/smalk/Desktop/research/prj-mcp/'
PATH_TEMPLATE_JSON = PATH_ROOT + 'code-py/src/prj-stats_analysis/qsel_json/{}.json'
PATH_DB = PATH_ROOT + 'data/database/db_CONFIRM-merged.accdb'
PATH_PLOTLY_TEMP = PATH_ROOT + 'temp_plotly/'
PATH_ANALYSIS = PATH_ROOT + 'code-py/analysis/'
PATH_ANALYSIS_FIG_PNG = PATH_ANALYSIS + 'figs/png/'
PATH_ANALYSIS_FIG_HTML = PATH_ANALYSIS + 'figs/html/'


# -------------------------------- FUNCTIONS ------------------------------- #
def make_directory(path):
    if len(path) > 0:
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise