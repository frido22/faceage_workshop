# FaceAge Workshop Slides

---

## 1. Goal

Run FaceAge on a small image folder and create a CSV with one FaceAge estimate per image.

```text
cropped face images -> FaceAge model -> results.csv
```

---

## 2. What Participants Need

- A laptop with `uv` installed
- This workshop repo
- The workshop model weights and synthetic test dataset
- A folder of cropped, aligned face images if running their own data

Do not place patient data in GitHub, Dropbox, Colab, Slack, or email unless approved by your institution.

---

## 3. Set Up The Environment

```bash
git clone https://github.com/frido22/faceage_workshop.git
cd faceage_workshop
uv sync
```

`uv` creates the Python environment from the repo settings.

---

## 4. Download The Demo Assets

```bash
uv run python scripts/download_assets.py
```

(Manual download link, optional:
https://www.dropbox.com/scl/fo/8umk60sre50kuenh4h6ui/AHFEM6nrvI4JlxKWyA7UXDg?rlkey=32tydco1iednsuw0rlkpcu53u&st=otll826s&dl=0)

This creates:

```text
models/faceage_model.h5
data/input_images/
```

---

## 5. Run FaceAge

```bash
uv run python run_faceage.py
```

The script loads each image, resizes it to `160 x 160`, normalizes it, runs the model, and writes the CSV.

---

## 6. Read The Output

```text
subj_id,faceage
image_001,72.3
image_002,68.1
```

- `subj_id`: image filename without extension
- `faceage`: model estimate

Review failed or low-quality images before using results in any analysis.

---

## 7. Running Local Data

Replace the test images in `data/input_images/` with cropped, aligned images from your own dataset.

```bash
uv run python run_faceage.py
```

Use study IDs in filenames. Do not use names, MRNs, dates of birth, or other identifiers.

---

## 8. Important Limits

- Workshop and research demo only
- Not clinical decision support
- This minimal version expects cropped, aligned faces
- Raw clinical photos need face detection/cropping before this step
