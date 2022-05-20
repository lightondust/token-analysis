from page.base_page import BasePage
import streamlit as st


class TagSimilarityPage(BasePage):
    title = 'Tag similarity'

    def __init__(self, app_data, **kwargs):
        super().__init__(app_data, **kwargs)
        st.title(TagSimilarityPage.title)

    def run(self):
        self.tag_sim()

    def tag_sim(self):
        tag_sim_df, tag_sim_list = self.app_data.tag_tag_sim_df, self.app_data.tag_tag_sim
        tag_tokens = self.app_data.tag_tokens
        tag_list = list(tag_tokens.keys())
        tag_select = st.selectbox('target tags:', tag_list)
        df_show = tag_sim_df[tag_sim_df.tag_src == tag_select]
        df_show = df_show.sort_values(by='weight')[::-1].reset_index().drop('index', axis=1)
        st.table(df_show)
