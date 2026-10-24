# QuantumShield ⚛️

**Quantum Kernel-Based Network Intrusion Detection**  
Interstate Quantum Hackathon for Beginners · Fall 2026 · Quantum Machine Learning (QML) track

## Research question

How do quantum feature-map design, entanglement, and circuit depth affect binary network-intrusion classification, compared with a classical radial-basis-function (RBF) support vector machine?

This is a **research demonstration using a classical quantum-state simulator**, not a deployed intrusion detection system or a demonstration of quantum computational speedup.

## Dataset and preprocessing

We use a small, class-balanced sample from the [NSL-KDD dataset mirror](https://github.com/Jehuty4949/NSL_KDD):

- **Training:** 160 records (80 benign, 80 attacks), sampled from `KDDTrain+_20Percent.txt`.
- **Testing:** 200 records (100 benign, 100 attacks), sampled from the separate `KDDTest+.txt` file.
- **Features:** `src_bytes`, `dst_bytes`, `count`, and `srv_serror_rate` (4 numerical inputs for 4 qubits).
- **Seed:** `42` (`SEED` in the notebook); the test sampling uses `SEED + 1`.
- **Preprocessing:** logarithmic transform of the three byte/count features, then MinMax scaling to `[0, π]`. Scaling is fitted on training data only, including separately within cross-validation folds.

The label `normal` means benign; other NSL-KDD labels are mapped to attack. All experiments replay historical labeled data; they do not capture live network traffic.

## Models and methods

1. **Classical RBF SVM:** classical non-linear reference model; cross-validation selects `C` and `gamma`.
2. **Quantum Z QSVC:** a 4-qubit, non-entangling Z feature map and a quantum-fidelity kernel; cross-validation selects bandwidth `λ` and SVM penalty `C`.
3. **Quantum ZZ QSVC:** a 4-qubit entangling ZZ feature map and a quantum-fidelity kernel; cross-validation independently selects bandwidth `λ` and penalty `C`.

The QSVC classifiers use Qiskit's `FidelityStatevectorKernel`, with quantum-state overlaps computed on a **classical statevector simulator**. The similarity matrices feed standard SVM classifiers. Training-only, three-fold cross-validation is used for hyperparameter selection.

## Independently tuned experimental results

These are the **exploratory held-out test results** from the current notebook configuration (`TRAIN_PER_CLASS=80`, `TEST_PER_CLASS=100`, `REPS=2`), after independent parameter tuning:

| Model | Accuracy | Attack recall | Attack F1 | False positives | Missed attacks |
|---|---:|---:|---:|---:|---:|
| Classical RBF SVM | **80.5%** | **65%** | **76.9%** | 4 | **35** |
| Quantum ZZ QSVC | 76.0% | 57% | 70.4% | 5 | 43 |
| Quantum Z QSVC | 78.0% | 58% | 72.5% | **2** | 42 |

The classical SVM performed best on accuracy and attack recall in this independently tuned configuration; the quantum Z model had the fewest false positives. These results are **not** evidence of a quantum computational advantage.

Earlier exploratory experiments varied training/test sample counts and feature-map repetitions. Some of those experiments favored a quantum classifier, but **their results should not be treated as directly equivalent to this independently tuned run** because the model-selection procedures differed. See `experiment_archives/` when included in the repository.

### Visualizations

The notebook generates model comparisons, confusion matrices, quantum kernel heatmaps, within/between-class similarity analyses, and examples where classical and quantum classifications disagree.

![Model performance](results/model_comparison.png)

![Quantum kernel comparison](results/kernel_comparison.png)

## Run locally on Ubuntu or macOS

Requirements: Python 3.10+ with `venv`, a browser, and an internet connection on the first run to obtain the NSL-KDD files.

```bash
git clone https://github.com/HerrickVasck/QuantumShield.git
cd QuantumShield
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt jupyterlab
jupyter lab
```

Open `QuantumShield.ipynb`, select the Python kernel for `.venv`, and choose **Run → Run All Cells**. The notebook's first cell also includes dependency installation to satisfy the hackathon's self-contained-notebook requirement. Downloaded data are cached under `data/`; generated outputs appear under `results/`.

To repeat an earlier experiment, change `TRAIN_PER_CLASS`, `TEST_PER_CLASS`, and/or `REPS` in the settings cell, **archive the current results first**, then restart the kernel and rerun all cells.

## Files

- `QuantumShield.ipynb` — primary, runnable quantum/classical comparison and analysis.
- `PROJECT_REPORT.md` — hackathon report (methods, results, interpretation, limitations, team details).
- `requirements.txt` — Python dependencies.
- `results/` — generated CSV tables, charts, and experiment configuration (after running the notebook).
- `experiment_archives/` — saved earlier exploratory experiments, if committed.
- `classical_baselines.py` — teammate's additional classical analysis, **once merged into the repository**.

## Limitations

- NSL-KDD is a legacy benchmark. This small, balanced sample is not representative of current enterprise network traffic or normal attack prevalence.
- Only four out of the dataset's many features are used, which limits the information available to any classifier.
- Several experimental configurations were examined on the same test subset, so these are **exploratory** comparisons rather than a fresh, untouched estimate of generalization performance.
- A 4-qubit statevector simulation on a classical computer does not establish quantum hardware speedup or practical advantage.
- Reported `fit_seconds` do not include all hyperparameter-search and prediction costs; they should not be interpreted as end-to-end algorithm runtimes.

## Attribution

Inspired by the hackathon organizers' `QML_1_Lecture.ipynb` quantum-kernel training module. Dataset files are from the public NSL-KDD benchmark, accessed via [Jehuty4949/NSL_KDD](https://github.com/Jehuty4949/NSL_KDD). Implemented with [Qiskit Machine Learning](https://qiskit-community.github.io/qiskit-machine-learning/) and scikit-learn.
