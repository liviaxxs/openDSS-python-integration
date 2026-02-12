# Week 7 – Automated Fault Simulation Using Loops

## Objective

The objective of this stage was to fully automate the simulation of different short-circuit fault types in OpenDSS using Python. Unlike previous weeks, where faults were implemented manually, this version applies an iterative logic structure to generate all fault configurations programmatically.

## Implemented Fault Types

The script automatically simulates the following eleven fault configurations:

- 3 single-phase faults
- 3 two-phase faults with ground
- 3 two-phase faults without ground
- 1 three-phase fault without ground
- 1 three-phase fault with ground

All simulations consider a fault resistance of 5 ohms applied at bus 802.

## Methodology

The automation was implemented using nested `for` loops to systematically generate phase combinations. This approach avoids redundancy and ensures that all possible configurations are executed exactly once.

For each fault scenario, the script performs the following steps:

1. Creates the Fault element
2. Creates a Monitor associated with Line.L2
3. Resets monitors
4. Calculates voltages
5. Sets simulation mode to snapshot
6. Solves the system
7. Samples the results
8. Exports data to CSV
9. Disables the fault before the next iteration

The results are exported automatically using `Set casename` and stored as `.CSV` files.

## Circuit Used

The IEEE 37-bus test feeder was used for this implementation.

## Required Libraries

- py_dss_interface
- pandas
- os
- pathlib

## How to Run

Make sure OpenDSS is installed and run:

```bash
python fault_loop_complete.py
