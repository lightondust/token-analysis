from plotly import express as px
import streamlit as st
import numpy as np
import pandas as pd
from app_data import AppData
from app_util import show_fig


def plot_tag_stats(app_data: AppData):
    tag_coins = app_data.tag_coins
    coin_tags = app_data.coin_tags
    tag_info_df = app_data.tag_info_df

    graph_type = st.selectbox('graph type', ['bar', 'scatter'])
    log_scale = st.checkbox('log scale', value=True)
    y_selected = st.selectbox('y:', ['count', 'market_cap'])
    tag_type = st.selectbox('tag group:', ['all', 'ecosystem'])
    highlight_tags = st.multiselect('highlight tags:', tag_coins.keys())
    high_light_tags_of_coins = st.multiselect('highlight tags:', coin_tags.keys())
    for c in high_light_tags_of_coins:
        highlight_tags += coin_tags[c]
    highlight_tags = list(set(highlight_tags))

    df_show = tag_info_df.copy().sort_values(by=y_selected)[::-1]
    if tag_type != 'all':
        df_show = df_show[df_show.tag_type == tag_type]

    def high_light(tag):
        if tag in highlight_tags:
            return tag
        else:
            return ''
    df_show['color'] = df_show.tag.apply(high_light)

    range_y=[0.1, 1.1*tag_info_df[y_selected].max()]

    if graph_type == 'bar':
        fig = px.bar(df_show, y=y_selected, x='tag', hover_data=['tag'], color='color', log_y=log_scale, range_y=range_y)
    else:
        fig = px.scatter(df_show, y=y_selected, x='tag', hover_data=['tag'], color='color', log_y=log_scale, range_y=range_y)

    show_fig(fig)


def plot_tag_members(app_data: AppData):
    tag_coins = app_data.tag_coins
    data_df = app_data.data_df

    tag_selected = st.selectbox('tag', tag_coins.keys())
    log_scale = st.checkbox('log scale', value=True)
    y_selected = 'market_cap'

    c_s = tag_coins[tag_selected]
    c_s_id = [int(c.split('_')[0]) for c in c_s]
    df_show = data_df[data_df.id.isin(c_s_id)]
    fig = px.bar(df_show, y=y_selected, x='name', log_y=log_scale, range_y=[0.1, 1.1 * data_df[y_selected].max()])
    show_fig(fig)


def plot_coins(app_data: AppData):
    data_df = app_data.data_df
    tag_coins = app_data.tag_coins

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


def get_tag_sim_df(app_data):
    tag_coins = app_data.tag_coins
    tag_list = list(tag_coins.keys())

    tag_tag_sim = []
    for tag in tag_list:
        coins = tag_coins[tag]
        for tag_tar in tag_list:
            if tag_tar != tag:
                coins_tar = tag_coins[tag_tar]
                n_int = len(set(coins).intersection(set(coins_tar)))
                if n_int:
                    tag_tag_sim.append([tag, tag_tar, n_int / np.sqrt(len(coins) * len(coins_tar))])
    tag_tag_sim_df = pd.DataFrame(tag_tag_sim, columns=['tag_src', 'tag_tar', 'weight'])
    return tag_tag_sim_df, tag_tag_sim


def tag_sim(app_data):
    tag_sim_df, tag_sim_list = get_tag_sim_df(app_data)
    tag_coins = app_data.tag_coins
    tag_list = list(tag_coins.keys())
    tag_select = st.selectbox('target tags:', tag_list)
    df_show = tag_sim_df[tag_sim_df.tag_src == tag_select]
    df_show = df_show.sort_values(by='weight')[::-1].reset_index().drop('index', axis=1)
    st.table(df_show)


def tag_graph(app_data):
    import networkx as nx
    import matplotlib.pyplot as plt

    tag_coins = app_data.tag_coins
    tag_list_all = list(tag_coins.keys())
    tag_list = tag_list_all
    tag_tag_sim_df, tag_tag_sim = get_tag_sim_df(app_data)

    ecosystem_tags = [t for t in list(tag_coins.keys()) if 'ecosystem' in t]
    fund_tags = [t for t in list(tag_coins.keys()) if 'portfolio' in t or 'capital' in t or 'group' in t]
    graph_type = st.selectbox('graph type:', ['ecosystem', 'fund', 'tag adj'])

    if graph_type == 'ecosystem':
        tags_filter = ecosystem_tags
    elif graph_type == 'fund':
        tags_filter = fund_tags
    else:
        tag_select = st.selectbox('target tags:', tag_list)
        tags_filter = tag_tag_sim_df[tag_tag_sim_df.tag_src == tag_select].tag_tar.to_list()
        st.markdown('### tag sim')
        tag_tag_sim_df_single = tag_tag_sim_df[tag_tag_sim_df.tag_src == tag_select]
        tag_tag_sim_df_single = tag_tag_sim_df_single.sort_values(by='weight')[::-1]
        tag_tag_sim_df_single = tag_tag_sim_df_single.reset_index()
        st.dataframe(tag_tag_sim_df_single)

    st.markdown('### graph links')
    tag_tag_sim_df_show = tag_tag_sim_df[tag_tag_sim_df.tag_src.isin(tags_filter)
                                         & tag_tag_sim_df.tag_tar.isin(tags_filter)]
    tag_tag_sim_df_show = tag_tag_sim_df_show.sort_values(by='weight')[::-1]
    tag_tag_sim_df_show = tag_tag_sim_df_show.reset_index()
    st.dataframe(tag_tag_sim_df_show)
    st.write(tag_tag_sim_df_show.shape)
    st.write(len(tags_filter))
    st.markdown('### tag graph sim distribution')
    fig_hist = px.histogram(tag_tag_sim_df_show, x='weight')
    st.plotly_chart(fig_hist)

    if_display_graph = st.checkbox('display graph')

    if if_display_graph:
        g = nx.Graph()
        g.add_nodes_from(tag_list)

        for sim in tag_tag_sim:
            g.add_edge(sim[0], sim[1], weight=sim[2])

        g_show = g.subgraph(tags_filter)

        fig = plt.figure(1, figsize=(30, 30))
        f = nx.draw(g_show, with_labels=True, font_color='red', font_size=20)
        st.pyplot(fig)
    # st.write(tags_filter)


def tag2vec(app_data: AppData):

    tag_coins = app_data.tag_coins
    model = app_data.tag2vec_model

    tag_select = st.selectbox('tag', list(tag_coins.keys()))
    tag_sim = model.wv.most_similar(tag_select, topn=100)
    tag_sim = [list(t) for t in tag_sim]
    for tag_info in tag_sim:
        tag_info.append(len(tag_coins[tag_info[0]]))
    tag_sim_df = pd.DataFrame(tag_sim, columns=['tag', 'similarity', 'coins_in_tag'])
    tag_sim_df['score'] = tag_sim_df.similarity * np.log(tag_sim_df.coins_in_tag)
    tag_sim_df = tag_sim_df.sort_values('score')[::-1]
    st.dataframe(tag_sim_df, height=500)
