# Scenario A — O3 2-Wide Experiment Status

Status: NOT INCLUDED IN THE VERIFIED RESULTS.

## Intended experiment

- Workload: Scenario A — Highway lane keeping
- CPU model: gem5 O3CPU
- Pipeline width: 2
- Workload source: workloads/scenario_a_cpu.c
- Padding implementation: standardized explicit-zero padding

## What happened

An attempt to run Scenario A with the standardized source and
O3 2-wide configuration encountered a gem5 LSQ TimeBuffer assertion.

The simulation did not produce a successfully validated result.

An earlier O3 2-wide result exists, but it was generated using the
previous conditional-skip padding implementation. It is excluded
from the current standardized-source comparison.

## Reporting decision

No execution time, CPI, IPC, or speedup value is reported for
Scenario A O3 2-wide in the verified results.

The missing result is treated as an experimental limitation,
not as a successful measurement.

## Current Scenario A coverage

- MinorCPU: verified result available
- O3 2-wide: not verified; excluded
- O3 4-wide: verified result available

## Future work

Investigate the gem5 assertion and repeat the experiment only after
the cause is understood and the run completes successfully.
