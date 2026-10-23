# QuantumShield ⚛️

**Quantum kernel-based cybersecurity intrusion detection** — Interstate Quantum Hackathon 2026, QML track.

## Research question
Can a 4-qubit entangling ZZ quantum feature map distinguish malicious NSL-KDD traffic better than a non-entangling Z map and a classical RBF SVM on the same small, held-out test subset?

## Run locally (Ubuntu / JupyterLab)

If your `~/school/QuantumHackathon/qml-env` virtual environment is installed already:

```bash
cd ~/school/QuantumHackathon
source qml-env/bin/activate
jupyter lab
```

Open `QuantumShield.ipynb`, select Python 3, and use **Run → Run All Cells**. The first cell installs dependencies. Internet is required for the first run to download NSL-KDD data to `data/`. Figures and metrics are written into `results/`.

If installing from scratch:

```bash
python3 -m venv qml-env
source qml-env/bin/activate
pip install -r requirements.txt jupyterlab
jupyter lab
```

## Methods
- NSL-KDD **official 20% training file** and **independent test file** (mirrored at https://github.com/Jehuty4949/NSL_KDD)
- Four numerical features: `src_bytes`, `dst_bytes`, `count`, `srv_serror_rate`.
- Balanced 80-row training subset and 40-row test subset, with `SEED=42`.
- Training-only preprocessing and cross-validation for bandwidth.
- Classical `SVC(rbf)` versus quantum `QSVC` with Z and ZZ maps.
- Exact statevector fidelity kernel; **simulation, not quantum hardware and not quantum speedup**.

## File contents
- `QuantumShield.ipynb` — executable, self-contained research notebook.
- `PROJECT_REPORT.md` — fill in after experiments.
- `requirements.txt` — dependency list.
- `results/` — automatically generated figures and scores.

## Limitations
Small balanced subsamples are not representative of network deployment. NSL-KDD is a legacy benchmark. This is an educational research comparison rather than a production IDS; no claim of quantum advantage is made. Tests must be interpreted using sample sizes and uncertainty.

## Attribution
Adapted conceptually from the official QML pre-training lecture notebook (`QML_1_Lecture.ipynb`). Data: NSL-KDD public benchmark, files mirrored by [Jehuty4949/NSL_KDD](https://github.com/Jehuty4949/NSL_KDD). Uses Qiskit Machine Learning and scikit-learn.
