import json

import streamlit as st

from app_pages.paths import FIGURES, METRICS


def display_page():
    st.title("Results and Conclusions")
    st.write("Every figure on this page is read from `outputs/metrics.json`, "
             "written by notebook 03 when it evaluates the model on the test set.")

    if not METRICS.exists():
        st.warning("No metrics yet: run notebook 03 to train and evaluate the model.")
        return
    m = json.loads(METRICS.read_text(encoding="utf-8"))

    st.info(
        "**Model Evaluation (test set, never seen during training)**\n"
        f"* Accuracy: {m['test_accuracy']:.2%} on {m['test_images']} images.\n"
        f"* Errors: {m['test_errors']} of {m['test_images']}.\n"
        f"* Split: {m['split']}, seed {m['seed']}; the training set was balanced "
        "after the split, so no synthetic copy of a test image was seen in training.\n"
        f"* Exact duplicates in the download were dropped before the split; test images with a "
        f"near-identical twin in training: {m['test_near_duplicates_in_train']}."
    )

    for name, caption in (("learning_curves.png", "Learning curves"),
                          ("confusion_matrix.png", "Confusion matrix on the test set")):
        if (FIGURES / name).exists():
            st.image(str(FIGURES / name), caption=caption)

    st.info(
        "**Hypothesis Validation**\n"
        "* Initial Hypothesis: Visible differences between healthy and mildew-infected "
        "cherry leaves can be detected by a CNN.\n"
        "* The test accuracy above supports it, within the limits of this dataset: "
        "photographs of single leaves on a plain background, at 50x50 pixels."
    )
