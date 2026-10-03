"""Premier entraînement YOLO OBB sur GPU CUDA."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import torch
import yaml
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parent
DATASET = PROJECT_ROOT / "Yolo" / "Playing Cards.v4-yolov8n.yolov8-obb"
RUNS_DIR = PROJECT_ROOT / "runs" / "obb"


def create_runtime_yaml() -> Path:
    """Create a data YAML with absolute paths for the local dataset."""
    source_yaml = DATASET / "data.yaml"
    if not source_yaml.is_file():
        raise FileNotFoundError(f"Dataset YAML introuvable : {source_yaml}")

    with source_yaml.open("r", encoding="utf-8") as stream:
        source: dict[str, Any] = yaml.safe_load(stream)

    names = source.get("names")
    if not names:
        raise ValueError(f"Aucun nom de classe dans {source_yaml}")

    for split in ("train", "valid", "test"):
        images = DATASET / split / "images"
        if not images.is_dir():
            raise FileNotFoundError(f"Dossier introuvable : {images}")

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    runtime_yaml = RUNS_DIR / "data_runtime.yaml"
    data = {
        "path": str(DATASET.resolve()),
        "train": "train/images",
        "val": "valid/images",
        "test": "test/images",
        "names": names,
    }
    with runtime_yaml.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(data, stream, sort_keys=False, allow_unicode=False)
    return runtime_yaml


def require_cuda() -> None:
    """Stop immediately if this Python environment cannot use the GPU."""
    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA indisponible. Votre PyTorch est probablement une version CPU-only "
            "(par exemple torch ...+cpu). Installez une version PyTorch CUDA dans "
            "le .venv, puis relancez ce script."
        )

    print(f"GPU : {torch.cuda.get_device_name(0)}")
    print(f"CUDA : {torch.version.cuda}")


def main() -> None:
    require_cuda()
    data_yaml = create_runtime_yaml()

    model = YOLO("yolov8n-obb.pt")
    model.train(
        data=str(data_yaml),
        device=0,
        epochs=10,
        imgsz=640,
        batch=8,
        workers=2,
        cache=False,
        project=str(RUNS_DIR),
        name="first-gpu-test",
        pretrained=True,
        patience=5,
        amp=True,
        exist_ok=True,
        plots=True,
        val=True,
    )


if __name__ == "__main__":
    main()
