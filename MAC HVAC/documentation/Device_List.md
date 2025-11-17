# Device List

This document provides a consolidated list of all physical I/O points for the AHU Controller, derived from the master `SDS_AHU_Controller.md`.

## Digital Inputs

| TIA Portal Tag Name Convention | Parameter Name            |
| :--- | :--- |
| `AHU1_SF_RunFdbk`          | Run Feedback/Status       |
| `AHU1_SF_AirflowSw`        | Airflow Switch Status     |
| `AHU1_SF_VfdFault`         | VFD Fault Status          |
| `AHU1_CW_FreezeStat`       | Chilled Water Freeze Stat |
| `AHU1_HW_FreezeStat`       | Hot Water Freeze Stat     |
| `AHU1_SYS_DirtyFilter`     | Dirty Filter Status       |

## Digital Outputs

| TIA Portal Tag Name Convention | Parameter Name         |
| :--- | :--- |
| `AHU1_SF_StartCmd`         | Start/Stop Command     |

## Analog Inputs

| TIA Portal Tag Name Convention | Parameter Name           |
| :--- | :--- |
| `AHU1_CW_VlvFdbk`          | Chilled Water Valve Fdbk |
| `AHU1_HW_VlvFdbk`          | Hot Water Valve Fdbk     |
| `AHU1_DMP_PosFdbk`         | Damper Position Fdbk     |
| `AHU1_RAT_Temp`            | Return Air Temp          |
| `AHU1_OAT_Temp`            | Outside Air Temp         |
| `AHU1_DAT_Temp`            | Discharge Air Temp       |
| `AHU1_RAR_RH`              | Return Air RH            |
| `AHU1_OAR_RH`              | Outside Air RH           |
| `AHU1_DAR_RH`              | Discharge Air RH         |
| `AHU1_PFL_DP`              | Pre-Filter DP            |
| `AHU1_AFL_DP`              | Post-Filter DP           |
| `AHU1_RM_DP`               | Room DP                  |

## Analog Outputs

| TIA Portal Tag Name Convention | Parameter Name            |
| :--- | :--- |
| `AHU1_SF_SpeedRef`         | Speed Reference           |
| `AHU1_CW_VlvCmd`           | Chilled Water Valve Cmd   |
| `AHU1_HW_VlvCmd`           | Hot Water Valve Cmd       |
| `AHU1_DMP_PosCmd`          | Damper Position Cmd       |
