# Performance Characterization of RISC-V CPU Configurations for CNN-Inspired Autonomous-Vehicle Workloads Using gem5

## 1. Project Overview

This repository contains the source code, gem5 simulation configurations, and experimental results for a study comparing RISC-V CPU configurations using synthetic CNN-inspired workloads related to autonomous-vehicle applications.

The study evaluates two workloads:

- **Scenario A – Highway Lane Keeping:** Four convolution layers.
- **Scenario B – Urban Pedestrian Detection:** Six convolution layers.

Scenario C is outside the scope of this research.

The experiments compare three CPU configurations:

1. MinorCPU
2. Out-of-order CPU (O3), 2-wide
3. Out-of-order CPU (O3), 4-wide

The simulations use gem5 to characterize execution time, instruction count, CPI, IPC, and selected microarchitectural statistics.

## 2. Simulation Environment

- Simulator: gem5 25.1.0.1
- Target ISA: RISC-V (RV64GC)
- Compiler: RISC-V GNU toolchain
- Simulated clock frequency: 1 GHz
- CPU models: MinorCPU and O3 configurations

See [EXPERIMENT_METADATA.md](EXPERIMENT_METADATA.md) for the recorded experiment metadata and source information.

## 3. Scenario A – Highway Lane Keeping

Scenario A represents a relatively lightweight CNN-inspired workload containing four convolution layers.

### Verified standardized results

| CPU configuration | Simulated time (s) | Instructions | CPI | IPC |
|---|---:|---:|---:|---:|
| MinorCPU | 0.051361673 | 61,513,634 | 0.834964 | 1.197656 |
| O3 4-wide | 0.021505555 | 61,513,634 | 0.349606 | 2.860360 |

The O3 4-wide configuration achieved approximately **2.39× speedup** over MinorCPU.

### Scenario A O3 2-wide verification note

An earlier O3 2-wide run completed using the previous conditional-skip padding implementation and produced matching layer checksums. However, it is not included in the standardized comparison because its padding implementation differed from the standardized workload.

The later standardized explicit-zero-padding attempt did not complete because gem5 encountered a TimeBuffer assertion. Therefore, this historical O3 2-wide result is treated as a diagnostic result, not as a directly comparable standardized result.

### Scenario A output checksums

| Layer | Checksum |
|---|---:|
| Layer 1 | -53709 |
| Layer 2 | 14119 |
| Layer 3 | -16231 |
| Layer 4 | -3886 |

## 4. Scenario B – Urban Pedestrian Detection

Scenario B represents a more computationally demanding CNN-inspired workload containing six convolution layers.

### Verified CPU-only results

| CPU configuration | Simulated time (s) | Instructions | CPI | IPC |
|---|---:|---:|---:|---:|
| MinorCPU | 2.108669736 | 2,636,634,126 | 0.799758 | 1.250378 |
| O3 2-wide | 1.739183364 | 2,636,634,126 | 0.659623 | 1.516018 |
| O3 4-wide | 1.117268615 | 2,636,634,126 | 0.423748 | 2.359893 |

The O3 4-wide configuration achieved approximately:

- **1.89× speedup** over MinorCPU.
- **1.56× speedup** over O3 2-wide.

These results show that the O3 configurations reduce simulated execution time compared with MinorCPU for this workload.

### Scenario B layer checksums

| Layer | Output dimensions | Checksum |
|---|---:|---:|
| 1 | 160 × 160 × 24 | -628222 |
| 2 | 80 × 80 × 48 | -269422 |
| 3 | 40 × 40 × 48 | 77367 |
| 4 | 20 × 20 × 64 | -50884 |
| 5 | 10 × 10 × 64 | 1385 |
| 6 | 5 × 5 × 96 | -4145 |

The saved CPU-only verification output reports successful completion of the Scenario B workload.

## 5. Evaluation Metrics

The study uses the following metrics:

- **Simulated execution time:** Time reported by gem5 (`simSeconds`).
- **Instruction count:** Number of simulated instructions (`simInsts`).
- **Cycles per instruction (CPI):** Average cycles required per instruction.
- **Instructions per cycle (IPC):** Average instructions completed per cycle.

Selected cache, branch-prediction, and instruction-commit statistics are also examined to help interpret the performance differences.

## 6. Microarchitectural Findings (Scenario B)

Additional gem5 statistics were examined to understand the behaviour of the two O3 configurations.

### D-cache MSHR behaviour

The O3 configurations report higher D-cache demand-miss counts than MinorCPU. However, these counts must be interpreted together with the MSHR statistics.

In gem5, an MSHR hit occurs when a request matches an existing outstanding miss and is coalesced with it. An MSHR miss occurs when a new MSHR entry is required.

| D-cache statistic | MinorCPU | O3 2-wide | O3 4-wide |
|---|---:|---:|---:|
| Demand misses | 109,459 | 247,559 | 330,108 |
| Demand MSHR hits | 2,206 | 140,630 | 223,409 |
| Demand MSHR misses | 107,253 | 106,929 | 106,699 |
| Demand miss rate | 0.0254% | 0.0574% | 0.0765% |

For each configuration, demand MSHR hits plus demand MSHR misses equal the reported demand misses. The increase in demand-miss counts in the O3 configurations is therefore primarily associated with increased MSHR hits, rather than an increase in new MSHR misses. These counts should not be interpreted as a proportional increase in unique cache-line misses or external memory traffic.

The L2 demand-miss rates were also similar across the configurations: 34.2990% for MinorCPU, 34.3435% for O3 2-wide, and 34.4304% for O3 4-wide.

### O3 instruction retirement behaviour

The instruction-commit statistics show higher average retirement throughput for O3 4-wide than O3 2-wide.

| Commit statistic | O3 2-wide | O3 4-wide |
|---|---:|---:|
| Average instructions committed per cycle | 1.516435 | 2.360899 |
| Cycles committing the maximum width | 67.48% (2 instructions) | 42.56% (4 instructions) |

Although O3 4-wide records more ROB-full and queue-full events, it achieves higher average retirement throughput. Branch-misprediction counts are nearly identical between the two configurations, suggesting that differences in branch prediction do not explain the observed performance improvement. These counters describe execution behaviour but do not establish a single cause for all pipeline stalls.

## 7. Repository Contents

Important experiment files include:

- `workloads/scenario_b_cpu.c` – Scenario B CPU-only workload source.
- `av_cpu_run.py` – gem5 CPU simulation configuration.
- `results/scenario_b_cpu_minor_corrected_stats.txt` – Scenario B MinorCPU statistics.
- `results/scenario_b_cpu_o3_2wide_stats.txt` – Scenario B O3 2-wide statistics.
- `results/scenario_b_cpu_o3_4wide_stats.txt` – Scenario B O3 4-wide statistics.
- `results/scenario_b_cpu_checksum_stdout.txt` – Saved Scenario B CPU-only checksum and completion output.
- `EXPERIMENT_METADATA.md` – Recorded experiment metadata and documentation.

The repository also contains other workload sources, simulation outputs, and supporting experiment files.

## 8. Scope and Limitations

- The workloads are synthetic CNN-inspired convolution kernels, not trained production neural networks.
- The study does not evaluate object-detection accuracy or use real autonomous-vehicle camera datasets.
- Results are gem5 simulation results, not measurements from physical automotive processors.
- The experiments reported here characterize CPU configurations; they do not claim measured AI-accelerator performance.
- Physical power, energy, silicon area, thermal behaviour, and vehicle-level safety are not evaluated.
- Scenario C is not included in this study.
- Scenario A O3 2-wide is excluded from the standardized comparison because the available completed run used a different padding implementation.

## 9. Reproducibility

The repository provides workload source code, simulation configuration files, and retained result files for inspection.

For reproduction, use the documented simulator environment and ensure that the workload source and gem5 configuration correspond to the experiment being repeated.

## 10. Repository

GitHub: https://github.com/parinithagampala0506-cell/riscv-av-cpu-characterization
