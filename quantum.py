"""A transparent one-qubit simulator. Only Python's standard library is needed.

Read gates left to right in time. Measurement is performed only at the end.
The two stored complex numbers are amplitudes, not probabilities.
"""

from __future__ import annotations

import math
import random
import re

SQRT2 = math.sqrt(2)
STATES = {
    "0": (1 + 0j, 0j),
    "1": (0j, 1 + 0j),
    "+": (1 / SQRT2, 1 / SQRT2),
    "-": (1 / SQRT2, -1 / SQRT2),
    "+i": (1 / SQRT2, 1j / SQRT2),
    "-i": (1 / SQRT2, -1j / SQRT2),
}
GATES = {
    "X": ((0, 1), (1, 0)),
    "Y": ((0, -1j), (1j, 0)),
    "Z": ((1, 0), (0, -1)),
    "H": ((1 / SQRT2, 1 / SQRT2), (1 / SQRT2, -1 / SQRT2)),
    "S": ((1, 0), (0, 1j)),
    "T": ((1, 0), (0, complex(math.cos(math.pi / 4), math.sin(math.pi / 4)))),
}
BASES = {"Z": ("0", "1"), "X": ("+", "-"), "Y": ("+i", "-i")}
MAX_GATES = 24
MAX_SHOTS = 100_000


def parse_gates(text: str) -> tuple[str, ...]:
    """Accept 'H Z H' or 'h,z,h'; an empty string means no gates."""
    if not isinstance(text, str):
        raise ValueError("Enter gate names as text, for example H Z H.")
    gates = tuple(word for word in re.split(r"[\s,]+", text.strip().upper()) if word)
    if len(gates) > MAX_GATES:
        raise ValueError(f"Use at most {MAX_GATES} gates for a readable experiment.")
    unknown = [gate for gate in gates if gate not in GATES]
    if unknown:
        raise ValueError(f"Unknown gate: {unknown[0]}. Choose X, Y, Z, H, S, or T.")
    return gates


def validate_state(state):
    if len(state) != 2:
        raise ValueError("A one-qubit state needs exactly two amplitudes.")
    values = tuple(complex(value) for value in state)
    if not all(math.isfinite(v.real) and math.isfinite(v.imag) for v in values):
        raise ValueError("Amplitudes must be finite.")
    if not math.isclose(sum(abs(v) ** 2 for v in values), 1, abs_tol=1e-10):
        raise ValueError("Squared amplitude magnitudes must sum to one.")
    return values


def apply_gate(state, gate: str):
    a, b = validate_state(state)
    if gate not in GATES:
        raise ValueError(f"Unsupported gate: {gate}")
    matrix = GATES[gate]
    return (matrix[0][0] * a + matrix[0][1] * b,
            matrix[1][0] * a + matrix[1][1] * b)


def evolve(gates=(), initial="0"):
    """Return the input and every intermediate state, with no measurements."""
    if initial not in STATES:
        raise ValueError("Choose initial state 0, 1, +, -, +i, or -i.")
    gates = tuple(gates)
    if len(gates) > MAX_GATES:
        raise ValueError(f"Use at most {MAX_GATES} gates.")
    history = [STATES[initial]]
    for gate in gates:
        history.append(apply_gate(history[-1], gate))
    return history


def probabilities(state, basis="Z"):
    """Born rule: square the overlap with the +1 eigenstate of the chosen axis."""
    state = validate_state(state)
    if basis not in BASES:
        raise ValueError("Measurement basis must be X, Y, or Z.")
    plus = STATES[BASES[basis][0]]
    overlap = sum(complex(v).conjugate() * a for v, a in zip(plus, state))
    p0 = min(1.0, max(0.0, abs(overlap) ** 2))
    # Remove floating-point residue for mathematically deterministic cases.
    if p0 < 1e-14:
        p0 = 0.0
    elif p0 > 1 - 1e-14:
        p0 = 1.0
    return {"0": p0, "1": 1 - p0}


def bloch(state):
    a, b = validate_state(state)
    product = a.conjugate() * b
    return {"X": 2 * product.real, "Y": 2 * product.imag,
            "Z": abs(a) ** 2 - abs(b) ** 2}


def sample(state, basis="Z", shots=1000, seed=1806):
    if type(shots) is not int or not 1 <= shots <= MAX_SHOTS:
        raise ValueError(f"Shots must be a whole number from 1 to {MAX_SHOTS}.")
    if type(seed) is not int or not 0 <= seed <= 2**32 - 1:
        raise ValueError("Seed must be a whole number from 0 to 4294967295.")
    p0 = probabilities(state, basis)["0"]
    generator = random.Random(seed)
    zeros = sum(generator.random() < p0 for _ in range(shots))
    return {"0": zeros, "1": shots - zeros}


def wilson_interval(successes, total):
    """Approximate 95% Wilson score interval for a binomial proportion."""
    if type(total) is not int or total < 1 or type(successes) is not int or not 0 <= successes <= total:
        raise ValueError("Counts must be whole numbers with 0 <= successes <= total.")
    z = 1.959963984540054
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return [max(0, center - half), min(1, center + half)]


def equivalent_up_to_global_phase(left, right):
    left, right = validate_state(left), validate_state(right)
    overlap = sum(a.conjugate() * b for a, b in zip(left, right))
    return math.isclose(abs(overlap), 1, rel_tol=0, abs_tol=1e-10)


def experiment(gates=(), initial="0", basis="Z", shots=1000, seed=1806):
    gates = tuple(gates)
    history = evolve(gates, initial)
    state = history[-1]
    counts = sample(state, basis, shots, seed)
    return {
        "initial": initial, "gates": list(gates), "basis": basis,
        "shots": shots, "seed": seed, "mode": "ideal classical simulation",
        "probabilities": probabilities(state, basis), "counts": counts,
        "observed_p0": counts["0"] / shots,
        "p0_wilson_95": wilson_interval(counts["0"], shots),
        "bloch": bloch(state),
        "amplitudes": [[complex(v).real, complex(v).imag] for v in state],
        "trace": [{"step": i, "gate": "start" if i == 0 else gates[i - 1],
                   **bloch(s)} for i, s in enumerate(history)],
    }
