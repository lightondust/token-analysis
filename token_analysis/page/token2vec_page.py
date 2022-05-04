import numpy as np
import pandas as pd

from app_data import AppData
from page.base_page import BasePage
import streamlit as st


class Token2VecPage(BasePage):
    def __init__(self, app_data: AppData):
        super().__init__(app_data)
        self.title = 'token2vec'
        st.title(self.title)

    def run(self):
        token_tags = self.app_data.token_tags
        model = self.app_data.token2vec_model

        tag_select = st.selectbox('tag', list(token_tags.keys()))
        token_sim = model.wv.most_similar(tag_select, topn=100)
        token_sim = [list(t) for t in token_sim]
        for token_info in token_sim:
            tgs = token_tags.get(token_info[0], [])
            token_info.append(len(tgs))
        token_sim_df = pd.DataFrame(token_sim, columns=['token', 'similarity', 'tags_in_token'])
        token_sim_df['score'] = token_sim_df.similarity * np.log(token_sim_df.tags_in_token)
        token_sim_df = token_sim_df.sort_values('score')[::-1]
        token_sim_df['link'] = token_sim_df.token.apply(self.app_data.token_url_html_from_identifier)
        # st.dataframe(token_sim_df, height=500)
        st.write(token_sim_df.to_html(escape=False, index=False), unsafe_allow_html=True)
