# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 22:40:31 2020

@author: smalk
"""

COLUMNS = [
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

BLACKLIST = [
    'mi_event',
    'lesion_culprit_ica_ct',
    ]