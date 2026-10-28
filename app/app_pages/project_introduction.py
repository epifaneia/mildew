import streamlit as st


def display_page():
    st.title("Project Introduction")
    st.write("This page outlines the project on cherry leaf mildew detection.")

    st.info(
        "**Project Overview**\n"
        "* Objective: Identify mildew in cherry leaves using a CNN.\n"
        "* Why: Mildew affects cherry crop health and yield.\n"
        "* Approach: Use a CNN for autonomous pattern recognition.\n"
        "* Data: Public dataset of cherry leaf images (Kaggle).\n"
        "* Classification: Healthy vs. Mildew-infected leaves.\n"
        "* Hypothesis: Visible differences to humans should be detectable by CNN."
    )

    st.write(
        "* The full process, from download to evaluation, is in the three "
        "notebooks in the repository's `notebooks/` folder.")
