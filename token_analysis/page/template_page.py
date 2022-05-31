from page.base_page import BasePage
import streamlit as st
import pandas as pd


class TemplatePage(BasePage):
    title = 'Template Page'

    def __init__(self, app_data, **kwargs):
        super().__init__(app_data, **kwargs)

    def run(self):
        st.title(TemplatePage.title)
        df = pd.DataFrame([f'<a target="_blank" href="https://coinmarketcap.com/ja/currencies/ethereum/">text</a>'])
        st.write(df.to_html(escape=False), unsafe_allow_html=True)
