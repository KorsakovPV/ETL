import logging
from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor
from models import AbstractExtractor

logger = logging.getLogger()


class PostgresExtractor(AbstractExtractor):

    data = []

    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = pg_conn.cursor(cursor_factory=RealDictCursor)

    def get_data(self):
        """
        Получает не проиндексированные фильмы с сопутствующими данными
        :return: результат выборки
        """
        sql = """
            SELECT * 
            FROM public."content.film_work"
            WHERE not indexed
            ORDER BY id ASC LIMIT 100
                 
        """

        self.cursor.execute(sql)
        self.data = self.cursor.fetchall()

        logger.info(f'Extracted {len(self.data)}')
        return self.data

    def set_index(self):
        """
        После загрузки устанавливается признак индексации
        Снятие индексации происходит во время обновления записей в админке
        :return:
        """
        data = ','.join(self.cursor.mogrify('%s', (item['id'],)).decode()
                        for item in self.data)
        sql = f"""
            UPDATE public."content.film_work"
            SET indexed = True
            WHERE id in ({data});
        """

        self.cursor.execute(sql, (data, ))
        self.conn.commit()
        logger.info(f'Indexed {len(self.data)}')
