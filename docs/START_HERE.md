# Start Here: Think Like a First-Time Researcher

You do not need advanced quantum mechanics. Start with a question, make a prediction, compare against a control, and explain what the evidence can and cannot show.

## 1. Learn six words

| Word | Meaning in this project |
| --- | --- |
| Qubit | A system described here by two complex amplitudes, alpha and beta. |
| Amplitude | A number used to calculate probabilities. In the Z basis, probabilities are the squared magnitudes of alpha and beta. |
| Gate | A reversible transformation of the amplitudes. |
| Basis | The pair of states the measurement distinguishes. Think of choosing which question to ask. |
| Shot | Prepare a fresh state, apply the gates, then measure once. |
| Phase | An angle carried by an amplitude. Relative phase can affect interference; global phase cannot change probabilities. |

The initial state `0` is the vector `(1, 0)`. A general pure state is `alpha|0> + beta|1>`, with `|alpha|² + |beta|² = 1`. The symbol `i` satisfies `i² = -1`. You can first use the interface without calculating complex numbers by hand.

## 2. Launch and inspect the controls

Follow the README setup commands. Choose **Guided experiments → 1. Establish a control**. Keep 1,000 shots and seed 1806.

Before running, predict whether A and B have the same probabilities. Circuit A has no gates; B has X. Both start in 0 and use Z measurement. Run the experiment. A should return only 0; B should return only 1 in this ideal model.

**Self-check:** What stayed fixed? Initial state, measurement basis, and number of shots. What changed? The X gate.

## 3. Test reversibility

Choose investigation 2. Predict whether H then H gives random outcomes. Run it. Both circuits return 0.

H on 0 produces `(1, 1)/sqrt(2)`. Applying H again gives `(1, 0)`. There is no measurement between the two H gates. This is why two H gates are not two independent coin tosses.

**Self-check:** Can you place a measurement between the H gates and assume the same result? No; that changes the experiment and is outside this app's model.

## 4. Investigate an apparently invisible change

Choose investigation 3. A uses H; B uses H then Z. Both measure in Z. Predict, then run.

- A prepares `|+> = (|0> + |1>)/sqrt(2)`.
- B prepares `|-> = (|0> - |1>)/sqrt(2)`.
- Both have exact Z probabilities of 0.5 and 0.5.

Independent sampled counts can differ even when the probabilities agree. The app deliberately uses separate seeds for A and B. Do not mistake finite-sample variation for evidence that the underlying probabilities differ.

**Question to write down:** Does this mean Z did nothing? A useful next test changes the measurement basis while keeping both preparations fixed.

## 5. Choose a measurement that answers the question

Choose investigation 4. This repeats the same preparations using X measurement. A now returns outcome 0; B returns outcome 1.

The output labels need care:

| Basis | Outcome 0 / eigenvalue +1 | Outcome 1 / eigenvalue -1 | How to implement with ordinary Z readout |
| --- | --- | --- | --- |
| Z | `|0>` | `|1>` | Measure directly. |
| X | `|+>` | `|->` | Apply H, then measure Z. |
| Y | `|+i>` | `|-i>` | Apply S-dagger, then H, then measure Z. |

The extra gates in the last column are readout rotations, separate from state preparation. S-dagger is the inverse of S and equals S repeated three times. The reference validator uses these rotations; the simple simulator computes overlaps directly.

**Conclusion you can defend:** Identical statistics in one basis do not establish state equivalence. For these two orthogonal states, an X measurement distinguishes them perfectly in the ideal model.

## 6. Look for counterexamples to your explanation

Run investigations 5 and 6. It is tempting to conclude that any change of gate order must be observable. Test that claim.

- H then X and X then H on 0 produce different states, visible in X measurement.
- X then Z and Z then X differ only by global phase. No measurement basis distinguishes their final states for the same input.

Read a sequence as a timeline: `H Z` means apply H first and Z second. The corresponding matrix expression is `Z H |psi>`, because the rightmost matrix acts first.

The app's equivalence check concerns the final states for the selected input. It does not generally prove that two gates or circuits are equal on every possible input.

## 7. Add Y and T only after the core makes sense

Investigation 7 prepares plus-i and minus-i. They have equal X and Z probabilities but differ in Y. This shows why inspecting only two axes can miss a difference.

Investigation 8 adds T after H. The exact X outcome-0 probability becomes `(1 + cos(pi/4))/2`, about 0.853553. A probability difference does not mean that a single shot always identifies which state was prepared.

In **Free exploration**, repeat any investigation while changing just one setting. Available gates are X, Y, Z, H, S, and T. An empty sequence is the identity control.

## 8. Keep a reproducible experiment record

Use **Download my experiment** after writing a reflection. The JSON includes preparation, gates, basis, shots, seeds, exact values, sampled values, and your explanation. The file is downloaded by your browser; reflections are not uploaded to a research service.

Use this short lab-note format:

```text
Question:
Prediction and reason:
Control:
Single variable changed:
Initial state / gates / basis / shots / seed:
Observed result:
Does the result support the prediction?
Alternative explanation or limitation:
Next experiment:
```

For investigations 3 and 8, compare 10, 100, 1,000, and 10,000 shots. The exact probability stays fixed. The observed fraction varies. A larger sample usually gives a narrower interval, but an individual run need not move closer to the exact probability.

The approximate 95% Wilson interval describes uncertainty in a binomial probability inferred from counts. Over repeated sampling its coverage is approximately 95%; it does not assign a 95% probability to a fixed parameter or guarantee coverage in this run. See the [NIST explanation](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm).

## Explain it in a three-minute demonstration

1. Show H versus H–Z in Z: same exact probabilities, possibly different sample counts.
2. Switch the investigation to X: the hidden relative phase becomes observable.
3. Show X–Z versus Z–X: explain why a global sign is different from a relative sign.
4. Show the self-check report and say exactly what was tested.

You are ready when you can explain those four points in your own words without claiming hardware access or a new algorithm.
