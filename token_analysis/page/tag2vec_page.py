import numpy as np
import pandas as pd

from app_data import AppData
from page.base_page import BasePage
import streamlit as st


class Tag2VecPage(BasePage):
    def __init__(self, app_data):
        super().__init__(app_data)
        self.title = 'Template Page'
        st.title(self.title)

    def run(self):
        self.tag2vec()

    def tag2vec(self):
        tag_coins = self.app_data.tag_coins
        model = self.app_data.tag2vec_model

        tag_select = st.selectbox('tag', list(tag_coins.keys()))
        tag_sim = model.wv.most_similar(tag_select, topn=100)
        tag_sim = [list(t) for t in tag_sim]
        for tag_info in tag_sim:
            tag_info.append(len(tag_coins[tag_info[0]]))
        tag_sim_df = pd.DataFrame(tag_sim, columns=['tag', 'similarity', 'coins_in_tag'])
        tag_sim_df['score'] = tag_sim_df.similarity * np.log(tag_sim_df.coins_in_tag)
        tag_sim_df = tag_sim_df.sort_values('score')[::-1]
        st.dataframe(tag_sim_df, height=500)
