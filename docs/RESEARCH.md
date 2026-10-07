# Research References and Comparison

Sources checked on **7 October 2026**. This is a focused review of relevant primary sources, not an exhaustive literature review or proof of originality.

## How sources were selected

Prefer official documentation, authors' code repositories, and identifiable research papers with stable publication metadata. Separate reviewed research software from teaching tools. Do not treat a search ranking, GitHub popularity, or an AI-generated project description as scientific validation.

The two main research-software comparators are **Qiskit Experiments** and **QuTiP**. **Quirk** is a teaching-tool comparator. Qiskit SDK documentation supplies the exact API used for the numerical reference check.

## 1. Qiskit Experiments — research-software comparator

[Kanazawa et al., 2023, Journal of Open Source Software 8(84), 5329](https://joss.theoj.org/papers/10.21105/joss.05329), DOI `10.21105/joss.05329`.

**Reliability evidence:** the journal page identifies authors, publication date, reviewers, review history, software repository, and archive. This is a published research-software project, not an anonymous tutorial.

The project's [official state-tomography tutorial](https://qiskit-community.github.io/qiskit-experiments/manuals/verification/state_tomography.html) describes reconstructing a state from repeated preparations and measurements in a complete set of bases. It also handles issues such as physical density-matrix fitting.

**Design lesson:** one measurement basis is insufficient to reconstruct an arbitrary qubit. This explorer therefore exposes X, Y, and Z readout and carefully distinguishes an exact simulated state from measured data.

**Boundary:** this repository does not run the Qiskit Experiments tomography fitter, reproduce its published experiments, or implement hardware characterization. Its Bloch coordinates are calculated directly from the known ideal state.

## 2. QuTiP — independent numerical reference

[Johansson, Nation and Nori, QuTiP 2](https://arxiv.org/abs/1211.6518), published in *Computer Physics Communications* 184, 1234–1240 (2013), DOI [`10.1016/j.cpc.2012.11.019`](https://doi.org/10.1016/j.cpc.2012.11.019).

**Reliability evidence:** the authors' preprint records the journal reference and DOI. The [official project](https://qutip.org/) and [state/operator guide](https://qutip.readthedocs.io/en/stable/guide/guide-states.html) document an established scientific simulation library. The paper establishes provenance; the current documentation supports the current API.

**What was used:** QuTiP 5.3.1 constructs reference states and operators, then calculates Pauli expectation values. The validator converts each expectation value `r` to outcome-0 probability `(1+r)/2`.

**Boundary:** no open-system solver or noise model was executed. Agreement validates this finite set of ideal calculations, not every feature of QuTiP or every possible one-qubit program.

## 3. Qiskit SDK — independent circuit reference

[IBM's official Statevector API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector) documents circuit evolution, probabilities, and equivalence up to global phase.

**What was used:** Qiskit 2.5.2 builds the same gate timelines independently. For X readout it appends H; for Y readout it appends S-dagger followed by H. It then calculates computational-basis probabilities. This differs from the teaching engine's direct overlap calculation and helps expose basis-convention bugs.

Qiskit SDK is related to, but distinct from, Qiskit Experiments. Running this SDK comparison is not a claim that the Experiments package was executed.

## 4. Quirk — educational comparison

[Craig Gidney's Quirk repository](https://github.com/Strilanc/Quirk) and [maintainer's usage guide](https://github.com/Strilanc/Quirk/wiki/How-to-use-Quirk).

**Reliability evidence:** original source repository and maintainer documentation. This is a transparent teaching tool; it is not being represented here as a peer-reviewed research paper.

**Design lesson:** small circuits benefit from immediate visible feedback. Our scope adds a specific predict–observe–explain sequence and paired controls. This is a design choice, not a claim that no existing tool has similar learning features.

**Execution status:** its documentation and source overview were reviewed; no automated numerical comparison with Quirk was run.

## 5. Sampling uncertainty

[NIST/SEMATECH: Confidence intervals for proportions](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm) supports the Wilson interval used beside observed proportions. This measures sampling uncertainty, not noise in a physical quantum processor.

## Comparison and resulting decisions

| Reference | Established strength | Our smaller scope | Check performed |
| --- | --- | --- | --- |
| Qiskit Experiments | Experimental characterization and tomography | Teach why more than one basis matters | Documentation and paper review; no fitter execution. |
| QuTiP | Scientific state/operator calculations and dynamics | One pure qubit with discrete gates | Numerical probability comparison. |
| Qiskit SDK | Quantum circuit/state simulation | Independent preparation and rotated readout | Numerical probability comparison. |
| Quirk | Interactive small-circuit exploration | Eight guided paired experiments | Documentation-level design comparison only. |

## Research questions and falsifiable checks

| Hypothesis | Control / intervention | Prediction that can fail |
| --- | --- | --- |
| Relative phase can be invisible in one basis | H versus HZ, measured in Z | Both have P(0)=0.5. |
| A changed basis can reveal the phase | Same preparations, switch to X | P(0)=1 versus P(0)=0. |
| More shots cannot recover information absent from the chosen basis | Repeat H/HZ in Z at larger shot counts | Exact distributions stay identical. |
| Gate order can matter | HX versus XH from 0, measured in X | Opposite deterministic outcomes. |
| A global sign is unobservable | XZ versus ZX with the same input | Identical probabilities in all bases. |
| Two axes can miss a difference | HS versus HSSS from 0 | X/Z agree; Y differs. |

These predictions follow from elementary matrix algebra and are tested in the project. They are not empirical discoveries or claims derived from running someone else's full research experiment.

## Remaining threats to validity

- All executed comparisons assume ideal unitary evolution and perfect readout.
- Both libraries and this implementation ultimately implement the same mathematical theory; software agreement is not independent physical evidence.
- The numerical grid is finite and does not cover arbitrary long circuits, continuous rotations, noise, or mixed states.
- The interface reveals exact states unavailable from a single real measurement. Labels make this distinction explicit.
- Learning effectiveness has not been evaluated with students. The teaching workflow is a proposal supported by a working tool, not a measured educational outcome.
