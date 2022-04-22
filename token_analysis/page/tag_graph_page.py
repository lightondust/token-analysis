from plotly import express as px
import networkx as nx
import matplotlib.pyplot as plt

from page.base_page import BasePage
import streamlit as st

from app_data import get_tag_sim_df


class TagGraphPage(BasePage):
    def __init__(self, app_data):
        super().__init__(app_data)
        self.title = 'Tag Graph'
        st.title(self.title)

    def run(self):
        self.tag_graph()

    def tag_graph(self):
        tag_coins = self.app_data.tag_coins
        tag_list_all = list(tag_coins.keys())
        tag_list = tag_list_all
        tag_tag_sim_df, tag_tag_sim = get_tag_sim_df(self.app_data)

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
