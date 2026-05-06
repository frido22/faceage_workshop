# FaceAge Workshop

Simple demo for running FaceAge on a small folder of cropped, aligned face images.

This is for workshop and research demonstration only. Do not use it for clinical
care, diagnosis, or treatment decisions. Do not upload patient images to GitHub,
Dropbox, Colab, Slack, or email unless your institution has approved that workflow.

## 1. Install uv

If you do not already have `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal after installation.

## 2. Set up the repo

```bash
git clone https://github.com/frido22/faceage_workshop.git
cd faceage_workshop
uv sync
```

## 3. Download the workshop assets

This downloads the model weights and synthetic test images into `models/` and `data/`.

```bash
uv run python scripts/download_assets.py
```

(Optional manual download:
https://www.dropbox.com/scl/fo/8umk60sre50kuenh4h6ui/AHFEM6nrvI4JlxKWyA7UXDg?rlkey=32tydco1iednsuw0rlkpcu53u&st=otll826s&dl=0)

## 4. Run the demo dataset

```bash
uv run python run_faceage.py
```

Open the result:

```bash
open outputs/faceage_results.csv
```

The CSV has one row per image:

```text
subj_id,faceage
example_image,72.3
```

## 5. Run your own images

Replace the test images in `data/input_images/` with your own cropped, aligned
face images. Use study IDs in filenames, not names, MRNs, dates of birth, or
other identifiers.

```bash
uv run python run_faceage.py
```

## Input Requirements

- Images should be `.jpg`, `.jpeg`, or `.png`.
- Each image should contain one cropped, aligned face.
- The model input is resized to `160 x 160`.
- Pixel values are normalized per image before prediction.

This minimal workshop repo does not do face detection. If your images are raw
clinical photographs, crop and align faces before running this demo.

## Credit

FaceAge was developed by AIM-Harvard. Please cite the original project and paper
if you use this code or model:

- GitHub: https://github.com/AIM-Harvard/FaceAge
- Paper: Bontempi et al., "FaceAge, a deep learning system to estimate biological
  age from face photographs to improve prognostication", The Lancet Digital Health.
