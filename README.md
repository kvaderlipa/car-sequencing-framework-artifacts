# Experimental Artifacts and Solver Logs

This repository contains raw solver logs, LP models, solution files, benchmark
datasets, and supporting materials generated or used during the experimental
evaluation presented in the paper:

> **Mixed-Integer Programming Framework for Car Sequencing: Constraint Languages, Objective Families, and Industrial Applications**

The repository serves as a complete experimental artifact accompanying the paper,
providing transparency and supporting reproducibility of the reported computational
results. All solver outputs are stored in their original, unprocessed form.

---

## 1. Experimental Overview

The experiments address three main objectives:
(i) to demonstrate an MILP framework that is practically usable for real-world automotive
production sequencing,
(ii) to validate the ability of the framework to represent and solve classical car-sequencing
benchmark instances from the literature, and 
(iii) to evaluate alternative objective-function designs, including the unexpected
observation that a simpler formulation can outperform more complex, intuitively superior alternatives.

A key methodological aspect of this study is that all color-transition objective-function variants
are directly and fairly comparable by design. Although the formulations differ in
structure and level of sophistication, each objective function represents the same
physical quantity: the absolute number of color transitions (changes) in the production sequence.
Objective values therefore share a common interpretation and can be compared
directly without normalization or post-processing, making performance differences
immediately meaningful from a production perspective.

All artifacts are organized by solver and configuration (Gurobi and SCIP, thread
limits, time limits, and warm-start looping) to enable transparent comparison of
model and objective-function variants under both practical and extended
computational settings.

---

## 2. Repository Structure

The repository layout reflects the experimental narrative and practical relevance
of solver configurations rather than alphabetical order.

### `lp_models`

LP models used in the industrial case-study experiments.

This directory contains LP formulations derived from real-world automotive
production sequencing data. For each sequence day, multiple models are provided
that are **constraint-identical** and differ only in the objective function,
ensuring that all variants are evaluated on exactly the same feasible region.
These models are the source of all solver runs and solution files contained in the
other directories.

#### Industrial Model Naming Convention

LP models follow the naming rule:

`YYYYMMDD_AAxBBBB_Y.lp`

Where:
- `YYYYMMDD` – sequence day
- `AA` – number of car types
- `BBBB` – sequence length
- `Y` – objective-function variant  
  (`0` denotes no objective function; `1–5` denote alternative objective-function
  formulations described and compared in the paper)

For each sequence day:
- a `.desc` file provides a short, human-readable model description,
- a ZIP archive contains all objective-function variants for that day.

---

### `gurobi_8_threads`

Solver output logs and solutions for **Gurobi** runs with no explicit thread limit
(up to 8 threads) and a time limit of 10,800 seconds.

This directory represents the **main experimental setup** discussed in the paper
and corresponds to configurations that are practically usable for real-time
automotive production planning.

Each sequence day and each objective-function variant is solved independently.
Solution files are provided in the accompanying `solutions.zip` archive.

---

### `gurobi_loop_1000_s`

Solver output logs and solutions for **Gurobi** runs executed in a looping setup
with a time limit of 1,000 seconds per run.

Each LP model is solved repeatedly, with the best solution from one run passed as
a warm start to the next. This configuration reflects operational requirements in
which an intermediate solution must be available within a fixed time budget and
allows assessment of the impact of repeated interruption and warm-starting on
solution quality.

---

### `scip`

Solver output logs and solutions for **SCIP** runs with an extended time limit of
350,000 seconds per model.

SCIP is included as a reference solver to study model solvability and scaling
behavior beyond real-time constraints. Although not intended for operational use,
these experiments provide additional validation of the proposed model and
objective-function formulations.

---

### `gurobi_1_thread`

Solver output logs and solutions for **Gurobi** runs limited to a single thread
with a time limit of 10,800 seconds.

Both the default root LP relaxation (root simplex) and a forced root barrier
relaxation (Gurobi parameter `Method = 2`) are included, enabling a methodological
comparison of solver parallelism and root relaxation strategies.

---

### `figures`

Scripts and generated visualizations used in the computational evaluation.

The directory contains Python scripts for parsing solver outputs, generating processed datasets, and creating the figures reported in the paper. It also includes supplementary figures and exploratory analyses that were not included in the final manuscript.

---

### `TESTING_RESULTS.xlsx`

Consolidated experimental results derived from the raw solver logs.

This workbook contains the processed data used to generate the figures and tables reported in the paper. In addition to the published results, it includes supplementary statistics collected during the experimental campaign, allowing readers to inspect solver behavior, compare model variants, and reproduce the reported analyses without parsing the original log files.

---

### `SEQUENCE_MODEL_DEFINITION_MANUAL.xlsx`

Supplementary documentation describing the definition of production constraints
and the LP model generation process. Intended primarily for technical and internal
reference.

---

### `benchmark_CSP`

Academic car-sequencing benchmark instances and validation results used to
complement the industrial evaluation presented in the paper.
 
The directory contains established car-sequencing benchmark instances from the
literature together with results obtained during the framework validation. These
datasets were used to verify that the proposed framework can represent and solve
classical car-sequencing problem instances in addition to the industrial
case-study instances.

Directory structure:

```text
benchmark_CSP/
+-- Pontes2024/
+-- Sun2022/
```

#### `Pontes2024`

Car-sequencing benchmark instances originating from Pontes et al. (2024), 
together with the corresponding framework-validation results.

- `instances/original` contains the original benchmark instances.
- `instances/aggregated` contains the aggregated or preprocessed instances 
used by the proposed framework.
- `results` contains the results obtained during framework validation.


#### `Sun2022`

Car-sequencing benchmark instances originating from Sun et al. (2022), 
together with the corresponding framework-validation results.

- `instances` contains the benchmark problem instances.
- `results` contains the results obtained during framework validation.

---

### `README.md`

This file.

---

## 3. Computational Environment

All experiments were executed on the same dedicated computing environment:

**Hardware**
- CPU: Intel(R) Xeon(R) Gold 6240 @ 2.60 GHz (instruction set: SSE2)
- Cores: 8 physical cores, 8 logical processors
- Memory: 24 GB RAM

**Operating System**
- Windows Server 2016 (64-bit), version 10.0.14393.2

**Solvers**
- Gurobi Optimizer version 11.0.3 (build v11.0.3rc0)
- SCIP version 10.0.0  
  - LP solver: SoPlex 8.0.0  
  - Precision: 8 byte  
  - Memory model: block  
  - Mode: optimized  
  - Git hash: f92057fe19

---

## 4. Reproducibility Notes

- All solver logs are provided in their original, unprocessed form.
- Model constraints correspond to real production rules used for the respective
  sequence days.
- Solver parameters and configurations are documented directly in the solver logs.
- Solution files correspond one-to-one to the reported solver runs using
  consistent naming conventions.  
- Public benchmark instances from the literature are included to support
  independent validation of the proposed framework and reproducibility of the
  benchmark-based experiments reported in the paper.  
- The same hardware and operating system environment was used consistently across
  all solver configurations.

This repository is intended to function as a complete experimental artifact
supporting the results and conclusions reported in the associated paper.