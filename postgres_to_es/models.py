import abc
import logging
from abc import ABCMeta, abstractmethod

from pydantic import BaseSettings, Field

logging.basicConfig(filename="etl.log", level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
FILE_NAME = 'data_file.json'
PADGE = 50

class PostgreSettings(BaseSettings):
    """
    Настройки подключения к базе данных
    """
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: str = Field(..., env='POSTGRES_PORT')

    class Config:
        env_file: str = '../.env'


class AbstractExtractor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data(self):
        pass
        """
        Возвращает массив не индексированных объектов
        :return:
        """

    @abstractmethod
    def set_index(self):
        pass
        """
        Выставляет загруженным объектам признак индексации
        :return:
        """


class AbstractTransformer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def transform(self, row):
        pass
        """
        Преобразование строки в формат для загрузки
        :param row: объект для преобразования
        :return:
        """


class AbstractLoader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self, data):
        pass
        """
        Реализация этапа загрзки данных
        :param data: массив данных для загрузки
        :return:
        """

class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass