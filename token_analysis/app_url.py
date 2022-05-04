import streamlit as st


class AppURL(object):
    def __int__(self):
        pass

    @property
    def query_params(self):
        query_params = st.experimental_get_query_params()
        return query_params

    @property
    def page(self):
        return self.query_params.get('page', [''])[0]

    def set_query_params(self, key, value):
        params = self.query_params
        params[key] = value
        st.experimental_set_query_params(**params)

