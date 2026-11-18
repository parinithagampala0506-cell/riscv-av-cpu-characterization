# Experiment Metadata

- Simulator: gem5 25.1.0.1
- Commit: a9b193c59b55e9266adaf29bb71dee3329270dc3
- Compiler: riscv64-linux-gnu-gcc 15.2.0
- Flags: -O2 -static -march=rv64gc -mabi=lp64d
- ISA/ABI: RV64GC / LP64D

## Source SHA-256

Scenario A source:
5eddc31519b18c8a51be8336c9ebae249f86e55fdcdc58a910021202c2147a41

Scenario B source:
0bb30bf1bb541d6f8186f2e80e4dade49b47b89066434ce4765871993673479f

## Scope

Scenario A: highway lane keeping.
Scenario B: urban pedestrian detection.
Scenario C: excluded.

## Outstanding experiment

Scenario A O3 2-wide result is not yet verified and is intentionally
not represented as a completed experiment.

## Scenario A O3 2-wide status

This configuration is not part of the verified results. The run
attempt using the standardized explicit-zero padding implementation
encountered a gem5 LSQ TimeBuffer assertion.

An earlier result used the previous conditional-skip padding
implementation and is excluded from the standardized-source
comparison. No performance metrics are claimed for this configuration.
See `results/scenario_a_o3_2wide_status.md`.
