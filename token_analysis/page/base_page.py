from abc import ABC, abstractmethod
from app_data import AppData
from app_url import AppURL
import streamlit as st
import urllib


class BasePage(ABC):
    def __init__(self, app_data: AppData, app_url: AppURL):
        self.app_data = app_data
        self.app_url = app_url

    @abstractmethod
    def run(self):
        pass

    def token_select(self):
        tokens = list(self.app_data.token_tags.keys())
        token_select = st.selectbox('change token', tokens + [''], index=len(tokens))
        token = ''
        if token_select:
            token = token_select
            self.app_url.set_query_params('token', token_select)
        else:
            if self.app_url.token:
                token = self.app_url.token
        st.markdown('#### selected token: {}'.format(token))
        return token

    def token_link(self, token):
        params = self.app_url.query_params
        params['token'] = token
        d_qs = urllib.parse.urlencode(params, doseq=True)
        return '<a target="_blank" href="./?{}">link</a>'.format(d_qs)
