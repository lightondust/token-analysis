import streamlit as st


def show_fig(fig, fig_el=None, size=None):
    if size is None:
        size = {'width': 1200, 'height': 800}
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    fig.update_layout(**size)
    if fig_el:
        fig_gen = fig_el.plotly_chart
    else:
        fig_gen = st.plotly_chart
    fig_gen(fig, **size)
