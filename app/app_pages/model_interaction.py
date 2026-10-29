import io
import zipfile

import numpy as np
import streamlit as st
from PIL import Image

from app_pages.paths import MODEL

IMAGE_SIZE = (50, 50)
IMAGE_TYPES = (".jpg", ".jpeg", ".png")


@st.cache_resource
def load_model():
    # Imported here so the other pages open without waiting for TensorFlow
    import keras
    return keras.models.load_model(MODEL)


def display_page():
    st.title("Model Interaction")
    st.write("""
    Upload images of cherry leaves, one by one, several at once or as a ZIP file,
    and the model says whether each leaf looks healthy or has powdery mildew.

    _Educational demo: not meant for decisions in a real plantation._
    """)

    st.warning(
        "**Only single detached leaves on a plain background, like the dataset's.** "
        "The model has no check for images unlike the ones it was trained on: it always "
        "answers healthy or mildew, whatever it is shown. A plain white image, with no "
        "leaf at all, gets a probability of mildew of 0.69. For a photo taken in a "
        "plantation, or of anything else, the answer means nothing.")

    uploaded_files = st.file_uploader(
        "Drag and drop or click to upload cherry leaf images or a ZIP file",
        type=["jpg", "jpeg", "png", "zip"], accept_multiple_files=True)

    if not uploaded_files:
        st.write("Upload JPG or PNG images, or a ZIP file with them.")
        return

    model = load_model()
    for uploaded_file in uploaded_files:
        if uploaded_file.name.lower().endswith(".zip"):
            # Process images inside a ZIP file
            with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                for file_name in zip_ref.namelist():
                    if file_name.lower().endswith(IMAGE_TYPES):
                        process_and_display_image(model, file_name, zip_ref.read(file_name))
        else:
            process_and_display_image(model, uploaded_file.name, uploaded_file.getvalue())


def process_and_display_image(model, name, image_data):
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    st.image(image, caption=name, width=200)
    # The model was trained on 50x50 images with pixel values in [0, 255]:
    # the rescaling to [0, 1] is a layer inside the model
    batch = np.expand_dims(np.asarray(image.resize(IMAGE_SIZE), dtype="float32"), axis=0)
    probability = float(model.predict(batch, verbose=0)[0][0])
    label = "Powdery mildew" if probability >= 0.5 else "Healthy"
    st.write(f"Prediction: **{label}** (probability of mildew {probability:.2f})")
