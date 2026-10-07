"""Cross-check every sequence of 0..4 gates against Qiskit and QuTiP.

References use their own gates and different measurement calculations.
This is a numerical replication check, not a quantum hardware experiment.
"""

import argparse
import itertools
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path

import qiskit
import qutip
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantum import evolve, probabilities


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="local-results/research-validation.json")
    args = parser.parse_args()
    gate_names = ("X", "Y", "Z", "H", "S", "T")
    # Construct reference input states independently of quantum.STATES.
    zero, one = qutip.basis(2, 0), qutip.basis(2, 1)
    inputs = {"0": zero, "1": one, "+": (zero + one).unit(), "-": (zero - one).unit(),
              "+i": (zero + 1j * one).unit(), "-i": (zero - 1j * one).unit()}
    paulis = {"X": qutip.sigmax(), "Y": qutip.sigmay(), "Z": qutip.sigmaz()}
    qt_gates = {**paulis, "H": (paulis["X"] + paulis["Z"]) / math.sqrt(2),
                # Rz differs from S/T by only a global phase, irrelevant to probabilities.
                "S": (-1j * math.pi / 4 * paulis["Z"]).expm(),
                "T": (-1j * math.pi / 8 * paulis["Z"]).expm()}
    rotations = {}
    for basis in "XYZ":
        circuit = QuantumCircuit(1)
        if basis == "Y":
            circuit.sdg(0)
        if basis in "XY":
            circuit.h(0)
        rotations[basis] = circuit
    max_error = {"qiskit": 0.0, "qutip": 0.0}
    sequence_count = setting_count = 0
    for length in range(5):
        for gates in itertools.product(gate_names, repeat=length):
            sequence_count += 1
            circuit = QuantumCircuit(1)
            for gate in gates:
                getattr(circuit, gate.lower())(0)
            for initial, qt_input in inputs.items():
                own_state = evolve(gates, initial)[-1]
                qi_state = Statevector(qt_input.full().ravel()).evolve(circuit)
                qt_state = qt_input
                for gate in gates:
                    qt_state = qt_gates[gate] * qt_state
                for basis in "XYZ":
                    setting_count += 1
                    own_p0 = probabilities(own_state, basis)["0"]
                    refs = {
                        "qiskit": float(qi_state.evolve(rotations[basis]).probabilities()[0]),
                        "qutip": float((1 + qutip.expect(paulis[basis], qt_state)) / 2),
                    }
                    for backend, reference in refs.items():
                        error = abs(own_p0 - reference)
                        max_error[backend] = max(max_error[backend], error)
                        if error > 1e-10:
                            raise AssertionError(f"{backend}: {initial=}, {gates=}, {basis=}, {own_p0=}, {reference=}")
    result = {
        "status": "PASS", "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "qiskit": qiskit.__version__, "qutip": qutip.__version__,
        "gate_set": list(gate_names), "max_sequence_length": 4,
        "initial_states": list(inputs), "measurement_bases": list("XYZ"),
        "sequences": sequence_count, "settings_per_reference": setting_count,
        "total_reference_comparisons": 2 * setting_count, "absolute_tolerance": 1e-10,
        "max_absolute_probability_error": max_error,
        "scope": "Exact ideal probabilities only. No external hardware, noise model, or Qiskit Experiments fitter was run.",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
