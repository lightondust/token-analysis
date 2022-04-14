import streamlit as st
from tag_analysis import plot_tag_stats, plot_tag_members, plot_coins, tag_graph, tag2vec
from app_data import get_app_data

st.set_page_config(layout='wide')


@st.cache
def _get_app_data():
    # return {}
    return get_app_data()


def tst(app_data):
    st_no = st.selectbox('aaa', [1,2,3])


app_data = _get_app_data()
page_function = {
    'tst': tst,
    'tag stats': plot_tag_stats,
    'tag members': plot_tag_members,
    'coins': plot_coins,
    'tag sim graph': tag_graph,
    'tag2vec': tag2vec
}
page = st.sidebar.radio('page:', page_function.keys())

page_function[page](app_data)




