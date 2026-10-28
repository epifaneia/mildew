"""Paths relative to the repository root, so the app runs from any working directory."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "outputs" / "cherry_leaf_cnn.keras"
METRICS = ROOT / "outputs" / "metrics.json"
FIGURES = ROOT / "outputs" / "figures"
BANNER = ROOT / "app" / "src" / "leaves.png"
