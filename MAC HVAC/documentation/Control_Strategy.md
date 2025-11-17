# AHU Control Strategy

## 1. Overview

This document outlines the control strategy for the Air Handling Unit (AHU) managed by the S7-1500 PLC. The primary goal is to maintain a comfortable and safe environment within the controlled space by delivering air at a specified temperature and humidity, while also optimizing for energy efficiency.

The strategy incorporates several key functions:
-   **Temperature Control:** Modulating heating and cooling coils to meet the supply air temperature setpoint.
-   **Ventilation Control:** Adjusting the fresh air damper to meet minimum ventilation requirements based on occupancy or CO2 levels, and to leverage "free cooling" when ambient conditions are favorable (economizer mode).
-   **Humidity Control:** Managing humidity levels to prevent condensation and ensure occupant comfort.
-   **Safety and Alarming:** Monitoring all equipment for operational failures and unsafe conditions.

## 2. Modes of Operation

The AHU will operate in one of the following modes, determined by a combination of the schedule, ambient conditions, and space requirements.

### a. Occupied Mode

-   **Description:** The primary operating mode when the building is occupied. The system actively controls temperature and ventilation.
-   **Enabling Conditions:**
    -   Building Management System (BMS) schedule indicates "Occupied".
    -   Manual override from HMI.
-   **Control Logic:**
    -   **Supply Fan:** Runs continuously.
    -   **Temperature Control:** The `EM100_Cooling_Coil_Valve` and `EM200_Heating_Coil_Valve` are modulated via separate PID loops to maintain the `SA_Temp_SP`. The heating and cooling loops are interlocked to prevent simultaneous operation.
    -   **Ventilation:** The `EM300_Fresh_Air_Damper` modulates to maintain the minimum fresh air position (`Min_Fresh_Air_Pos`) or a higher position if economizer mode is active.
    -   **Return Fan:** Runs and modulates to maintain a constant static pressure in the return duct.

### b. Unoccupied Mode

-   **Description:** An energy-saving mode for when the building is empty. Temperature is allowed to drift within a wider deadband, and ventilation is minimized.
-   **Enabling Conditions:**
    -   BMS schedule indicates "Unoccupied".
-   **Control Logic:**
    -   **Supply & Return Fans:** Cycled on/off as needed to maintain the unoccupied temperature setpoints.
    -   **Temperature Control:** Heating or cooling is enabled only if the space temperature exceeds the unoccupied upper or lower limits.
    -   **Ventilation:** The fresh air damper remains fully closed.

### c. Economizer (Free Cooling) Mode

-   **Description:** An energy-saving sub-mode of "Occupied Mode". When outside air is cool and dry enough, it is used for cooling in lieu of mechanical refrigeration.
-   **Enabling Conditions:**
    -   System is in "Occupied Mode".
    -   Outside air enthalpy is less than return air enthalpy (`OA_Enthalpy < RA_Enthalpy`).
    -   Outside air temperature is below the required supply air temperature, but above freezing (`Freezing_Protect_SP < OA_Temp < SA_Temp_SP`).
-   **Control Logic:**
    -   The cooling coil valve (`EM100`) is closed.
    -   The fresh air damper (`EM300`) modulates to maintain the supply air temperature setpoint.
    -   The return and exhaust dampers modulate oppositionally to the fresh air damper to maintain building pressure.

## 3. Core Control Loops

### a. Supply Air Temperature Control

-   **Objective:** Maintain `SA_Temp` at `SA_Temp_SP`.
-   **Sensors:** `SA_Temp`, `RA_Temp`
-   **Actuators:** `Cooling_Valve_CMD`, `Heating_Valve_CMD`
-   **Logic:**
    1.  A primary PID loop calculates a master cooling/heating demand (e.g., -100% to +100%).
    2.  This demand is split:
        -   If demand is negative (cooling needed), the value is scaled and sent to the cooling valve PID.
        -   If demand is positive (heating needed), the value is scaled and sent to the heating valve PID.
    3.  A deadband is implemented to prevent rapid switching between heating and cooling.

### b. Condensation Prevention

-   **Objective:** Prevent condensation from forming on the exterior of the supply air ductwork.
-   **Sensors:** `OA_Temp`, `OA_RH`, `SA_Temp`
-   **Actuators:** `Cooling_Valve_CMD`
-   **Logic:**
    1.  The dew point of the outside air is continuously calculated using the `FB_CondensationPrevention` block.
    2.  If the supply air temperature (`SA_Temp`) approaches the outside air dew point within a predefined safety margin (`DewPoint_Safety_Margin`), the condensation prevention logic will override the primary temperature control loop.
    3.  The override will limit the cooling valve command, raising the supply air temperature to stay safely above the dew point. This prevents the duct surface from becoming cold enough to cause condensation.

## 4. Alarming and Safeties

-   **Device Failure:** Each equipment module (`EM100`, `EM200`, etc.) monitors its feedback signal. A discrepancy between the command (`CMD`) and feedback (`FDBK`) for a specified time duration will trigger a `Device_Failure` alarm.
-   **Freezing Protection:** If `OA_Temp` drops below the `Freezing_Protect_SP` (e.g., 35°F), the fresh air damper will close to its minimum position, and the heating coil will be activated to preheat the air if necessary.
-   **High/Low Alarms:** All analog sensors (`SA_Temp`, `RA_Temp`, etc.) have configurable high and low alarm setpoints.
