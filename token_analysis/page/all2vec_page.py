import numpy as np
import pandas as pd

from app_data import AppData
from page.base_page import BasePage
import streamlit as st


class All2VecPage(BasePage):
    title = 'All2vec Page'

    def __init__(self, app_data: AppData, **kwargs):
        super().__init__(app_data, **kwargs)
        self.no_to_show = 100

    def run(self):
        st.title(All2VecPage.title)
        tag_tokens = self.app_data.tag_tokens
        token_tags= self.app_data.token_tags
        model = self.app_data.all2vec_model

        term_select = st.selectbox('tag', list(tag_tokens.keys()) + list(token_tags.keys()))
        st.markdown('#### ' + term_select)
        term_sim = model.wv.most_similar(term_select, topn=len(model.wv.index_to_key))
        term_sim = [list(t) for t in term_sim]
        for term_info in term_sim:
            adjs = tag_tokens.get(term_info[0], [])
            if len(adjs) == 0:
                adjs = token_tags.get(term_info[0], [])
            term_info.append(len(adjs))
        term_sim_df = pd.DataFrame(term_sim, columns=['term', 'similarity', 'adjs'])
        term_sim_df['score'] = term_sim_df.similarity * np.log(term_sim_df.adjs + 1.)
        tag_sim_df = term_sim_df.sort_values('score')[::-1][:self.no_to_show]
        st.dataframe(tag_sim_df, height=500)
