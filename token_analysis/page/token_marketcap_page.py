import streamlit as st
from plotly import express as px

from app_data import AppData
from app_util import show_fig
from page.base_page import BasePage


class TokenMarketCapPage(BasePage):
    def __init__(self, app_data):
        super().__init__(app_data)
        self.title = 'Token market cap'
        st.title(self.title)

    def run(self):
        self.plot_coins()

    def plot_coins(self):
        data_df = self.app_data.data_df
        tag_coins = self.app_data.tag_coins

        highlight_tags = st.multiselect('highlight coins by tag:', tag_coins.keys())
        y_selected = 'market_cap'

        df_show = data_df
        if y_selected == 'market_cap':
            df_show = df_show[df_show[y_selected] > 1]
            st.markdown('market cap of all data available tokens :{:.3} trillion dollar'.format(df_show[y_selected].sum() / 10.0 ** 12))
        df_show = df_show.sort_values(by=y_selected)[::-1]

        top_n = st.slider('top n coins:', 0, df_show.shape[0], 300, 1)
        top_n = int(top_n)
        df_show = df_show[:top_n]

        log_scale = st.checkbox('display in log scale', value=True)
        fig_el = st.empty()

        def highlight_coin(tags):
            if set(tags).intersection(set(highlight_tags)):
                return 'red'
            else:
                return 'blue'
        df_show['color'] = df_show.tags.apply(highlight_coin)

        df_filtered = df_show[df_show.color == 'red']
        for i, v in df_filtered.iterrows():
            # st.markdown('{}: {}'.format(v['name'], v['tags']))
            st.markdown('[{}](https://coinmarketcap.com/ja/currencies/{}/)'.format(v['name'], v['slug']))
            # st.write(v.to_dict())

        fig = px.bar(df_show, x='name', y=y_selected, color='color', log_y=log_scale,
                     color_discrete_sequence=df_show.color.unique(),
                     range_y=[0.1, 1.1*data_df[y_selected].max()])
        show_fig(fig, fig_el)
