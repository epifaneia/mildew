import streamlit as st

from app_pages.paths import BANNER


def display_page():
    st.title("Cherry Leaves Mildew Detection App")

    st.write("### Quick Project Overview")

    st.info(
        f"**General Information**\n"
        f"* Mildew in cherry leaves is a common fungal infection.\n"
        f"* It affects health and yield of cherry plantations.\n"
        f"* Early detection and treatment are crucial.\n"
        f"* They prevent disease spread and ensure quality harvest.\n"
        f"**Project Dataset**\n"
        f"* This app uses image processing for mildew identification.\n"
        f"* It identifies mildew presence in cherry leaves.\n\n"
        f"* Dataset includes high-resolution images of cherry leaves.\n"
        f"* Images are categorised into healthy and mildew-infected leaves.\n"
        f"* Each image is labelled by the folder it comes in: healthy or powdery_mildew.")

    st.write(
        f"* For more information and to understand the dataset better, "
        f"please read the Readme file.")

    st.success(
        f"The project focuses on 2 primary objectives:\n"
        f"* 1 - Study to differentiate healthy and infected leaves.\n"
        f"* 2 - Develop a model to predict mildew presence.")

    # Insert an interactive or static image related to the project
    st.image(str(BANNER),
             caption="Healthy vs Mildew Infected Cherry Leaves")
