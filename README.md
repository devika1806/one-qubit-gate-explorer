# One-Qubit Gate Explorer

**A beginner's investigation into gates, hidden phase, and choosing the right measurement.**

Why can two different quantum states produce the same 50/50 counts? What can you change to tell them apart? This project answers those questions through eight short experiments and a free exploration mode.

Built for `devika1806`. This is an educational software project, not a claim of a new quantum algorithm or research discovery.

## What is included

- Eight guided investigations: predict → run → inspect → explain → repeat.
- Six gates: X, Y, Z, H, S, and T; six starting states; X, Y, and Z measurement bases.
- Side-by-side circuit comparisons, exact probabilities, sampled counts, and sampling uncertainty.
- A state trace after each gate and exact Bloch coordinates.
- Downloadable experiment records with settings, seeds, predictions, and reflections.
- A command-line tool that uses only Python's standard library.
- Automated checks and an independent numerical comparison with Qiskit and QuTiP.

## Start in two minutes

You need Python installed. The completed local verification used **Python 3.14.4 on Windows**. Other environments have not been locally verified; the repository includes a proposed Linux CI workflow.

Open a terminal in this repository. Try the central experiment without installing anything:

```powershell
python explore.py --gates "H Z" --basis Z
python explore.py --gates "H Z" --basis X
```

The first command predicts 50/50 outcomes. The second predicts outcome 1 with certainty in the ideal model. The state preparation is the same; only the measurement basis changes.

For the visual interface on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open [the local explorer](http://localhost:8501). Stop the server with Ctrl+C. If `.venv` already exists, reuse it. These commands do not require PowerShell activation or an execution-policy change.

On macOS/Linux, use `.venv/bin/python` instead of `.\.venv\Scripts\python.exe`. Those commands are provided for portability, not as a claim of a completed platform test.

## Learn in the right order

1. Follow [Start Here](docs/START_HERE.md): vocabulary, exact actions, expected observations, and self-check answers.
2. Read the [critical path and scope decisions](docs/CRITICAL_PATH.md).
3. Examine [reliable references and project comparisons](docs/RESEARCH.md).
4. Inspect [the self-check report](docs/SELF_CHECK.md) and [machine-readable numerical results](results/research-validation.json).

The main learning sequence is:

| Investigation | Question |
| --- | --- |
| 1. Establish a control | Does X change a qubit prepared in 0? |
| 2. Undo a gate | Why does H followed by H return the starting state? |
| 3. Find the hidden phase | Can two different states have the same Z probabilities? |
| 4. Choose a better measurement | Can an X measurement reveal that difference? |
| 5. Test gate order | Does H then X behave like X then H? |
| 6. Recognize global phase | Does an overall minus sign change any measurement probability? |
| 7. Look along Y | What does a third measurement axis reveal? |
| 8. Explore a smaller phase | What changes when the phase shift is pi/4? |

## Reproduce the checks

The standard-library tests run without the interface installed. The interface test is explicitly skipped if Streamlit is unavailable.

```powershell
python -m unittest discover -s tests -v
python run_experiments.py
```

For the independent reference comparison:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-research.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe verify_references.py
```

New output goes to ignored `local-results/`. Committed `results/` files preserve the actual checked run. Top-level package versions are pinned; `requirements-lock.txt` records the full environment used for the original verification.

## Repository map

```text
app.py                    visual learning interface
quantum.py                small, inspectable simulator
lessons.py                questions and explanations
explore.py                command-line entry point
run_experiments.py        reproducible lesson outputs
verify_references.py      comparison with Qiskit and QuTiP
tests/                    mathematical and interface checks
docs/                     learning steps, research, critical path, self-check
results/                  actual saved numerical results
```

## Scientific limits

The model contains one ideal, pure qubit, unitary gates, and a final projective measurement. It has no entanglement, noise, intermediate measurement, or physical quantum device. Sampled counts use a classical pseudorandom generator. More shots reduce typical sampling uncertainty; they do not reveal a phase that the chosen measurement cannot see.

The finite reference check covers all sequences of length 0–4 in the selected gate set, not all quantum circuits or all possible continuous states. The interface accepts up to 24 gates for exploration.

Qiskit Experiments and QuTiP have published research-software papers; Quirk is used as an educational comparison. Their different roles, exact links, and what was actually executed are recorded in [RESEARCH.md](docs/RESEARCH.md).

## GitHub publication

Public repository: [devika1806/one-qubit-gate-explorer](https://github.com/devika1806/one-qubit-gate-explorer). See [publication and update steps](docs/PUBLISH.md).
