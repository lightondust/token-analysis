import numpy as np
import pandas as pd

from app_data import AppData
from page.base_page import BasePage
import streamlit as st


class Tag2VecPage(BasePage):
    def __init__(self, app_data: AppData, **kwargs):
        super().__init__(app_data, **kwargs)
        self.title = 'Template Page'
        st.title(self.title)

    def run(self):
        self.tag2vec()

    def tag2vec(self):
        tag_tokens = self.app_data.tag_tokens
        model = self.app_data.tag2vec_model

        tag_select = st.selectbox('tag', list(tag_tokens.keys()))
        tag_sim = model.wv.most_similar(tag_select, topn=100)
        tag_sim = [list(t) for t in tag_sim]
        for tag_info in tag_sim:
            tks = tag_tokens.get(tag_info[0], [])
            tag_info.append(len(tks))
        tag_sim_df = pd.DataFrame(tag_sim, columns=['tag', 'similarity', 'tokens_in_tag'])
        tag_sim_df['score'] = tag_sim_df.similarity * np.log(tag_sim_df.tokens_in_tag)
        tag_sim_df = tag_sim_df.sort_values('score')[::-1]
        tag_sim_df['link'] = tag_sim_df.tag.apply(self.app_data.tag_url)
        # st.dataframe(tag_sim_df, height=500)
        st.write(tag_sim_df.to_html(escape=False, index=False), unsafe_allow_html=True)
