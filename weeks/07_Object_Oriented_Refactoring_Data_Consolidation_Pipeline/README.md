# Week 8 – Object-Oriented Refactoring and Parquet Export

## Overview

In this stage, the fault simulation project was refactored using an object-oriented programming (OOP) structure.  
The automated fault loop (Week 7) was integrated with a random line selection routine and reorganized into a modular architecture.

## Main Changes

- Creation of the `SimulacaoDSS` class to centralize:
  - Circuit compilation
  - Monitor and EnergyMeter configuration
  - Fault application
  - Simulation execution
  - Result export and consolidation

- Implementation of a `main.py` file as the program entry point.
- Separation of results into:
  - `Antes/` (without fault)
  - `Depois/` (with fault)

## Data Consolidation

The previous multiple CSV outputs were unified into structured `.parquet` files using `pandas` and `pyarrow`.

Advantages of Parquet:
- Columnar format
- Preserves data types
- Smaller file size
- More efficient for data analysis

Final outputs per scenario:
- `Monitors_ALL.parquet`
- `EnergyMeters_ALL.parquet`
- `Monitors_FAULT_ALL.parquet`
- `EnergyMeters_FAULT_ALL.parquet`

## How to Run

```bash
python main.py
