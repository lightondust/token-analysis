from page.base_page import BasePage
import streamlit as st


class TokenSimilarityPage(BasePage):
    def __init__(self, app_data):
        super().__init__(app_data)
        self.title = 'Token Similarity Page'
        st.title(self.title)

    def run(self):
        t_t_df = self.app_data.token_token_sim_df
        token_src = st.selectbox('token:', list(self.app_data.token_tags.keys()))
        show_df = t_t_df[t_t_df.token_src == token_src]
        show_df = show_df.sort_values(by='sim')[::-1]
        show_df = show_df.reset_index().drop(columns=['index'])
        st.dataframe(show_df)
