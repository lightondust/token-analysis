from plotly import express as px

from app_data import AppData
from app_util import show_fig
from page.base_page import BasePage
import streamlit as st


class TagStatisticsPage(BasePage):
    def __init__(self, app_data):
        super().__init__(app_data)
        self.title = 'Tag statistics'
        st.title(self.title)

    def run(self):
        self.plot_tag_stats()

    def plot_tag_stats(self):
        tag_tokens = self.app_data.tag_tokens
        token_tags = self.app_data.token_tags
        tag_info_df = self.app_data.tag_info_df

        graph_type = st.selectbox('graph type', ['bar', 'scatter'])
        log_scale = st.checkbox('log scale', value=True)
        y_selected = st.selectbox('y:', ['count', 'market_cap'])
        tag_type = st.selectbox('tag group:', ['all', 'ecosystem'])
        highlight_tags = st.multiselect('highlight tags:', tag_tokens.keys())
        high_light_tags_of_tokens = st.multiselect('highlight tags:', token_tags.keys())
        for c in high_light_tags_of_tokens:
            highlight_tags += token_tags[c]
        highlight_tags = list(set(highlight_tags))

        df_show = tag_info_df.copy().sort_values(by=y_selected)[::-1]
        if tag_type != 'all':
            df_show = df_show[df_show.tag_type == tag_type]

        def high_light(tag):
            if tag in highlight_tags:
                return tag
            else:
                return ''
        df_show['color'] = df_show.tag.apply(high_light)

        range_y=[0.1, 1.1*tag_info_df[y_selected].max()]

        if graph_type == 'bar':
            fig = px.bar(df_show, y=y_selected, x='tag', hover_data=['tag'], color='color', log_y=log_scale, range_y=range_y)
        else:
            fig = px.scatter(df_show, y=y_selected, x='tag', hover_data=['tag'], color='color', log_y=log_scale, range_y=range_y)

        show_fig(fig)
