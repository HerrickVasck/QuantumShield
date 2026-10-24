"""Independent reproducible classical benchmarks for QuantumShield.

Matches the quantum notebook's four selected NSL-KDD features, dataset sources,
balanced sampling, seed, and training-only preprocessing. Does not edit the
quantum notebook. Intended to run from the repository root.
"""
from pathlib import Path
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, confusion_matrix,
    f1_score, precision_score, recall_score,
)
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC

SEED = 42
FEATURE_COLUMNS = {"src_bytes": 4, "dst_bytes": 5, "count": 22, "srv_serror_rate": 25}
TRAIN_PER_CLASS = 80
TEST_PER_CLASS = 100
DATA_DIR = Path("data")
RESULTS_DIR = Path("results")
DATA_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)
DATA_URLS = {
    "KDDTrain+_20Percent.txt": "https://raw.githubusercontent.com/Jehuty4949/NSL_KDD/master/KDDTrain%2B_20Percent.txt",
    "KDDTest+.txt": "https://raw.githubusercontent.com/Jehuty4949/NSL_KDD/master/KDDTest%2B.txt",
}


def load_frame(filename):
    path = DATA_DIR / filename
    if not path.exists():
        print(f"Downloading {filename}")
        urlretrieve(DATA_URLS[filename], path)
    raw = pd.read_csv(path, header=None)
    if raw.shape[1] != 43:
        raise ValueError(f"Expected 43 NSL-KDD columns, got {raw.shape[1]} in {filename}")
    features = pd.DataFrame({
        name: pd.to_numeric(raw.iloc[:, col], errors="raise")
        for name, col in FEATURE_COLUMNS.items()
    })
    features["is_attack"] = (raw.iloc[:, 41].astype(str).str.strip() != "normal").astype(int).to_numpy()
    return features.dropna().reset_index(drop=True)


def balanced_subset(df, per_class, seed):
    samples = [df.loc[df.is_attack == label].sample(n=per_class, random_state=seed)
               for label in (0, 1)]
    return pd.concat(samples, ignore_index=True).sample(frac=1, random_state=seed).reset_index(drop=True)


def build_arrays():
    train_df = balanced_subset(load_frame("KDDTrain+_20Percent.txt"), TRAIN_PER_CLASS, SEED)
    test_df = balanced_subset(load_frame("KDDTest+.txt"), TEST_PER_CLASS, SEED + 1)
    names = list(FEATURE_COLUMNS)
    X_train = train_df[names].to_numpy(dtype=float)
    X_test = test_df[names].to_numpy(dtype=float)
    for index in (0, 1, 2):
        X_train[:, index] = np.log1p(np.clip(X_train[:, index], 0, None))
        X_test[:, index] = np.log1p(np.clip(X_test[:, index], 0, None))
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X_train = scaler.fit_transform(X_train)
    X_test = np.clip(scaler.transform(X_test), 0, np.pi)
    return X_train, X_test, train_df.is_attack.to_numpy(), test_df.is_attack.to_numpy()


def main():
    X_train, X_test, y_train, y_test = build_arrays()
    models = {
        "Linear SVM": SVC(kernel="linear", C=1.0),
        "RBF SVM": SVC(kernel="rbf", C=1.0, gamma="scale"),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=SEED),
    }
    rows = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        tn, fp, fn, tp = confusion_matrix(y_test, preds, labels=[0, 1]).ravel()
        rows.append({
            "model": name,
            "accuracy": accuracy_score(y_test, preds),
            "balanced_accuracy": balanced_accuracy_score(y_test, preds),
            "precision_attack": precision_score(y_test, preds, zero_division=0),
            "recall_attack": recall_score(y_test, preds, zero_division=0),
            "f1_attack": f1_score(y_test, preds, zero_division=0),
            "false_positive_rate": fp / (tn + fp),
            "false_negatives": int(fn),
        })
    results = pd.DataFrame(rows)
    print(results.round(3).to_string(index=False))
    results.to_csv(RESULTS_DIR / "classical_baselines.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    indices = np.arange(len(results))
    ax.bar(indices - .18, results["balanced_accuracy"], .36, label="Balanced accuracy")
    ax.bar(indices + .18, results["f1_attack"], .36, label="Attack F1")
    ax.set_xticks(indices, results["model"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Held-out test score (0–1)")
    ax.set_title("Classical intrusion-detection baselines")
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "classical_baselines.png", dpi=170)
    plt.close(fig)
    print("Saved results/classical_baselines.csv and results/classical_baselines.png")
    print("Compare the RBF SVM row with QuantumShield.ipynb's Classical RBF SVM row.")


if __name__ == "__main__":
    main()
