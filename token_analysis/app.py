import streamlit as st
from tag_analysis import plot_tag_stats, plot_tag_members, plot_coins, tag_graph, tag2vec, tag_sim
from app_data import get_app_data, pre_process
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%m/%d/%Y %X")

st.set_page_config(layout='wide', page_title='token analysis', page_icon='./favico_s_t.png')


@st.cache(allow_output_mutation=True)
def _get_app_data():
    return get_app_data()


app_data = _get_app_data()

page_function = {
    'token marketcap': plot_coins,
    'tokens in tag': plot_tag_members,
    'tag statistice': plot_tag_stats,
    'tag similarity': tag_sim,
    'tag graph': tag_graph,
    'tag2vec': tag2vec
}
page = st.sidebar.radio('page:', page_function.keys())

page_function[page](app_data)

st.sidebar.markdown('- based on data {} from [coinmarket]({}) \n'.format(
    app_data.data_path.split('/')[-1].split('.')[0].split('_')[1],
    'https://coinmarketcap.com/') + '- [source code]({})'.format(
    'https://github.com/lightondust/token-analysis'))

