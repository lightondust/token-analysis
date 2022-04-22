from plotly import express as px

from app_util import show_fig
from page.base_page import BasePage
import streamlit as st


class TagMembersPage(BasePage):
    def __init__(self, app_data):
        super().__init__(app_data)
        self.title = 'Tag Members'
        st.title(self.title)

    def run(self):
        self.plot_tag_members()

    def plot_tag_members(self):
        tag_coins = self.app_data.tag_coins
        data_df = self.app_data.data_df

        tag_selected = st.selectbox('tag', tag_coins.keys())
        log_scale = st.checkbox('log scale', value=True)
        y_selected = 'market_cap'

        c_s = tag_coins[tag_selected]
        c_s_id = [int(c.split('_')[0]) for c in c_s]
        df_show = data_df[data_df.id.isin(c_s_id)]
        fig = px.bar(df_show, y=y_selected, x='name', log_y=log_scale, range_y=[0.1, 1.1 * data_df[y_selected].max()])
        show_fig(fig)
