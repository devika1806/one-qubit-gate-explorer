"""Optional UI smoke checks; install requirements.txt to run them."""

import importlib.util
import unittest
from pathlib import Path


@unittest.skipUnless(importlib.util.find_spec("streamlit"), "Optional Streamlit dependency is not installed")
class InterfaceTests(unittest.TestCase):
    def test_prediction_reveal_reset_and_invalid_input(self):
        from streamlit.testing.v1 import AppTest

        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.metric), 0, "Evidence must be hidden before the prediction step")
        app.button[0].click().run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual([metric.value for metric in app.metric], ["100.00%", "0.00%"])
        app.selectbox[0].select("3. Find the hidden phase").run(timeout=30)
        self.assertEqual(len(app.metric), 0, "A changed experiment needs a fresh reveal")
        app.button[0].click().run(timeout=30)
        self.assertEqual([metric.value for metric in app.metric], ["50.00%", "50.00%"])
        app.sidebar.radio[0].set_value("Free exploration").run(timeout=30)
        app.text_input[0].set_value("CNOT").run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertIn("Unknown gate", app.error[0].value)


if __name__ == "__main__":
    unittest.main()
