from page.base_page import BasePage
import streamlit as st


class TemplatePage(BasePage):
    def __init__(self, app_data):
        super().__init__(app_data)
        self.title = 'Template Page'
        st.title(self.title)

    def run(self):
        pass
