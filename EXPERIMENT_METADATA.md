# Experiment Metadata

## Recorded Simulation Environment

- Simulator: gem5 25.1.0.1
- Recorded gem5 commit: a9b193c59b55e9266adaf29bb71dee3329270dc3
- Recorded compiler: riscv64-linux-gnu-gcc 15.2.0

### Compiler Configuration

- Scenario A recorded compiler flags: -O2 -static -march=rv64gc -mabi=lp64d.
- Scenario B original optimization flag: Could not be independently recovered from the available command history or executable metadata.
- Scenario B reproducible build: riscv64-linux-gnu-gcc 15.2.0 with -O2 -static -march=rv64gc -mabi=lp64d.
- The newly documented Scenario B executable is byte-for-byte identical to the retained original executable, as confirmed by SHA-256.
- Identical original compiler optimization settings across Scenarios A and B cannot be independently confirmed.
- Scenario A recorded ISA/ABI: RV64GC / LP64D.
- Scenario B reproducible build ISA/ABI: RV64GC / LP64D.

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

## Scenario B Microarchitectural Analysis

The following statistics were collected from the Scenario B CPU-only gem5 simulations.

### D-cache MSHR Analysis

| Statistic | MinorCPU | O3 2-wide | O3 4-wide |
|---|---:|---:|---:|
| D-cache demand accesses | 431,766,502 | 431,649,969 | 431,594,208 |
| D-cache demand misses | 109,459 | 247,559 | 330,108 |
| D-cache demand miss rate | 0.000254 | 0.000574 | 0.000765 |
| Demand MSHR hits | 2,206 | 140,630 | 223,409 |
| Demand MSHR misses | 107,253 | 106,929 | 106,699 |
| MSHR blocked cycles | 0 | 86 | 100 |

In gem5, an MSHR hit indicates that a request matches an existing outstanding miss and can be coalesced with it. An MSHR miss indicates that a new MSHR entry is required.

The following identities hold:

- MinorCPU: 2,206 + 107,253 = 109,459 demand misses.
- O3 2-wide: 140,630 + 106,929 = 247,559 demand misses.
- O3 4-wide: 223,409 + 106,699 = 330,108 demand misses.

Thus, the higher demand-miss counts in the O3 configurations are primarily associated with increased MSHR hits. New MSHR misses remain approximately constant across the three configurations. The demand-miss count should not be interpreted as a proportional increase in unique cache-line misses or external memory traffic.

L2 demand-miss rates were:

- MinorCPU: 0.342990 (34.2990%).
- O3 2-wide: 0.343435 (34.3435%).
- O3 4-wide: 0.344304 (34.4304%).

These rates are similar across the configurations.

### O3 Instruction Retirement Statistics

| Statistic | O3 2-wide | O3 4-wide |
|---|---:|---:|
| Average instructions committed per cycle | 1.516435 | 2.360899 |
| 0 instructions committed | 15.83% | 24.49% |
| 1 instruction committed | 16.69% | 10.57% |
| 2 instructions committed | 67.48% | 11.86% |
| 3 instructions committed | Not applicable | 10.51% |
| 4 instructions committed | Not applicable | 42.56% |
| Squashed instructions skipped by commit | 2,655,553 | 5,203,935 |

O3 2-wide reaches its maximum commit width in 67.48% of sampled cycles. O3 4-wide commits four instructions in 42.56% of sampled cycles and achieves higher average retirement throughput.

### O3 Queue and Pipeline Statistics

| Statistic | O3 2-wide | O3 4-wide |
|---|---:|---:|
| ROB full events | 593 | 33,815 |
| IQ full events | 1,037 | 3,800 |
| SQ full events | 11,203 | 46,893 |
| Dispatch blocked events | 19,532 | 31,727 |
| Branch mispredictions (commit statistic) | 453,548 | 453,576 |
| Average load queue occupancy | 0.05 | 0.07 |
| Average store queue occupancy | 0.02 | 0.02 |

The wider O3 configuration records more ROB-full, IQ-full, and SQ-full events. However, these counters alone do not establish that queue capacity is the single limiting factor. Branch-misprediction counts are nearly identical between the two O3 configurations. The results are therefore reported as observed microarchitectural behaviour rather than proof of one specific performance bottleneck.

### Interpretation and Reporting Notes

- The Scenario B CPU-only comparison uses the same instruction count (2,636,634,126) for all three CPU configurations.
- O3 4-wide achieves higher average retirement throughput than O3 2-wide.
- Higher O3 D-cache demand-miss counts are mainly associated with MSHR hits, not a corresponding increase in new MSHR misses.
- Similar L2 demand-miss rates and nearly identical O3 branch-misprediction counts should be considered when interpreting the performance results.
- The statistics characterize this synthetic CNN-inspired workload under the recorded gem5 configuration. They should not be generalized to all workloads or physical processors.
