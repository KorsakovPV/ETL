from models import AbstractTransformer


class Transformer(AbstractTransformer):

    def transform(self, row) -> dict:
        pass
        """
        Преобразование названий полей в структуру для elastic search
        :param row: поле для преобразования
        :return:
        """

        return {
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                # 'creation_date': row['creation_date'],
                'certificate': row['certificate'],
                'file_path': row['file_path'],
                'rating': row['rating'],
                'type': row['type'],
                'mpaa_rating': row['mpaa_rating'],
                # 'created': row['created'],
                # 'modified': row['modified'],
            }
