from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from faceage_workshop.legacy_model import load_faceage_model

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
IMAGE_SIZE = (160, 160)


def predict_folder(input_dir: str | Path, model_path: str | Path, output_csv: str | Path) -> pd.DataFrame:
    input_dir = Path(input_dir)
    output_csv = Path(output_csv)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input folder not found: {input_dir}")

    image_paths = sorted(
        path for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not image_paths:
        raise ValueError(f"No .jpg, .jpeg, or .png images found in {input_dir}")

    model = load_faceage_model(model_path)
    rows: list[dict[str, float | str]] = []

    for index, image_path in enumerate(image_paths, start=1):
        print(f"[{index}/{len(image_paths)}] {image_path.name}")
        image_array = preprocess_image(image_path)
        prediction = model.predict(image_array, verbose=0)
        rows.append({
            "subj_id": image_path.stem,
            "faceage": float(np.squeeze(prediction)),
        })

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    result = pd.DataFrame(rows)
    result.to_csv(output_csv, index=False)
    return result


def preprocess_image(image_path: Path) -> np.ndarray:
    image = Image.open(image_path).convert("RGB").resize(IMAGE_SIZE)
    array = np.asarray(image, dtype=np.float32)

    std = float(array.std())
    if std == 0.0:
        raise ValueError(f"Image has zero pixel variance and cannot be normalized: {image_path}")

    array = (array - float(array.mean())) / std
    return array.reshape((1, IMAGE_SIZE[1], IMAGE_SIZE[0], 3))
