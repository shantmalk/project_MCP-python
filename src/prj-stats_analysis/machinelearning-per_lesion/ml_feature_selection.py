# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 18:54:45 2020

@author: smalk

REFERENCES:  
    https://datagraphi.com/blog/post/2019/9/23/feature-selection-with-sklearn-in-python
    https://pubmed.ncbi.nlm.nih.gov/27252451/
"""

import ml_raw_data
import pandas as pd
from plotly.offline import plot
from plotly.express import bar
import lib_prj
from sklearn.feature_selection import VarianceThreshold
from scipy.stats import entropy

def view_features_variance(df:'pd.DataFrame', ft, title):
    args_plotly = {
    'y' : 'index',
    'x' : ft,
    }
    y_label = 'Information Gain - ' + args_plotly['x']
    figure_fname_label = title.lower().replace(' ', '')
    args_plotly['title'] = title
    fig = bar(df, **args_plotly)
    fig.update_yaxes(title=y_label)
    fig.update_xaxes(title='')
    plot_url = plot(fig, filename=title.replace(' ','_') + '.html')

def information_gain(members, split):
    '''
    Measures the reduction in entropy after the split  
    :param v: Pandas Series of the members
    :param split:
    :return:
    '''
    entropy_before = entropy(members.value_counts(normalize=True))
    split.name = 'split'
    members.name = 'members'
    grouped_distrib = members.groupby(split) \
                        .value_counts(normalize=True) \
                        .reset_index(name='count') \
                        .pivot_table(index='split', columns='members', values='count').fillna(0)
    
    entropy_after = entropy(grouped_distrib, axis=1)
    if not len(entropy_after):
        entropy_after = [0]
    entropy_after = entropy_after * split.value_counts(sort=False, normalize=True)
    return entropy_before - entropy_after.sum()

def information_gain_df(df, col_select, split):
    features = pd.DataFrame(columns=['index', split])
    for ii in range(len(col_select)):
        features = features.append({'index' : col_select[ii], split : information_gain(df[col_select[ii]], df[split])}, ignore_index=True)
    return features.sort_values(by=[split])


# In[ ]
df = ml_raw_data.PD_COMBINED
cols = [
        'age',
        'aorta100mm2_lesion',
        'bifurcation',
        # 'confirm_idc',
        'culpr_contr_between_pat',
        'culpr_ica_ct_contr_within_pat_matchid',
        'culprit_lesion_ica_ct',
        'culprit_lesion_verifiedbyica',
        'culprit_seg_ica',
        'culprit_seg_ica_ct',
        'densecalcium_area',
        'densecalciumvolume_lesion',
        # 'dob',
        # 'dos',
        'fibrous_area',
        'fibrousfatty_area',
        'fibrousfattyvolume_lesion',
        'fibrousvolume_lesion',
        'id_main_vessel',
        'lap',
        'les_culpr_ica_ct_contr_within_pat',
        'lesion_culprit_ica_ct',
        'lesion_id',
        'lesion_length',
        'lesion_num_vp_char',
        'lesion_obst_neg_ri',
        'lesion_status',
        'lesion_worst',
        'lesiongroup',
        'lesionmaximalplaquethickness',
        'lesionspan',
        'lesiontype',
        'lumenarea',
        'lumenareastenosis',
        'lumendiameterstenosis',
        'lumenmeandiameter',
        'lumenminimaldiameter',
        'lumenvolume_lesion',
        # 'main_vessel_id',
        'mass_mcp_perc',
        'mass_mcp_g',
        # 'matched',
        'maxplq_va',
        'mi_event',
        'mi_match_id',
        'mi_type',
        'min_mld',
        'mldlesion',
        'mldlesion_arterial_dist',
        'mldlesion_epicardial',
        # 'mldlesion_id',
        'mldlesion_lm',
        'mldlesion_num',
        'mldlesion_proximal',
        'napkinringsign',
        'necroticcore_area',
        'necroticcorevolume_lesion',
        'no_culprit_lesion_reason',
        'noncalcifiedvolume_lesion',
        'omlddistance',
        'order_lesion',
        'peak_va',
        'plaqueburden',
        'plaqueburdenmean_lesion',
        'plaquecomposition',
        'plaqueeccentricity',
        'plaquethicknessmaximal',
        'plaquevolume_lesion',
        'pr',
        'refva',
        'regionname_lesion',
        'sc',
        'sex',
        'startlesion',
        'startlesion_num',
        'tortuosity',
        'vesselvolume_lesion',
        'vesselwallarea',
        'vesselwallmeandiameter',
        'vesselwallremodelingindex',
        'wl_lesion',
        'ww_lesion',
        ] 

# In[ ] FILTER COLUMNS - If majority of values is None, remove
df['lesion_culprit_ica_ct'] = pd.to_numeric(df['lesion_culprit_ica_ct'], errors='coerce').fillna(0)

updated_cols = cols.copy()
for ii in range(len(cols)):
    cur_count = (len(df[cols[ii]]) - df[cols[ii]].count()) / len(df[cols[ii]])
    if cur_count > 0:
        if cols[ii] in updated_cols:
            updated_cols.remove(cols[ii])
    if type(df[cols[ii]][0]) is str:
        if cols[ii] in updated_cols:
            updated_cols.remove(cols[ii])
    
    # if 'mmar' in cols[ii]:
    #     updated_cols.remove(cols[ii])
        
# THESE ARE THE SAME AS MI_EVENT - REMOVE THEM FROM MODEL
# BLACKLIST:
updated_cols.remove('mi_event')
updated_cols.remove('lesion_culprit_ica_ct')
# updated_cols.remove('mace_event_confirm')
# updated_cols.remove('mace_time_confirm')
# updated_cols.remove('mi_time')
# updated_cols.remove('macelr_time_confirm')
# updated_cols.remove('macelr_event_confirm')
# updated_cols.remove('death_confirm')
# updated_cols.remove('acm_time_confirm')
# updated_cols.remove('propscore_good')
# updated_cols.remove('propscore_norf')


cols = updated_cols.copy()

# In[ ] Clean outcome variable
OUTCOME = 'lesion_culprit_ica_ct'

# CLEAN OUTCOME VAR


# In[ ] INFORMATION-GAIN METHOD (SAME AS UCLA GROUP)
# Most robust method
# Similarities with previous UCLA study, but note the outcome in this code is MI event, the outcome in the UCLA study was all-cause mortality
ft = information_gain_df(df, cols, OUTCOME)
ft = ft[ft[OUTCOME] > 0 ]
FEATURES = ft

if __name__ == '__main__':
     view_features_variance(ft, 'lesion_culprit_ica_ct', '') # VISUALIZE