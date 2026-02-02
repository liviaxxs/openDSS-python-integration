# Python Integration for OpenDSS Simulation

This task focused on adapting the previously used OpenDSS code to run via Python, aiming to automate the simulation process and correct the issue observed in the export of measurement data.

Migrating the code to Python allowed greater control over the execution order of commands, ensuring that the meter sampling occurred before data export.

For this adaptation, the `py_dss_interface` library was used, enabling direct interaction with the OpenDSS simulation engine through Python scripts. The same circuit as in the previous task was employed, with modifications to guarantee correct meter sampling and data export.

The Python script used for these simulations is available in [python_integration_script.py](python_integration_script.py).
