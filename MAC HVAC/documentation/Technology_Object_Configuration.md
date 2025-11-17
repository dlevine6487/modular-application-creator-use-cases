# Technology Object (TO) Configuration

This document specifies the configuration and tuning parameters for the Technology Objects (TOs) used in the AHU Controller, as defined in the `SDS_AHU_Controller.md`.

## 1. TO_PID_DAT_Control

*   **Instance Name:** `TO_PID_DAT_Control_1`
*   **Purpose:** This is the primary PID controller responsible for maintaining the Discharge Air Temperature (DAT) setpoint. It provides a bipolar output that is mapped to the heating and cooling equipment modules.
*   **Controller Type:** `PID_Temp` (as per TIA Portal selection)

### Configuration

| Parameter                 | Value / Tag                  | Notes                                                              |
|:--------------------------|:-----------------------------|:-------------------------------------------------------------------|
| `Mode`                    | Automatic                    | Controller is always active in "Occupied" mode.                    |
| `ProcessValue`            | `AHU1_DAT_Temp`              | The Discharge Air Temperature sensor reading.                      |
| `Setpoint`                | `SA_Temp_SP`                 | The desired Discharge Air Temperature (HMI adjustable).            |
| `Output`                  | `TO_PID_DAT_Control_Output`  | Internal tag, bipolar output (-100% to +100%).                      |
| `OutputUpperLimit`        | 100.0                        | Corresponds to 100% cooling demand.                               |
| `OutputLowerLimit`        | -100.0                       | Corresponds to 100% heating demand.                               |
| `ProportionalGain`        | 2.5                          | Initial tuning value. Subject to field adjustment.               |
| `IntegralTime`            | 120 s                        | Initial tuning value. Subject to field adjustment.               |
| `DerivativeTime`          | 15 s                         | Initial tuning value. Subject to field adjustment.               |

### Logic Integration

*   If `TO_PID_DAT_Control_Output` > 0, its value is mapped to the `EM200_Cooling_Coil_Valve` command.
*   If `TO_PID_DAT_Control_Output` < 0, its absolute value is mapped to the `EM200_Heating_Coil_Valve` command.
*   A deadband (e.g., +/- 5%) is applied to prevent simultaneous heating and cooling.

## 2. TO_PID_Econ_Control

*   **Instance Name:** `TO_PID_Econ_Control_1`
*   **Purpose:** This PID controller is enabled only during "Economizer (Free Cooling) Mode." It modulates the fresh air damper to control the discharge air temperature using cool outside air.
*   **Controller Type:** `PID_Compact` (as per TIA Portal selection)

### Configuration

| Parameter                 | Value / Tag                  | Notes                                                              |
|:--------------------------|:-----------------------------|:-------------------------------------------------------------------|
| `Mode`                    | Disabled (by default)        | Enabled only when economizer conditions are met.                   |
| `ProcessValue`            | `AHU1_DAT_Temp`              | The Discharge Air Temperature sensor reading.                      |
| `Setpoint`                | `SA_Temp_SP`                 | The desired Discharge Air Temperature.                             |
| `Output`                  | `AHU1_DMP_PosCmd`            | Direct control of the damper position command (0-100%).             |
| `OutputUpperLimit`        | 100.0                        | Maximum damper position.                                           |
| `OutputLowerLimit`        | `Min_Fresh_Air_Pos`          | Minimum damper position during occupied mode.                      |
| `ProportionalGain`        | 5.0                          | Initial tuning value. Tuned for faster response than the main loop.|
| `IntegralTime`            | 90 s                         | Initial tuning value.                                              |
| `DerivativeTime`          | 0 s                          | Derivative action is typically not needed for damper control.      |

### Logic Integration

*   This PID is only activated when the `Economizer_Enable` condition is TRUE (based on enthalpy comparison).
*   When active, it overrides the `EM300_Fresh_Air_Damper`'s normal minimum position logic.
