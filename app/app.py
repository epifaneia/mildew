import streamlit as st
from app_pages.multipage import MultiPage
# Import page modules from the app_pages folder
from app_pages import home_page
from app_pages import project_introduction
from app_pages import model_interaction
from app_pages import results_conclusions

# Set the Streamlit page configuration with title and icon
st.set_page_config(
    page_title="Cherry Leaves Mildew Detection App", page_icon="🌿")

# Create an instance of the MultiPage class
app = MultiPage("Cherry Leaves Mildew Detection App")

# Add pages to the multi-page app
# Each page is defined in its own module within the app_pages folder
app.add_page("Home", home_page.display_page)
app.add_page("Project Introduction", project_introduction.display_page)
app.add_page("Model Interaction", model_interaction.display_page)
app.add_page("Results and Conclusions", results_conclusions.display_page)

# Execute the app
# This is the main block to run the Streamlit app
if __name__ == "__main__":
    app.run()
