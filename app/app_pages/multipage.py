import streamlit as st


class MultiPage:
    """
    Class for multi-page Streamlit apps using object-oriented design.
    """

    def __init__(self, app_name) -> None:
        self.pages = []
        self.app_name = app_name
        if "current_page" not in st.session_state:
            st.session_state.current_page = 0

    def add_page(self, title, func) -> None:
        """
        Add a new page to the app.
        :param title: Title of the page.
        :param func: Python function to render this page in Streamlit.
        """
        self.pages.append({"title": title, "function": func})

    def run(self):
        # Each page writes its own title
        page_index = st.sidebar.radio(
            'Navigation', range(len(self.pages)),
            format_func=lambda index: self.pages[index]['title'])
        st.session_state.current_page = page_index
        self.pages[st.session_state.current_page]['function']()
