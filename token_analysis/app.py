import streamlit as st

from app_url import AppURL
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
def _get_app_data():
    return get_app_data()


app_data = _get_app_data()
app_url = AppURL()

page_class = {
    'Token marketcap': TokenMarketCapPage,
    'Token similarity': TokenSimilarityPage,
    'Token2vec': Token2VecPage,
    'All2vec': All2VecPage,
    'Tag members': TagMembersPage,
    'Tag similarity': TagSimilarityPage,
    'Tag2vec': Tag2VecPage,
    'Tag statistics': TagStatisticsPage,
    'Tag graph': TagGraphPage,
    'Template_page': TemplatePage
}
page_selected = st.sidebar.radio('page:', list(page_class.keys())+[''], index=len(page_class))

if page_selected:
    app_url.set_query_params('page', page_selected)
    page = page_selected
else:
    if app_url.page:
        page = app_url.page
    else:
        page = 'Token marketcap'

# st.write(app_url.query_params)
page_obj = page_class[page](app_data=app_data, app_url=app_url)
page_obj.run()

st.sidebar.markdown('- based on data {} from [coinmarket]({}) \n'.format(
    app_data.data_path.split('/')[-1].split('.')[0].split('_')[1],
    'https://coinmarketcap.com/') + '- [source code]({})'.format(
    'https://github.com/lightondust/token-analysis'))
