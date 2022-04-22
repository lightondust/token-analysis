from abc import ABC, abstractmethod
from app_data import AppData


class BasePage(ABC):
    def __init__(self, app_data: AppData):
        self.app_data = app_data

    @abstractmethod
    def run(self):
        pass
