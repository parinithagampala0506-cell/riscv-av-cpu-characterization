# Performance Characterization of RISC-V CPU Configurations for CNN-Inspired Autonomous-Vehicle Workloads Using gem5

## Overview

This repository contains the source code and experimental results for a
RISC-V CPU performance-characterization study using gem5.

The study evaluates CNN-inspired convolution workloads representing two
autonomous-vehicle scenarios:

- Scenario A: Highway lane keeping
- Scenario B: Urban pedestrian detection

## CPU configurations

- MinorCPU
- O3 2-wide
- O3 4-wide

## Workloads

The workloads are synthetic CNN-inspired convolution kernels implemented
in C. They are not trained production neural networks.

Both workloads use the same convolution-loop padding implementation.
Their input dimensions, channel counts, and layer counts differ to
represent the two workload scenarios.

## Simulation environment

- Simulator: gem5
- gem5 version: 25.1.0.1
- gem5 commit: a9b193c59b55e9266adaf29bb71dee3329270dc3
- Compiler: riscv64-linux-gnu-gcc 15.2.0
- Compiler flags: -O2 -static -march=rv64gc -mabi=lp64d

## Evaluation metrics

- Simulated execution time
- Instruction count
- Cycles per instruction (CPI)
- Instructions per cycle (IPC)

## Current experimental coverage

Scenario A:
- MinorCPU: available
- O3 2-wide: pending verification
- O3 4-wide: available

Scenario B:
- MinorCPU: available
- O3 2-wide: available
- O3 4-wide: available

See the results directory for the currently collected statistics.

## Limitations

These workloads are synthetic CNN-inspired kernels. The study does not
claim real-world autonomous-driving accuracy, vehicle safety validation,
silicon power measurements, or hardware area measurements.

The repository contains CPU-only experiments. It does not claim that
the CNN layers were executed by a simulated AI accelerator.

## Reproducibility

The source files, simulation configuration script, and available
statistics are provided for inspection and reproducibility.
The gem5 simulator must be separately installed and built for RISC-V.

## Scenario A O3 2-wide experiment status

The Scenario A O3 2-wide experiment is not included in the verified
results. The attempt using the standardized explicit-zero padding
implementation encountered a gem5 LSQ TimeBuffer assertion and did
not complete successfully.

An earlier result used the previous conditional-skip padding
implementation. It is excluded from the current comparison to avoid
mixing results from different source implementations.

Accordingly, Scenario A currently has verified MinorCPU and O3 4-wide
results only. See
`results/scenario_a_o3_2wide_status.md` for the experiment record.
