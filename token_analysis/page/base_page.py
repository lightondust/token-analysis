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
        token_select = st.selectbox('change token', [''] + tokens)
        token = self.app_url.sync_variable('token', token_select, '')
        st.markdown('#### selected token: {}'.format(token))
        return token

    def token_link(self, token):
        return '<a target="_blank" href="{}">link</a>'.format(self.app_url.internal_link(token=token))

