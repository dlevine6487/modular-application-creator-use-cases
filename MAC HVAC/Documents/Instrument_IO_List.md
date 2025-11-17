# Instrument I/O List

This document provides a comprehensive list of all instrument I/O points for the AHU Controller project, formatted for easy copying into a spreadsheet.

| Equipment Module | Instrument Tag | Description | PLC Tag | I/O Type | Signal Type |
| :--- | :--- | :--- | :--- | :--- | :--- |
| EM-100 | - | Supply Fan Start/Stop Command | AHU1_SF_StartCmd | Output | Digital |
| EM-100 | - | Supply Fan Speed Reference | AHU1_SF_SpeedRef | Output | Analog |
| EM-100 | - | Supply Fan Run Feedback | AHU1_SF_RunFdbk | Input | Digital |
| EM-100 | - | Supply Fan Airflow Switch | AHU1_SF_AirflowSw | Input | Digital |
| EM-100 | - | Supply Fan VFD Fault | AHU1_SF_VfdFault | Input | Digital |
| EM-200 | V-101 | Chilled Water Valve Command | AHU1_CW_VlvCmd | Output | Analog |
| EM-200 | P-101 | Chilled Water Valve Feedback | AHU1_CW_VlvFdbk | Input | Analog |
| EM-200 | FS-101 | Chilled Water Freeze Stat | AHU1_CW_FreezeStat | Input | Digital |
| EM-300 | V-102 | Hot Water Valve Command | AHU1_HW_VlvCmd | Output | Analog |
| EM-300 | P-102 | Hot Water Valve Feedback | AHU1_HW_VlvFdbk | Input | Analog |
| EM-300 | FS-102 | Hot Water Freeze Stat | AHU1_HW_FreezeStat | Input | Digital |
| EM-400 | D-101 | Damper Position Command | AHU1_DMP_PosCmd | Output | Analog |
| EM-400 | P-103 | Damper Position Feedback | AHU1_DMP_PosFdbk | Input | Analog |
| EM-400 | T-102 | Return Air Temperature | AHU1_RAT_Temp | Input | Analog |
| EM-400 | T-103 | Outside Air Temperature | AHU1_OAT_Temp | Input | Analog |
| EM-400 | T-101 | Discharge Air Temperature | AHU1_DAT_Temp | Input | Analog |
| EM-500 | DPS-101 | Dirty Filter Status | AHU1_SYS_DirtyFilter | Input | Digital |
| EM-500 | H-102 | Return Air Relative Humidity | AHU1_RAR_RH | Input | Analog |
| EM-500 | H-103 | Outside Air Relative Humidity | AHU1_OAR_RH | Input | Analog |
| EM-500 | H-101 | Discharge Air Relative Humidity | AHU1_DAR_RH | Input | Analog |
| EM-500 | DP-101 | Pre-Filter Differential Pressure | AHU1_PFL_DP | Input | Analog |
| EM-500 | DP-102 | Post-Filter Differential Pressure | AHU1_AFL_DP | Input | Analog |
| EM-500 | DP-103 | Room Differential Pressure | AHU1_RM_DP | Input | Analog |
