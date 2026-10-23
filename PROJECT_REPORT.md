# QuantumShield: Quantum Kernel-Based Network Intrusion Detection

**Interstate Quantum Hackathon 2026 — QML track**

**Team name:** [ADD]

**Team members:** [FULL NAME 1], [FULL NAME 2]

**Affiliation / department / career level:** [ADD BOTH MEMBERS]

**Submission category:** [Rising-star / Champion, subject to judging committee determination]

## Executive summary
- Implemented a quantum kernel support vector classifier (QSVC) using a four-qubit feature map.
- Compared a classical RBF SVM with non-entangling Z and entangling ZZ quantum kernels.
- Used NSL-KDD benign/attack records with distinct train and test sources.
- Selected quantum bandwidth using cross-validation **on training data only**.
- [REPLACE WITH OBSERVED RESULT — DO NOT INVENT ACCURACY]

## Motivation
We investigate whether quantum feature mapping and entanglement can capture useful structure in network intrusion data. The motivation is exploratory, not a claim of quantum acceleration or operational threat protection.

## Method
**Dataset:** NSL-KDD 20% train file / independent NSL-KDD test file.

**Sample sizes:** 80 training samples (40 benign, 40 attack) and 40 held-out test samples (20 of each), random seed 42.

**Features:** `src_bytes`, `dst_bytes`, `count`, `srv_serror_rate`.

**Preprocessing:** `log1p` for byte/count columns; fit MinMax scaler on training subset only to [0, π], clip test encoding range.

**Models:** Classical SVC with RBF kernel; Quantum QSVC with Z feature map; QSVC with entangling ZZ feature map (4 qubits; reps=2; local exact statevector simulator). SVM penalty C=1.0 throughout. Quantum λ chosen via 3-fold CV on the training records.

## Results
**Insert actual numbers from `results/metrics.csv`, no hypothetical values.**

| Model | Balanced accuracy | Attack precision | Attack recall | Attack F1 | False-positive rate |
|---|---:|---:|---:|---:|---:|
| Classical RBF SVM | TBD | TBD | TBD | TBD | TBD |
| Quantum Z QSVC | TBD | TBD | TBD | TBD | TBD |
| Quantum ZZ QSVC | TBD | TBD | TBD | TBD | TBD |

**Figures:** Insert `results/model_comparison.png`, `results/confusion_matrices.png`, `results/kernel_comparison.png`.

**Bandwidth CV:** Summarize `results/bandwidth_cv.csv` and selected λ.

## Interpretation
[Explain whether entanglement helped *on this specific sample*, how quantum compared with RBF, what confusion matrices show, and possible reasons. Be transparent if classical performs better.]

## Limitations
Small deliberately balanced datasets, selection variability, legacy NSL-KDD, only four numerical features, clipped feature transforms, simulator computation rather than quantum hardware, no established speedup or deployment readiness.

## Reproducibility
Run all cells in `QuantumShield.ipynb`. Input files download from public NSL-KDD mirror. Exact parameters are in `results/experiment_config.json`.

## References
- IQ Hackathon Fall 2026 launch and QML pre-training lecture (organizers' materials).
- https://github.com/Jehuty4949/NSL_KDD
- https://qiskit-community.github.io/qiskit-machine-learning/
