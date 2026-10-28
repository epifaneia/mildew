# Mildew · Cherry leaf classifier, rescued

*Léelo en [español](README.es.md).*

A convolutional network that tells healthy cherry leaves from leaves with powdery mildew, three notebooks that take it from the raw download to the test-set evaluation, and a Streamlit app to try it with your own images.

It was my Code Institute Predictive Analytics project, in April 2024. In October 2026 I rescued it: the app was no longer deployed, the dependencies no longer installed, and the training notebook had no saved outputs, so nothing in the repository proved its accuracy. Rescuing it, I found two ways the old test set could leak into training. This version closes both and measures again.

[What the rescue found](#what-the-rescue-found) · [Measured](#measured) · [The notebooks](#the-notebooks) · [Try it](#try-it) · [Limitations](#limitations)

---

## What the rescue found

**1. The dataset repeats itself.** The Kaggle download has 5,779 images, but 1,393 of them are byte-for-byte copies of another (704 healthy, 689 mildew), apparently spread across the dataset's own `train/` and `test/` folders. Unique images: 2,282 healthy and 2,104 with mildew. In 2024 they all went into the split, so the same image could be in training and in test.

**2. The synthetic images were made before the split.** To balance the classes, the 2024 notebook generated mirrored, rotated or brightened copies of mildew leaves, and only then split everything into train, validation and test. A copy could land in test while its original was in training.

**The fix, in that order:** drop exact duplicates, split 70/10/20 per class with a fixed seed, and only then balance the **training** set with synthetic images. Validation and test hold only original images, in their natural proportions.

## Measured

| | |
|---|---|
| Test set | 879 original images (457 healthy, 422 mildew), never seen in training in any form |
| Accuracy on test | **879 / 879 (100%)**, 0 errors |
| Test images with a near-identical twin in training | 1 of 879 (64-bit difference hash, ≤ 2 bits) |
| Training | 3,194 images (1,597 per class, 125 of them synthetic) · 15 epochs · about 2 minutes on a laptop CPU |
| 2024 figure, for reference | 99.83%, measured with both leaks above and not reproducible from the repository |

A perfect score is a reason for suspicion before it is a reason for pride, so notebook 03 checks it: exact duplicates are already gone, and near duplicates (the same photo recompressed or slightly changed) are practically absent. The score is not leakage. **This dataset is easy**: one leaf per photo, a plain background, even light. The learning curves show the validation loss rising slightly after epoch 8, a mild overfit that 15 epochs keep for comparison with 2024.

Every figure in this table comes from `outputs/metrics.json`, which notebook 03 writes; the app's results page reads the same file.

## The notebooks

The core of the project, and what to read first. Each one opens with its objective, explains every step before the code, and is saved **with its outputs**: you can read the whole process on GitHub without running anything.

| Notebook | What it does | What you see in it |
|---|---|---|
| [01 · Data download](notebooks/01_Kaggle_Data_Download.ipynb) | Downloads the dataset from Kaggle with your own API token | The images per folder, as published |
| [02 · Data preparation](notebooks/02_Data_preparation.ipynb) | Drops duplicates, splits with a seed, balances only training, resizes to 50×50 | Duplicates found, the three sets, sample leaves |
| [03 · CNN](notebooks/03_CNN.ipynb) | Trains, evaluates once on test, checks near duplicates, saves the model and the metrics | Training log, learning curves, classification report, confusion matrix |

The raw download is never modified: notebook 02 writes to `inputs/prepared/` and can be run again.

## Try it

```bash
python -m venv .venv && .venv\Scripts\activate          # on Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/app.py
```

The trained model is in the repository (`outputs/cherry_leaf_cnn.keras`), so the app works without retraining. *Model Interaction* takes JPG or PNG images, several at once or in a ZIP.

To repeat the whole process, from download to evaluation:

```bash
pip install -r requirements-notebooks.txt
jupyter notebook notebooks/
```

Notebook 01 needs a Kaggle API token in `~/.kaggle/kaggle.json` (kaggle.com → Settings → API → *Create New Token*). The token never goes into the repository.

## Limitations

- **One easy dataset.** Single leaves on a plain background. How the model does with photos taken in a plantation, with several leaves, shadows and soil, is unmeasured, and it is the first thing that would need new data.
- **50×50 pixels**, kept from 2024 so the result can be compared. Early mildew spots may be smaller than one pixel at that size.
- **One run, one seed.** No cross-validation and no confidence interval: with 0 errors in 879, the honest statement is "fewer than about 1 in 300 errors on this kind of image", not "100%".
- **Dataset licence:** not stated on its [Kaggle page](https://www.kaggle.com/datasets/ahmadhabibhasanzein/cherry-leaves) (checked October 2026). The images are not redistributed here; the notebooks download them.
- The app is a demo, not a tool for decisions in a real plantation.

---

## Structure

```
notebooks/     01 download · 02 preparation · 03 CNN (saved with outputs)
app/           Streamlit app: app.py and app_pages/ (one module per page)
outputs/       cherry_leaf_cnn.keras · metrics.json · figures/ (written by notebook 03)
inputs/        the dataset, downloaded by notebook 01 (outside git)
```

Built with TensorFlow/Keras 3, scikit-learn, Pillow and Streamlit, on Python 3.13.

Daniel Martín · [epifaneia.dev](https://epifaneia.dev) · Apache-2.0
