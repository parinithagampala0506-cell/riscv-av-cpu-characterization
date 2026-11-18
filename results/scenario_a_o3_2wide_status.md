# Scenario A — O3 2-Wide Verification

**Verification status: Completed**

- Scenario: A — Highway lane keeping
- CPU: RISC-V O3 CPU, 2-wide pipeline
- Workload: `scenario_a_cpu_old_padding`
- Simulation: Completed successfully
- Simulated time: 0.036945 seconds
- Simulated ticks: 36,944,781,000
- Instructions: 61,513,549
- CPI: 0.600596
- IPC: 1.665013

## Output verification

All four layer checksums match the expected Scenario A outputs:

| Layer | Checksum |
|---|---:|
| 1 | -53709 |
| 2 | 14119 |
| 3 | -16231 |
| 4 | -3886 |

## Standardized-source diagnostic

A separate attempt using `workloads/scenario_a_cpu` terminated with a gem5 O3 TimeBuffer assertion in the LSQ writeback path.

The successful result above uses the earlier padding implementation. Its instruction count therefore differs slightly from the standardized MinorCPU and O3 4-wide results.

**Reporting note:** This experiment is verified, but should be identified as using the earlier padding implementation rather than presented as a fully standardized six-run comparison.
