import datetime
import json
import logging
import os
from functools import wraps
from time import sleep
from typing import Optional, Any

import backoff
import psycopg2
from elasticsearch import Elasticsearch

from extractor import PostgresExtractor
from loader import ESLoader
from models import AbstractExtractor, AbstractLoader, AbstractTransformer, PostgreSettings, BaseStorage, logger, \
    FILE_NAME
from transformer import Transformer




def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


@backoff.on_exception(backoff.expo, BaseException)
def etl(target):
    logger.info('etl.py. Started.')
    while True:
        pointer_begin_date = datetime.datetime.strptime(state.get_state('pointer_begin_date'), '%Y-%m-%d %H:%M:%S')
        pointer_end_date = pointer_begin_date + datetime.timedelta(days=1)

        while datetime.datetime.now() < pointer_end_date:
            logger.info(f'etl.py. pointer_end_date > now() pointer_end_date={pointer_end_date}, now()={datetime.datetime.now()}. Wait one hours.')
            sleep(3600)

        target.send(['film_work', 'title', pointer_begin_date, pointer_end_date])
        target.send(['person', 'full_name', pointer_begin_date, pointer_end_date])
        target.send(['genre', 'name', pointer_begin_date, pointer_end_date])

        state.set_state('pointer_begin_date', str(pointer_end_date))
        sleep(0.1)


@coroutine
@backoff.on_exception(backoff.expo, BaseException)
def extract(target, extractor: AbstractExtractor):
    """ Получение неиндексированных данных """
    while key := (yield):

        table, column, pointer_begin_date, pointer_end_date = key
        extractor.get_data(
            target=target,
            table=table,
            column=column,
            pointer_begin_date=pointer_begin_date,
            pointer_end_date=pointer_end_date
        )



@coroutine
@backoff.on_exception(backoff.expo, BaseException)
def transform(target, transformer: AbstractTransformer):
    """ Подготовка записей для загрузки в elastic """
    while key := (yield):
        result, table, column = key
        transformed = []
        for row in result:
            transformed.append(transformer.transform(row, column))

        target.send([transformed, table, column])


@coroutine
@backoff.on_exception(backoff.expo, BaseException)
def load(loader: AbstractLoader):
    """ Загрузка в elastic """
    while key := (yield):

        transformed, table, column = key
        if len(transformed) == 0:
            continue

        logger.info(f'etl.py. Loaded start {table}. {len(transformed)} items.')
        loader.load(transformed, table)
        logger.info(f'etl.py. Loaded stop {table}. {len(transformed)} items.')


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        if self.file_path is None:
            return

        with open(self.file_path, 'w') as f:
            json.dump(state, f)

    def retrieve_state(self) -> dict:
        if self.file_path is None:
            logging.info('No state file provided. Continue with in-memory state')
            return {}

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)

            return data

        except FileNotFoundError:
            self.save_state({})


class State:
    """
     Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.state = self.retrieve_state()

    def retrieve_state(self) -> dict:
        data = self.storage.retrieve_state()
        if not data:
            return {}
        return data

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.state[key] = value

        self.storage.save_state(self.state)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        return self.state.get(key)


def connect_to_database():
    conn = None
    try:
        conn = psycopg2.connect(**PostgreSettings().dict())
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logger.info(f'etl.py. Connect to database ERROR. {error}')
    return False


if __name__ == '__main__':

    json_file_storage = JsonFileStorage(FILE_NAME)
    state = State(json_file_storage)
    begin_date = state.get_state('pointer_begin_date') or datetime.datetime(year=2000, month=1, day=1)
    state.set_state('pointer_begin_date', str(begin_date))

    while not connect_to_database():
        logger.info(f'etl.py. Wait connect to database Postgres. 10 sec.')
        sleep(10)

    es = Elasticsearch([os.getenv('ES_HOST', 'http://localhost:9200/')])

    while not es.ping():
        logger.info(f'etl.py. Wait connect to database Elasticsearch. 10 sec.')
        sleep(10)

    with psycopg2.connect(**PostgreSettings().dict()) as pg_conn:
        # этап загрузки в es
        loader = load(ESLoader(os.getenv('ES_HOST', 'http://localhost:9200/')))

        # этап подготовки данных
        transformer = transform(loader, Transformer())

        # этап получения записей
        extractor = extract(transformer, PostgresExtractor(pg_conn))

        # запуск etl процесса
        etl(extractor)
