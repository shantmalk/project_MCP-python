# SCRIPT:  main.py
#   Author - Shant Malkasian
#   Email - smalkasi@uci.edu
#   Description - Main script for running processing scripts

import routines


# ROUTINE BLOCK ============================================================ #
routines.routineGeneral_status.run()
routines.routineGeneral_error.run()
routines.routineMIType_worstlesion.run('C:/Users/smDesktop/Desktop/research/prj-mcp/data/mitype_versus_mass/')
routines.routineMIvNoMI_worstlesion.run('C:/Users/smDesktop/Desktop/research/prj-mcp/data/mi_versus_nomi/')