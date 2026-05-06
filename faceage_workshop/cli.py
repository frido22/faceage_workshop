from __future__ import annotations

import os
from pathlib import Path

from faceage_workshop.predict import predict_folder

INPUT_DIR = Path("data/input_images")
MODEL_PATH = Path("models/faceage_model.h5")
OUTPUT_CSV = Path("outputs/faceage_results.csv")


def main() -> None:
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

    print(f"Input: {INPUT_DIR}")
    print(f"Model: {MODEL_PATH}")
    print(f"Output: {OUTPUT_CSV}")
    print("")

    result = predict_folder(INPUT_DIR, MODEL_PATH, OUTPUT_CSV)
    print("")
    print(f"Saved {len(result)} predictions to {OUTPUT_CSV}")
