from page.base_page import BasePage
import streamlit as st


class TokenSimilarityPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Token Similarity Page'
        st.title(self.title)
        self.t_t_df = self.app_data.token_token_sim_df
        self.token_list = list(self.app_data.token_tags.keys())
        self.token_info = self.app_data.token_info

    def run(self):
        token_src = st.selectbox('token:', self.token_list)
        tags_src = self.app_data.tags_from_token_identifier(token_src)
        st.write('tags: '+', '.join(tags_src))

        show_df = self.t_t_df[self.t_t_df.token_src == token_src]
        show_df = show_df.sort_values(by='sim')[::-1].iloc[:50]
        show_df = show_df.reset_index().drop(columns=['index', 'token_src'])
        show_df = show_df.rename(columns={'token_tar': 'token'})
        show_df['link'] = show_df.token.apply(self.app_data.token_url_html_from_identifier)
        show_df['tag'] = show_df.token.apply(self.app_data.tags_from_token_identifier)
        show_df['tag common'] = show_df.tag.apply(lambda x: [t for t in x if t in tags_src])
        show_df['tag own'] = show_df.tag.apply(lambda x: [t for t in x if t not in tags_src])
        show_df = show_df.drop(columns=['tag'])
        # st.dataframe(show_df)
        st.write(show_df.to_html(escape=False, index=False), unsafe_allow_html=True)
