# Experiment Metadata

## Recorded Simulation Environment

- Simulator: gem5 25.1.0.1
- Recorded gem5 commit: a9b193c59b55e9266adaf29bb71dee3329270dc3
- Recorded compiler: riscv64-linux-gnu-gcc 15.2.0
- Recorded compiler flags: -O2 -static -march=rv64gc -mabi=lp64d
- ISA/ABI: RV64GC / LP64D

## Source SHA-256

Scenario A source:
5eddc31519b18c8a51be8336c9ebae249f86e55fdcdc58a910021202c2147a41

Scenario B source:
0bb30bf1bb541d6f8186f2e80e4dade49b47b89066434ce4765871993673479f

## Research Scope

- Scenario A: Highway lane keeping.
- Scenario B: Urban pedestrian detection.
- Scenario C: Excluded from this study.

## CPU Configurations

- MinorCPU
- O3 2-wide
- O3 4-wide

## Scenario A O3 2-wide: Verification and Reporting Status

An earlier O3 2-wide simulation completed using the previous
conditional-skip padding implementation and produced matching
layer checksums.

However, this result is excluded from the standardized performance
comparison because its padding implementation differs from the
standardized workload source.

A subsequent attempt using the standardized explicit-zero-padding
implementation did not complete because gem5 encountered a
TimeBuffer assertion.

Consequently, no standardized Scenario A O3 2-wide performance
result is reported in this study. The earlier completed run is
retained only as a historical diagnostic result.

See `results/scenario_a_o3_2wide_status.md` for the experiment record.
