# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 00:49:50 2021

@author: smalk
"""
import numpy as np
import os
from pydicom import dcmread
import matplotlib.pyplot as plt

# import unittest

# class TestMCP(unittest.TestCase):
    
#     def test_mpc(self):
#         pass

if __name__ == '__main__':
    path_dcm = 'C:/Users/smalk/Desktop/MCP_STUDY/ANIMALSTUDY/pig-data/pig_01072015/SEGMENT_dcm/WH_dcm'
    files_dcm = [os.path.join(path_dcm, ff) for ff in os.listdir(path_dcm) if ff.endswith('.dcm')]
    vol_test = np.zeros((512, 512, len(files_dcm)))
    
    for ii in range(len(files_dcm)):
        cur_np = dcmread(files_dcm[ii]).pixel_array
        vol_test[:, :, ii] = cur_np
    vol_test_copy = vol_test
    vol_test[vol_test_copy < -1024] = 0
    vol_test[vol_test_copy == -1024] = 0
    vol_test[vol_test_copy > 0] = 1
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    
