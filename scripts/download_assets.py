from __future__ import annotations

import argparse
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath


DEFAULT_URL = (
    "https://www.dropbox.com/scl/fo/8umk60sre50kuenh4h6ui/AHFEM6nrvI4JlxKWyA7UXDg"
    "?rlkey=32tydco1iednsuw0rlkpcu53u&st=otll826s&dl=1"
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download workshop model weights and synthetic test images.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Dropbox shared-folder download URL.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    model_path = Path("models/faceage_model.h5")
    data_path = Path("data/synthetic_dataset_cropped_aligned")

    if model_path.exists() and data_path.exists() and not args.force:
        print("Assets already exist. Use --force to download again.")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        zip_path = tmpdir_path / "faceage_assets.zip"
        extracted_path = tmpdir_path / "extracted"

        print(f"Downloading assets to {zip_path} ...")
        urllib.request.urlretrieve(args.url, zip_path)

        print("Extracting assets ...")
        extracted_path.mkdir(parents=True, exist_ok=True)
        safe_extract(zip_path, extracted_path)

        source_model = extracted_path / "faceage_model.h5"
        source_data = extracted_path / "synthetic_dataset_cropped_aligned"

        if not source_model.exists():
            raise FileNotFoundError("Downloaded archive did not contain faceage_model.h5")
        if not source_data.exists():
            raise FileNotFoundError("Downloaded archive did not contain synthetic_dataset_cropped_aligned/")

        model_path.parent.mkdir(parents=True, exist_ok=True)
        data_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source_model, model_path)
        if data_path.exists():
            shutil.rmtree(data_path)
        shutil.copytree(source_data, data_path)

    print(f"Model: {model_path}")
    print(f"Images: {data_path}")


def safe_extract(zip_path: Path, destination: Path) -> None:
    destination = destination.resolve()

    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            member_path = PurePosixPath(member.filename)
            if member.filename in {"", "/"} or member_path.is_absolute() or ".." in member_path.parts:
                continue

            target_path = (destination / Path(*member_path.parts)).resolve()
            if destination not in target_path.parents and target_path != destination:
                raise ValueError(f"Unsafe zip member path: {member.filename}")

            if member.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
                continue

            target_path.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, target_path.open("wb") as target:
                shutil.copyfileobj(source, target)


if __name__ == "__main__":
    main()
