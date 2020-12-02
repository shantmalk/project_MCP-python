# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 16:00:49 2020
Exploratory figures for per-lesion analysis of CONFIRM data

@author: smalk
"""

import lib_prj
from plotly.offline import plot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc
from lifelines import *
from lifelines.datasets import load_waltons


# In[] DEFINE PATHS
json_path = 'C:/Users/smalk/Desktop/research/prj-mcp/code-py/src/prj-stats_analysis/fig_scripts/qsel.json'
fig_path = 'C:/Users/smalk/Desktop/research/prj-mcp/code-py/src/prj-stats_analysis/figs/png'
fig_name_prefix = 'Per-lesion analysis: '

# In[] FIGURE 1

fig_name = fig_name_prefix + 'MMAR (%)'
json_query = lib_prj.parse.json_parse(json_path, 'script1-figure1-perlesion')

 

# In[]