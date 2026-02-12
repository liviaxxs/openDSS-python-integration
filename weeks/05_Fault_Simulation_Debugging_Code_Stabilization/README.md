# Week 5 and 6 – Fault Simulation Debugging and Validation (OpenDSS)

## Objective

The objective of this stage was to obtain and execute the necessary code
to simulate the eleven possible fault types in OpenDSS, considering
a fault resistance of 5 Ω in all cases. The goal was to ensure correct
execution of the simulations and eliminate runtime errors.

## Initial Approach

At first, an automated loop-based implementation in Python was attempted
in order to generate the different fault combinations programmatically.
However, this approach presented difficulties related to the correct
definition of buses and phase configurations for each fault type.

Although the theoretical classification of single-phase, two-phase,
and three-phase faults was well understood, each configuration requires
a specific definition in OpenDSS. A single generic loop proved insufficient
to correctly handle all cases.

As an intermediate solution, the fault simulations were implemented manually,
using a working single-phase fault model as a base and adapting it for
each configuration.

## Debugging Process

During execution, recurring issues were observed:

- EnergyMeter-related warning messages  
- Output file overwriting  
- Inconsistent simulation updates  

After technical review and guidance, the IEEE 34-bus test feeder was adopted
as the standard simulation model. The IEEE 34 feeder was chosen due to its
grounded neutral configuration, which provides more predictable behavior
for single-line-to-ground faults compared to delta-based systems.

To stabilize the simulations, the following OpenDSS commands were incorporated:

- `set casename` → to properly define output folders and avoid file overwriting  
- `CalcV` → to recalculate nodal voltages after circuit modifications  
- Explicit deactivation/reset of previously defined faults before creating a new one  

These adjustments eliminated the EnergyMeter warnings and ensured consistent
execution across all simulations.

## Final Result

After implementing these corrections, the code successfully executed all
eleven fault types with a fault resistance of 5 Ω, without runtime errors.
This stage was fundamental for understanding the internal execution logic
of OpenDSS and the importance of command sequencing during fault simulations.
