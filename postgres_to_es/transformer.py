from models import AbstractTransformer


class Transformer(AbstractTransformer):

    def transform(self, row, column) -> dict:
        """
        Преобразование названий полей в структуру для elastic search
        :param row: поле для преобразования
        :return:
        """

        return {
                'id': row.get('id'),
                column: row.get(column)
            }
