# Self-Check Report

Checked on **7 October 2026**, using Python 3.14.4 on Windows. These are actual local checks, not planned work or GitHub Actions results.

## Results

| Check | Result | Evidence and scope |
| --- | --- | --- |
| Analytical behavior, inputs, CLI, and exports | PASS | 11 standard-library test methods, including all eight lesson predictions. |
| Interface behavior | PASS | Streamlit AppTest: prediction/reveal, settings reset, control and hidden-phase results, invalid-input handling. |
| Independent reference agreement | PASS | 27,990 settings per library; 55,980 probability comparisons in total. |
| Package consistency | PASS | `pip check`: no broken requirements. |
| No-dependency path | PASS | System Python ran all 11 core tests; the optional interface test was explicitly skipped. |
| Live interface | PASS | Opened locally in the browser; selected the X-basis phase investigation, submitted a prediction, and inspected results. |
| Physical quantum device | NOT RUN | This project is an ideal simulator. |
| Qiskit Experiments tomography fitter | NOT RUN | Used as a research/design reference only. |
| Quirk numerical comparison | NOT RUN | Documentation-level teaching-tool comparison only. |
| GitHub Actions | NOT RUN LOCALLY | A workflow is provided; remote execution requires publication. |

Read the exact numerical evidence in [research-validation.json](../results/research-validation.json). The complete reference check uses all 1,555 gate sequences of length 0–4, six starting states, and three measurement bases.

| Reference | Version | Maximum absolute probability error | Required tolerance |
| --- | --- | --- | --- |
| Qiskit SDK | 2.5.2 | 8.881784197001252e-16 | 1e-10 |
| QuTiP | 5.3.1 | 7.771561172376096e-16 | 1e-10 |

Qiskit computes probabilities after readout rotations. QuTiP uses Pauli expectation values. The small simulator uses direct state overlaps. The different calculation paths reduce the chance of sharing a measurement-basis mistake. Agreement is still a software/mathematics check, not physical experimental evidence.

## Selected observed runs

All rows below use 1,000 simulated shots. Exact probabilities are model predictions; counts are actual outputs from the saved run. See [experiments.csv](../results/experiments.csv) for each seed and [experiments.json](../results/experiments.json) for complete records.

| Preparation from 0 | Basis | Exact P(0) | Observed 0 / 1 | Interpretation |
| --- | --- | --- | --- | --- |
| H | Z | 0.5 | 493 / 507 | A finite sample fluctuates around the model. |
| H then Z | Z | 0.5 | 474 / 526 | Different counts do not imply different underlying probabilities. |
| H | X | 1 | 1000 / 0 | Plus is deterministic in X. |
| H then Z | X | 0 | 0 / 1000 | The relative phase is revealed in X. |
| H then T | X | 0.8535533906 | 852 / 148 | A partial phase shift changes a probability. |

The lesson-generation script assigns seeds starting at 1806 and increments them for each circuit. The interface uses the selected seed for A and the next seed for B. Match the saved per-circuit seed when reproducing a specific count.

## What the tests deliberately check

- Six cardinal states in three measurement bases, including the sign of Y.
- H²=X²=Y²=Z²=I, S⁴=I, T⁸=I, and HZH=X on all six initial states.
- Global phase equivalence without confusing it with relative phase.
- Normalization and the Born/Bloch relationship for 200 generated continuous pure states, each evolved through 12 gates.
- Count conservation, deterministic controls, fixed-seed reproducibility, and Wilson interval reference values.
- Invalid gates, invalid shot counts, invalid states, invalid bases, and invalid seeds.
- JSON records that include settings and state traces, plus successful and invalid CLI calls.
- Hiding results before a prediction and resetting old results when a new investigation is selected.

## Limits of this self-check

This does not prove all code is bug-free. The cross-library grid stops at four gates and six specific input states. Continuous-state invariant tests extend coverage but are not an exhaustive independent-library comparison. Browser behavior was inspected locally; other browsers, operating systems, and accessibility assistive technologies have not received comprehensive testing.

No learning-effectiveness study, physical noise experiment, security audit, or performance claim is included. The complete dependency snapshot is in [requirements-lock.txt](../requirements-lock.txt).

## Reproduce

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe verify_references.py
.\.venv\Scripts\python.exe run_experiments.py
.\.venv\Scripts\python.exe -m pip check
```

QuTiP may warn that Matplotlib is unavailable. The validator uses numerical operators only, so plotting support is not required. Streamlit's AppTest may emit a bare-mode context warning; inspect the test status and exceptions rather than treating the warning as a result.
