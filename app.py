"""Run with: python -m streamlit run app.py"""

import json

import altair as alt
import streamlit as st

from lessons import LESSONS
from quantum import BASES, STATES, bloch, equivalent_up_to_global_phase, evolve, experiment, parse_gates

st.set_page_config(page_title="One-Qubit Gate Explorer", page_icon="🔬", layout="wide")
st.title("One-Qubit Gate Explorer")
st.markdown("### Discover what a measurement can miss.")
st.write("Prepare a qubit, change a gate, and choose how to measure it. Make a prediction before revealing the evidence.")
st.caption("An ideal simulation on your laptop • One qubit • No quantum hardware or account required")

mode = st.sidebar.radio("Learning mode", ["Guided experiments", "Free exploration"])
shots = st.sidebar.select_slider("Shots per circuit", options=[10, 100, 1000, 10000], value=1000)
seed = int(st.sidebar.number_input("Random seed", min_value=0, max_value=4294967295, value=1806, step=1))
st.sidebar.caption("A shot is a fresh preparation followed by one measurement. A fixed seed makes this simulation repeatable.")

if mode == "Guided experiments":
    title = st.selectbox("Choose an investigation", [lesson["title"] for lesson in LESSONS])
    lesson = next(item for item in LESSONS if item["title"] == title)
    initial, basis = lesson["initial"], lesson["basis"]
    a_text, b_text = lesson["a"], lesson["b"]
    st.info(lesson["question"])
else:
    lesson = None
    initial = st.selectbox("Initial state", list(STATES))
    basis = st.selectbox("Measurement basis", list(BASES))
    a_text = st.text_input("Circuit A gates", "H", help="X Y Z H S T; separate with spaces. Leave empty for a control.")
    b_text = st.text_input("Circuit B gates", "H Z", help="Gates run left to right. Up to 24 gates.")

try:
    gates_a, gates_b = parse_gates(a_text), parse_gates(b_text)
except ValueError as error:
    st.error(str(error))
    st.stop()

st.code(f"A: |{initial}>  →  {' → '.join(gates_a) or '(no gates)'}  →  measure {basis}\n"
        f"B: |{initial}>  →  {' → '.join(gates_b) or '(no gates)'}  →  measure {basis}", language=None)
st.caption("Read gates left to right in time. State preparation is separate from the gates you are comparing.")

settings = (mode, initial, basis, a_text, b_text, shots, seed)
if st.session_state.get("settings") != settings:
    st.session_state.settings = settings
    st.session_state.revealed = False
    st.session_state.prediction = "Not sure yet"
    st.session_state.reason = ""
    st.session_state.reflection = ""

with st.form("prediction_form"):
    st.subheader("1 · Predict")
    prediction = st.radio("Will the exact outcome probabilities be the same or different?",
                          ["Not sure yet", "Same", "Different"], horizontal=True, key="prediction")
    reason = st.text_input("My reason (optional)", key="reason")
    submitted = st.form_submit_button("Run experiment", type="primary")
if submitted:
    st.session_state.revealed = True
    st.session_state.recorded_prediction = prediction
    st.session_state.recorded_reason = reason

if not st.session_state.get("revealed"):
    st.info("Choose a prediction, or keep ‘Not sure yet’, then run the experiment.")
    st.stop()

# Separate random streams: equal probabilities need not produce equal observed counts.
result_a = experiment(gates_a, initial, basis, shots, seed)
result_b = experiment(gates_b, initial, basis, shots, (seed + 1) % 2**32)
same = abs(result_a["probabilities"]["0"] - result_b["probabilities"]["0"]) < 1e-10
answer = "Same" if same else "Different"
recorded = st.session_state.recorded_prediction
st.subheader("2 · Examine the evidence")
st.write(f"**Exact probabilities: {answer.lower()}.** Your prediction: {recorded}.")
if recorded != "Not sure yet":
    if recorded == answer:
        st.success("Your prediction agrees with the model. Explain why before moving on.")
    else:
        st.warning("This is a useful counterexample. Revise the explanation using the evidence below.")

for column, name, result in zip(st.columns(2), ["A", "B"], [result_a, result_b]):
    with column:
        st.markdown(f"#### Circuit {name}")
        st.metric("Exact probability of outcome 0", f"{result['probabilities']['0']:.2%}")
        bars = [{"outcome": str(i), "series": series, "fraction": value}
                for i in (0, 1)
                for series, value in [("Exact probability", result["probabilities"][str(i)]),
                                      ("Observed fraction", result["counts"][str(i)] / shots)]]
        chart = alt.Chart(alt.Data(values=bars)).mark_bar().encode(
            x=alt.X("outcome:N", title="Measurement outcome", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("fraction:Q", title="Probability / fraction", scale=alt.Scale(domain=[0, 1])),
            xOffset="series:N", color=alt.Color("series:N", title=None),
            tooltip=["outcome:N", "series:N", alt.Tooltip("fraction:Q", format=".3f")],
        ).properties(height=230)
        st.altair_chart(chart, width="stretch")
        st.caption("Horizontal labels 0 and 1 are measurement outcomes. Bar heights are fractions from 0 to 1.")
        st.write(f"Counts: **0 → {result['counts']['0']}**, **1 → {result['counts']['1']}**")
        low, high = result["p0_wilson_95"]
        st.caption(f"Observed fraction of 0: {result['observed_p0']:.3f}; approximate 95% Wilson interval: [{low:.3f}, {high:.3f}].")

plus, minus = BASES[basis]
st.info(f"In the {basis} basis, outcome 0 means |{plus}> (eigenvalue +1); outcome 1 means |{minus}> (eigenvalue −1).")
st.caption("The exact probabilities come from the mathematical state. Counts are pseudorandom samples. The interval describes finite-sample uncertainty; it is not device error or a guarantee of containing the true probability.")

st.subheader("3 · Look beyond one measurement")
state_a, state_b = evolve(gates_a, initial)[-1], evolve(gates_b, initial)[-1]
coordinates = [dict(circuit="A", **bloch(state_a)), dict(circuit="B", **bloch(state_b))]
st.dataframe(coordinates, hide_index=True, width="stretch")
st.caption("These are exact Bloch coordinates from the simulator. Each axis is an expectation value between −1 and +1. They are not three outcomes measured simultaneously on one qubit.")
equivalent = equivalent_up_to_global_phase(state_a, state_b)
st.write("**Same physical pure state (up to global phase):** " + ("Yes" if equivalent else "No"))
if same and not equivalent:
    st.warning("This measurement hides a difference. Try another basis in Free exploration.")
with st.expander("Follow the state after each gate"):
    st.write("Each row is a mathematical snapshot before final measurement, not a measurement inserted into the circuit.")
    for name, result in [("A", result_a), ("B", result_b)]:
        st.write(f"Circuit {name}")
        st.dataframe(result["trace"], hide_index=True, width="stretch")
        st.caption(f"Final amplitudes [real, imaginary]: {result['amplitudes']}")

st.subheader("4 · Revise and repeat")
if lesson:
    st.write(lesson["why"])
st.write("Change just one thing: the measurement basis, gate order, initial state, or shot count. Predict what will change before running again.")
reflection = st.text_area("What did I learn, and what should I test next?", key="reflection")
record = {"schema_version": 1, "prediction": recorded,
          "reason": st.session_state.recorded_reason, "reflection": reflection,
          "exact_answer": answer, "equivalent_up_to_global_phase": equivalent,
          "A": result_a, "B": result_b}
st.download_button("Download my experiment (JSON)", json.dumps(record, indent=2),
                   file_name="qubit-experiment.json", mime="application/json")
st.caption("Simulation only. The educational contribution is the investigation workflow; the physics is established. No quantum speedup, entanglement, hardware noise, or new research result is claimed.")
