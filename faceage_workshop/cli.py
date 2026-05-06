from __future__ import annotations

import argparse
import os

from faceage_workshop.predict import predict_folder


def main() -> None:
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

    parser = argparse.ArgumentParser(description="Run FaceAge on a folder of cropped, aligned face images.")
    parser.add_argument("--input", required=True, help="Folder containing .jpg, .jpeg, or .png images.")
    parser.add_argument("--model", default="models/faceage_model.h5", help="Path to faceage_model.h5.")
    parser.add_argument("--output", default="outputs/results.csv", help="Output CSV path.")
    args = parser.parse_args()

    result = predict_folder(args.input, args.model, args.output)
    print("")
    print(f"Saved {len(result)} predictions to {args.output}")
