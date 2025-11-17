# Repository Synopsis and MAC Setup Evaluation

**Version:** 1.0
**Date:** September 18, 2025
**Author:** Jules, Senior Controls Engineer

This document provides a high-level synopsis of the repository and an evaluation of the existing documentation for setting up and running the Modular Application Creator (MAC) C# tool.

---

## 1. Repository Synopsis

This repository contains a comprehensive project for an industrial **HVAC Air Handler Unit (AHU) Controller**, designed for the Siemens TIA Portal and S7-1500 PLC platform. The project is centered around the **Siemens Modular Application Creator (MAC)**, a C#/.NET tool that automates the generation of TIA Portal projects from standardized "Equipment Modules."

### Key Directories

*   **`MAC HVAC/`**: This is the core of the HVAC application's engineering and design.
    *   `Documents/`: Contains all design specifications, including the master IO list (`SDS_AHU_Controller.md`), UDT definitions, and control loop configuration guides.
    *   `Lets_Make_The_MAC/`: Intended to hold user-focused guides for the MAC tool (currently empty).

*   **`MAC_use_cases/`**: This directory contains the C# source code for the **Modular Application Creator (MAC)** tool itself. It is a .NET application built on the MVVM (Model-View-ViewModel) pattern, which provides the GUI for configuring and generating the TIA Portal projects.

*   **`TiaPortal_Export_Files/`**: This directory serves as the library of standardized code blocks that are used by the MAC to generate the final PLC program. It contains the source code for all the Equipment Module Function Blocks (e.g., `FB100_EM_SupplyFan.scl`), User Data Types (`.udt`), and other PLC components in a text-based format that can be imported into TIA Portal.

*   **`TestSuiteFiles/`**: Contains the quality assurance and testing documentation for the HVAC application. This includes detailed Markdown Test Plans for each Equipment Module and corresponding Python test scripts (`.py`) for simulated testing.

*   **`validation/`**: Holds the formal validation and qualification documents (DQ, IQ, etc.), which are critical for projects in regulated industries.

---

## 2. MAC Setup & Usage Evaluation

The existing documentation provides a solid foundation for a developer to get the MAC C# tool running, but it is missing a clear, user-focused guide that connects the C# tool to the specific HVAC application.

### Strengths

*   The root **`README.md`** provides excellent, clear instructions for a C# developer to:
    *   Install the necessary prerequisites (TIA Portal, Visual Studio).
    *   Clone the repository.
    *   Build and run the `MAC_use_cases` solution.
    *   Configure the MAC GUI to use the generated modules.

### Missing Links & Recommendations

The primary missing link is a guide for an **end-user** (e.g., a Controls Engineer who is not a C# developer) who wants to use the pre-built MAC tool to generate an HVAC project. The `README.md` is developer-centric, focusing on building the tool from source.

**Recommendation:** Create a new guide, **`MAC_HVAC_Quickstart_Guide.md`**, to be placed in the `MAC HVAC/Lets_Make_The_MAC/` directory. This guide should:

1.  **Provide a Pre-Compiled Executable:** Link to a `.zip` file containing a pre-compiled, standalone version of the `ModularApplicationCreator.exe` so that a user does not need to build the C# project in Visual Studio.
2.  **User-Focused Workflow:** Provide a step-by-step tutorial on how to use the MAC GUI to create the specific AHU project defined in the SDS. This would include:
    *   How to launch the `.exe`.
    *   How to load the specific HVAC Equipment Modules from the `TiaPortal_Export_Files`.
    *   A walk-through of configuring a Supply Fan, a Cooling loop, and a Heating loop in the GUI.
    *   Instructions on how to use the "Generate" feature to produce the final, importable TIA Portal project file (`.al19`).
3.  **Clarify the "Why":** Briefly explain the connection between the C# tool, the `TiaPortal_Export_Files`, and the design documents in `MAC HVAC/Documents`, so the user understands how the pieces fit together.

By creating this user-focused guide, the repository would be accessible not only to the developers maintaining the MAC tool but also to the Controls Engineers who are its primary users.
