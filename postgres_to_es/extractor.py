import logging

from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor

from models import AbstractExtractor

logging.basicConfig(filename="etl.log", level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PostgresExtractor(AbstractExtractor):
    data = []

    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = pg_conn.cursor(cursor_factory=RealDictCursor)

    def get_data(self, table, column, pointer_begin_date, pointer_end_date):
        """
        Получает не проиндексированные фильмы
        :return: результат выборки
        """
        sql = f"""
            SELECT
                id,
                {column} 
            FROM public."content.{table}" d 
            WHERE d.modified <= to_date( '{str(pointer_end_date)}', 'YYYY-MM-DD HH24:MI:SS' ) AND d.modified > to_date( '{str(pointer_begin_date)}', 'YYYY-MM-DD HH24:MI:SS' )
        """

        self.cursor.execute(sql)
        self.data = self.cursor.fetchall()

        return self.data
