# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 08:00:26 2020

@author: smalk
"""

import ml_raw_data
import lib_prj.process as prc
import lib_prj.visualize as viz
import params

# In[1] Raw data
cols = params.COLUMNS
blacklist = params.BLACKLIST
outcome = 'lesion_culprit_ica_ct'

df = ml_raw_data.PD_COMBINED

# In[2] Clean data
updated_cols = prc.clean_df(df, cols, blacklist)
outcome = 'lesion_culprit_ica_ct'

# In[3] ROC-AUC ANALYSIS - USING ALL DATA
outcome = 'lesion_culprit_ica_ct'
figure_label = 'Per-Lesion:  High-risk plaque features [Outcome = ' + outcome + ']'
labels = {'vesselvolume_lesion' : 'Lesion vessel vol.',
          'lumenvolume_lesion' : 'Lesion lumen vol.',
          'lumenminimaldiameter' : 'MLD',
          'lesion_worst' : 'MIN(MLA)',
          'omlddistance' : 'Distance to MLD',
          'vesselwallremodelingindex' : 'Remodeling index (HRP Ft.)',
          'necroticcorevolume_lesion' : 'Low-atten. plaque (HRP Ft.)',
          }
description = '''
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)

# In[4] ROC-AUC ANALYSIS - USING ALL DATA
outcome = 'lesion_culprit_ica_ct'
figure_label = 'Per-Lesion:  High-risk plaque features [Outcome = ' + outcome + ']'
labels = {'lesion_length' : 'Length of lesion',
          'vesselvolume_lesion' : 'Vessel volume in lesion',
          'lumenvolume_lesion' : 'Lumen volume in lesion',
          'plaquevolume_lesion' : 'Plaque volume in segment/lesion',
          'fibrousvolume_lesion' : 'Fibrous plaque volume in lesion HU 131-350',
          'fibrousfattyvolume_lesion' : 'Fibrous fatty plaque volume in lesion HU 31-130',
          'necroticcorevolume_lesion' : 'Necrotic core volume in lesion HU 0-30',
          'densecalciumvolume_lesion' : 'Dense calcium volume in lesion HU>350',
          'noncalcifiedvolume_lesion' : 'Total non-calcified plaque volume in  lesion',
          'plaqueburdenmean_lesion' : 'plaque volume/ vessel volume * 100',
          }
description = ''' 
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)

# In[5] ROC-AUC ANALYSIS - USING ALL DATA
outcome = 'lesion_culprit_ica_ct'
figure_label = 'Per-Lesion:  High-risk plaque features - Composite [Outcome = ' + outcome + ']'

df['lesion_vesselvolume_permm'] = df['vesselvolume_lesion'] / df['lesion_length']
df['lesion_lumenvolume_permm'] = df['lumenvolume_lesion']  / df['lesion_length']
df['lesion_plaquevolume_permm'] = df['plaquevolume_lesion'] / df['lesion_length']
df['lesion_fibrousvolume_pct'] = df['fibrousvolume_lesion'] / df['plaquevolume_lesion']
df['lesion_fibrousfattyvolume_pct'] = df['fibrousfattyvolume_lesion'] / df['plaquevolume_lesion']
df['lesion_necroticcorevolume_pct'] = df['necroticcorevolume_lesion'] / df['plaquevolume_lesion']
df['lesion_densecalciumvolume_pc'] = df['densecalciumvolume_lesion'] / df['plaquevolume_lesion']

labels = {'lesion_vesselvolume_permm' : 'vessel_vesselvolume/ vessel_regionlength',
          'lesion_lumenvolume_permm' : 'vessel_lumenvolume/ vessel_regionlength',
          'lesion_plaquevolume_permm' : 'vessel_plaquevolume/ vessel_regionlength',
          'lesion_fibrousvolume_pct' : 'VesselFibrousVolume/ vessel_plaquevolume',
          'lesion_fibrousfattyvolume_pct' : 'vessel_fibrousfattyvolume/ vessel_plaquevolume',
          'lesion_necroticcorevolume_pct' : 'vessel_necroticcorevolume/ vessel_plaquevolume',
          'lesion_densecalciumvolume_pc' : 'vessel_densecalciumvolume / vessel_plaquevolume',
          }
description = ''' 
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)


# In[6] ROC-AUC ANALYSIS - USING ALL DATA
outcome = 'lesion_culprit_ica_ct'
figure_label = 'Per-Lesion:  MMAR [Outcome = ' + outcome + ']'
labels = {'mass_mcp_perc' : 'MMAR(%)',
          'mass_mcp_g' : 'MMAR(g)',
          }
description = '''
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)

# In[7] ROC-AUC ANALYSIS - USING ALL DATA
outcome = 'lesion_culprit_ica_ct'
figure_label = 'Per-Lesion:  MMAR + HRP [Outcome = ' + outcome + ']'

df['mmar_vesselvolume_permm'] = df['vesselvolume_lesion'] * df['mass_mcp_perc']
df['mmar_lumenvolume_permm'] = df['lumenvolume_lesion']  * df['mass_mcp_perc']
df['mmar_plaquevolume_permm'] = df['plaquevolume_lesion'] * df['mass_mcp_perc']
df['mmar_fibrousvolume_pct'] = df['fibrousvolume_lesion'] * df['mass_mcp_perc']
df['mmar_fibrousfattyvolume_pct'] = df['fibrousfattyvolume_lesion'] * df['mass_mcp_perc']
df['mmar_necroticcorevolume_pct'] = df['necroticcorevolume_lesion'] * df['mass_mcp_perc']
df['mmar_densecalciumvolume_pc'] = df['densecalciumvolume_lesion'] * df['mass_mcp_perc']




labels = {'mmar_vesselvolume_permm' : 'vesselvolume_lesion * mmar_perc',
          'mmar_lumenvolume_permm' : 'lumenvolume_lesion * mmar_perc',
          'mmar_plaquevolume_permm' : 'plaquevolume_lesion * mmar_perc',
          'mmar_fibrousvolume_pct' : 'fibrousvolume_lesion * mmar_perc',
          'mmar_fibrousfattyvolume_pct' : 'fibrousfattyvolume_lesion * mmar_perc',
          'mmar_necroticcorevolume_pct' : 'necroticcorevolume_lesion * mmar_perc',
          'mmar_densecalciumvolume_pc' : 'densecalciumvolume_lesion * mmar_perc',
          }

description = '''
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)

# In[8] DEFINE HRP OUTCOME BASED ON MIN PAPER
# https://www.sciencedirect.com/science/article/abs/pii/S1936878X19309349?via%3Dihub
# IF SUM(sc, pr, lap) > 2 -> HRP 

df['is_hrp'] = (df['pr'] + df['sc'] + df['lap']) > 1



# In[9] ROC-AUC ANALYSIS - USING ALL DATA
outcome = 'is_hrp'
figure_label = 'Per-Lesion:  MMAR [Outcome = ' + outcome + ']'

labels = {'mmar_vesselvolume_permm' : 'vesselvolume_lesion * mmar_perc',
          'mmar_lumenvolume_permm' : 'lumenvolume_lesion * mmar_perc',
          'mmar_plaquevolume_permm' : 'plaquevolume_lesion * mmar_perc',
          'mmar_fibrousvolume_pct' : 'fibrousvolume_lesion * mmar_perc',
          'mmar_fibrousfattyvolume_pct' : 'fibrousfattyvolume_lesion * mmar_perc',
          'mmar_necroticcorevolume_pct' : 'necroticcorevolume_lesion * mmar_perc',
          'mmar_densecalciumvolume_pc' : 'densecalciumvolume_lesion * mmar_perc',
          }

description = '''
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)

# In[10] ROC-AUC ANALYSIS - USING ALL DATA  
outcome = 'is_hrp'
figure_label = 'Per-Lesion:  MMAR [Outcome = ' + outcome + ']'

labels = {'mass_mcp_perc' : 'MMAR(%)',
          'mass_mcp_g' : 'MMAR(g)',
          }
description = '''
AUC analysis demonstrates the value of several high-risk plaque features, to predict the culprit lesion leading to MI in patients with multivessel CAD.
'''
figure_fname_label = figure_label.lower().replace(' ', '')
fig, roc_tbl = viz.roc_plot(df, outcome, labels)
fig.title(figure_label)
