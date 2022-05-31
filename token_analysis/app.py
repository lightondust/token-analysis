import streamlit as st

from app_url import AppURL
from page.main_page import MainPage
from page.tag2vec_page import Tag2VecPage
from page.tag_graph_page import TagGraphPage
from page.token_similarity_page import TokenSimilarityPage
from page.token2vec_page import Token2VecPage
from page.all2vec_page import All2VecPage
from page.tag_similarity_page import TagSimilarityPage
from page.tag_statistics_page import TagStatisticsPage
from page.tag_members_page import TagMembersPage
from page.token_marketcap_page import TokenMarketCapPage
from page.template_page import TemplatePage
from app_data import get_app_data
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%m/%d/%Y %X")

st.set_page_config(layout='wide', page_title='token analysis', page_icon='./favico_s_t.png')


@st.cache(allow_output_mutation=True)
def _get_app_data(page_class):
    return get_app_data(page_class)


page_class_list = [
    MainPage,
    TokenMarketCapPage,
    TokenSimilarityPage,
    Token2VecPage,
    All2VecPage,
    TagMembersPage,
    TagSimilarityPage,
    Tag2VecPage,
    TagStatisticsPage,
    TagGraphPage,
    TemplatePage
]
page_class = {p.title: p for p in page_class_list}
page_selected = st.sidebar.radio('page:', list(page_class.keys())+[''], index=len(page_class))

app_data = _get_app_data(page_class)
app_url = AppURL()

page = app_url.sync_variable('page', page_selected, MainPage.title)

page_obj = page_class[page](app_data=app_data, app_url=app_url)
page_obj.run()

st.sidebar.markdown('- based on data {} from [coinmarket]({}) \n'.format(
    app_data.data_path.split('/')[-1].split('.')[0].split('_')[1],
    'https://coinmarketcap.com/') + '- [source code]({})'.format(
    'https://github.com/lightondust/token-analysis'))
