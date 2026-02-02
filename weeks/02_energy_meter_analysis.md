EnergyMeter and Monitor behavior analysis

This week focused on understanding the behavior of the EnergyMeter and Monitor
devices in OpenDSS and on investigating the issue of zero-valued outputs observed
in previous simulations.

Through testing and documentation review, it was identified that EnergyMeters
do not provide meaningful results when using a single static solution, as they
measure accumulated energy over time. This led to the adoption of time-domain
simulations using the daily mode, which enabled proper energy accumulation.

Comparisons between EnergyMeter accumulated energy and Monitor instantaneous
measurements were performed, confirming the consistency of the obtained results.
All methodological details and simulation outputs are documented in the
Overleaf report.
