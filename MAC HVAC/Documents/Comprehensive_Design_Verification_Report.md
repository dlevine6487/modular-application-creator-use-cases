# Comprehensive Design Verification Report

**Date:** September 17, 2025
**Author:** Jules, Controls & Instrumentation Engineer

This report documents the results of a comprehensive design verification, comparing the Master IO List against the UDT Specification, Test Plans, and Validation Documents.

---

## 1. MISSING FROM DESIGN DOCUMENTS

The following IO points are defined in the Master IO List (`SDS_AHU_Controller.md`) but could not be found in the `AHU_UDT_Specification.md`.

| Tag Name | Description |
| :--- | :--- |
| `AHU1_SF_StartCmd` | Supply Fan Start/Stop Command |
| `AHU1_SF_RunFdbk` | Supply Fan Run Feedback/Status |
| `AHU1_SF_AirflowSw` | Supply Fan Airflow Switch Status |
| `AHU1_SF_VfdFault` | Supply Fan VFD Fault Status |
| `AHU1_SYS_DirtyFilter` | System Dirty Filter Status |

---

## 2. MISSING FROM IO LIST

The following items were found in the design, test, or validation documents but are not defined in the Master IO List (`SDS_AHU_Controller.md`).

| Tag / Parameter | Source Document | Description |
| :--- | :--- | :--- |
| `Min_Fresh_Air_Pos` | `EM400_Test_Plan.md` | A parameter used in the test plan for setting the minimum fresh air position. |
| `H-101, H-102, H-103` | `validation/IQ-HVAC-001.md` | RH Sensors listed in the validation documents. |
| `DP-101, DP-102, DP-103` | `validation/IQ-HVAC-001.md` | Differential Pressure Sensors listed in the validation documents. |

---

## 3. DISCREPANCIES

The following discrepancies were identified between the Master IO List (`SDS_AHU_Controller.md`) and the other design documents.

| Document | Tag / Parameter | Expected (from IO List) | Actual (in Document) | Problem |
| :--- | :--- | :--- | :--- | :--- |
| `AHU_UDT_Specification.md` | `Run_Fdbk_DI` | `AHU1_SF_RunFdbk` | `Run_Fdbk_DI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `Airflow_Status_DI` | `AHU1_SF_AirflowSw` | `Airflow_Status_DI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `VFD_Fault_DI` | `AHU1_SF_VfdFault` | `VFD_Fault_DI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `Start_Cmd_DO` | `AHU1_SF_StartCmd` | `Start_Cmd_DO` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `Speed_Ref_AO` | `AHU1_SF_SpeedRef` | `Speed_Ref_AO` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `CHW_Freeze_Stat_DI` | `AHU1_CW_FreezeStat` | `CHW_Freeze_Stat_DI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `CHW_Valve_Fdbk_AI` | `AHU1_CW_VlvFdbk` | `CHW_Valve_Fdbk_AI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `CHW_Valve_Cmd_AO` | `AHU1_CW_VlvCmd` | `CHW_Valve_Cmd_AO` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `HW_Freeze_Stat_DI` | `AHU1_HW_FreezeStat` | `HW_Freeze_Stat_DI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `HW_Valve_Fdbk_AI` | `AHU1_HW_VlvFdbk` | `HW_Valve_Fdbk_AI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `HW_Valve_Cmd_AO` | `AHU1_HW_VlvCmd` | `HW_Valve_Cmd_AO` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `Return_Air_Temp_AI` | `AHU1_RAT_Temp` | `Return_Air_Temp_AI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `Outside_Air_Temp_AI`| `AHU1_OAT_Temp` | `Outside_Air_Temp_AI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `Discharge_Air_Temp_AI`|`AHU1_DAT_Temp` | `Discharge_Air_Temp_AI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `Damper_Pos_Fdbk_AI` | `AHU1_DMP_PosFdbk` | `Damper_Pos_Fdbk_AI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `Damper_Pos_Cmd_AO`| `AHU1_DMP_PosCmd` | `Damper_Pos_Cmd_AO` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `AHU_UDT_Specification.md` | `Dirty_Filter_DI`| `AHU1_SYS_DirtyFilter`| `Dirty_Filter_DI` | **Name Mismatch:** UDT parameter name does not follow the project's tag naming convention. |
| `validation/IQ-HVAC-001.md` | `T-101, T-102, T-103` | `AHU1_DAT_Temp`, `AHU1_RAT_Temp`, `AHU1_OAT_Temp` | `T-101, T-102, T-103` | **Name Mismatch:** The validation documents use a different naming convention for temperature sensors. |
