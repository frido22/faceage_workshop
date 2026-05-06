from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import h5py
import tensorflow as tf


class ScaleSum(tf.keras.layers.Layer):
    """Replacement for the legacy FaceNet Lambda scale-sum layers."""

    def __init__(self, scale: float = 1.0, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.scale = scale

    def call(self, inputs: list[tf.Tensor]) -> tf.Tensor:
        return inputs[0] + inputs[1] * self.scale

    def get_config(self) -> dict[str, Any]:
        config = super().get_config()
        config["scale"] = self.scale
        return config


def load_faceage_model(model_path: str | Path) -> tf.keras.Model:
    """Load the legacy FaceAge H5 model without deserializing old Lambda bytecode."""

    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model_config = _read_model_config(model_path)
    _replace_legacy_lambdas(model_config)

    model = tf.keras.models.model_from_json(
        json.dumps(model_config),
        custom_objects={"ScaleSum": ScaleSum},
    )
    model.load_weights(str(model_path))
    return model


def _read_model_config(model_path: Path) -> dict[str, Any]:
    with h5py.File(model_path, "r") as h5_file:
        raw_config = h5_file.attrs.get("model_config")

    if raw_config is None:
        raise ValueError(f"No Keras model_config found in {model_path}")

    if isinstance(raw_config, bytes):
        raw_config = raw_config.decode("utf-8")

    return json.loads(raw_config)


def _replace_legacy_lambdas(node: Any) -> None:
    if isinstance(node, dict):
        if node.get("class_name") == "Lambda":
            config = node.get("config", {})
            arguments = config.get("arguments", {})
            node["class_name"] = "ScaleSum"
            node["config"] = {
                "name": config.get("name"),
                "trainable": config.get("trainable", True),
                "dtype": config.get("dtype", "float32"),
                "scale": float(arguments.get("scale", 1.0)),
            }

        for value in node.values():
            _replace_legacy_lambdas(value)

    elif isinstance(node, list):
        for value in node:
            _replace_legacy_lambdas(value)
