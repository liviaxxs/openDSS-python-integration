Week 4 – Single-phase fault simulation using OpenDSS and Python.

In this stage, a single-phase-to-ground fault was implemented in the IEEE 37 bus distribution system using the OpenDSS interface in Python. The objective was to analyze the electrical behavior of the system before and after the fault occurrence.

A fault element was inserted in phase A at bus 701 with low resistance (0.001 Ω), representing a near-metallic short circuit. Monitors were created to record voltages and currents both before and after the fault. The simulation was executed in snapshot mode, and the results were exported to CSV files for analysis.

Since the IEEE37 system is configured as a three-wire delta network, the analysis focused primarily on phase currents rather than phase-to-ground voltages. The results showed a significant increase in current in the faulted phase after the short-circuit event, confirming the expected behavior of a distribution system under fault conditions.

All scripts and generated data were organized and uploaded to the GitHub repository as part of the weekly project development.
