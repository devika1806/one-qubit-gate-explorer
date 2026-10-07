import json
import math
import random
import subprocess
import sys
import unittest

from lessons import LESSONS
from quantum import (GATES, STATES, apply_gate, bloch, equivalent_up_to_global_phase,
                     evolve, experiment, parse_gates, probabilities, sample, wilson_interval)


class QuantumTests(unittest.TestCase):
    def test_six_cardinal_states_in_three_bases(self):
        expected = {
            "0": (0.5, 0.5, 1), "1": (0.5, 0.5, 0),
            "+": (1, 0.5, 0.5), "-": (0, 0.5, 0.5),
            "+i": (0.5, 1, 0.5), "-i": (0.5, 0, 0.5),
        }
        for name, values in expected.items():
            for basis, probability in zip("XYZ", values):
                with self.subTest(state=name, basis=basis):
                    self.assertAlmostEqual(probabilities(STATES[name], basis)["0"], probability)

    def test_hidden_phase_and_revealing_basis(self):
        plus, minus = evolve(("H",))[-1], evolve(("H", "Z"))[-1]
        self.assertEqual(probabilities(plus, "Z"), probabilities(minus, "Z"))
        self.assertEqual(probabilities(plus, "X")["0"], 1)
        self.assertEqual(probabilities(minus, "X")["0"], 0)

    def test_gate_identities_on_all_initial_states(self):
        for name, initial in STATES.items():
            for sequence in [("H", "H"), ("X", "X"), ("Y", "Y"), ("Z", "Z"), ("S",) * 4, ("T",) * 8]:
                self.assertTrue(equivalent_up_to_global_phase(initial, evolve(sequence, name)[-1]))
            self.assertTrue(equivalent_up_to_global_phase(evolve(("H", "Z", "H"), name)[-1],
                                                         evolve(("X",), name)[-1]))

    def test_global_phase_is_not_relative_phase(self):
        plus, minus = STATES["+"], STATES["-"]
        self.assertTrue(equivalent_up_to_global_phase(plus, tuple(-v for v in plus)))
        self.assertFalse(equivalent_up_to_global_phase(plus, minus))
        for initial in STATES:
            self.assertTrue(equivalent_up_to_global_phase(evolve(("X", "Z"), initial)[-1],
                                                         evolve(("Z", "X"), initial)[-1]))

    def test_all_guided_predictions_against_analytic_values(self):
        expected = [(1, 0), (1, 1), (.5, .5), (1, 0), (1, 0), (0, 0), (1, 0),
                    (1, (1 + math.cos(math.pi / 4)) / 2)]
        for lesson, pair in zip(LESSONS, expected):
            values = [probabilities(evolve(parse_gates(lesson[key]), lesson["initial"])[-1], lesson["basis"])["0"]
                      for key in ("a", "b")]
            for actual, predicted in zip(values, pair):
                self.assertAlmostEqual(actual, predicted)
            answer = "Same" if math.isclose(*values, abs_tol=1e-10) else "Different"
            self.assertEqual(answer, lesson["answer"])

    def test_bloch_norm_and_probabilities_for_arbitrary_states(self):
        generator = random.Random(42)
        for _ in range(200):
            theta, phi = generator.random() * math.pi, generator.random() * 2 * math.pi
            state = (math.cos(theta / 2), complex(math.cos(phi), math.sin(phi)) * math.sin(theta / 2))
            for _ in range(12):
                state = apply_gate(state, generator.choice(tuple(GATES)))
            vector = bloch(state)
            self.assertAlmostEqual(sum(v * v for v in vector.values()), 1)
            for basis in "XYZ":
                p = probabilities(state, basis)
                self.assertAlmostEqual(sum(p.values()), 1)
                self.assertAlmostEqual(p["0"], (1 + vector[basis]) / 2)

    def test_shots_are_reproducible_and_conserved(self):
        a = sample(STATES["+"], "Z", 1000, 1806)
        self.assertEqual(a, sample(STATES["+"], "Z", 1000, 1806))
        self.assertEqual(sum(a.values()), 1000)
        self.assertEqual(sample(STATES["0"], "Z", 100), {"0": 100, "1": 0})
        self.assertEqual(sample(STATES["1"], "Z", 100), {"0": 0, "1": 100})

    def test_wilson_reference_values_and_endpoints(self):
        low, high = wilson_interval(50, 100)
        self.assertAlmostEqual(low, 0.4038315303659956)
        self.assertAlmostEqual(high, 0.5961684696340044)
        self.assertAlmostEqual(wilson_interval(0, 100)[0], 0)
        self.assertAlmostEqual(wilson_interval(100, 100)[1], 1)

    def test_input_errors(self):
        self.assertEqual(parse_gates(" h, z H "), ("H", "Z", "H"))
        self.assertEqual(parse_gates(""), ())
        for text in ("CNOT", "H;X", "H " * 25):
            with self.assertRaises(ValueError):
                parse_gates(text)
        for shots in (0, -1, 1.5, True, 100001):
            with self.assertRaises(ValueError):
                sample(STATES["0"], shots=shots)
        for state in ((0, 0), (1, 1), (float("nan"), 0)):
            with self.assertRaises(ValueError):
                probabilities(state)
        with self.assertRaises(ValueError):
            probabilities(STATES["0"], "Q")
        with self.assertRaises(ValueError):
            sample(STATES["0"], seed=-1)

    def test_export_has_reproduction_inputs_and_trace(self):
        data = json.loads(json.dumps(experiment(("H", "S"), basis="Y")))
        self.assertEqual(data["counts"], {"0": 1000, "1": 0})
        self.assertEqual(len(data["trace"]), 3)
        self.assertEqual(data["seed"], 1806)
        self.assertEqual(data["mode"], "ideal classical simulation")

    def test_cli_success_and_invalid_input(self):
        result = subprocess.run([sys.executable, "explore.py", "--gates", "H Z", "--basis", "X"],
                                capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["counts"]["1"], 1000)
        invalid = subprocess.run([sys.executable, "explore.py", "--gates", "CNOT"], capture_output=True, text=True)
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("Unknown gate", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
