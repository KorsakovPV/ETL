# Проектное задание: ETL

[comment]: <> (В предыдущем модуле вы реализовывали механизм для полнотекстового поиска. Теперь улучшим его: научим его работать с новой схемой и оптимизируем количество элементов для обновления.)

[comment]: <> (## Подсказки)

[comment]: <> (Перед тем как вы приступите к выполнению задания, дадим несколько подсказок:)

[comment]: <> (1. Прежде чем выполнять задание, подумайте, сколько ETL-процессов вам нужно.)

[comment]: <> (2. Для валидации конфига советуем использовать pydantic.)

[comment]: <> (3. Для построения ETL-процесса используйте корутины.)

[comment]: <> (4. Чтобы спокойно переживать падения Postgres или Elasticsearch, используйте решение с техникой `backoff` или попробуйте использовать одноимённую библиотеку.)

[comment]: <> (5. Ваше приложение должно уметь восстанавливать контекст и начинать читать с того места, где оно закончило свою работу.)

[comment]: <> (6. При конфигурировании ETL-процесса подумайте, какие параметры нужны для запуска приложения. Старайтесь оставлять в коде как можно меньше «магических» значений.)

[comment]: <> (7. Желательно, но необязательно сделать составление запросов в БД максимально обобщённым, чтобы не пришлось постоянно дублировать код. При обобщении не забывайте о том, что все передаваемые значения в запросах должны экранироваться.)

[comment]: <> (8. Использование тайпингов поможет сократить время дебага и повысить понимание кода ревьюерами, а значит работы будут проверяться быстрее :&#41;)

[comment]: <> (9. Обязательно пишите, что делают функции в коде.)

[comment]: <> (10. Для логирования используйте модуль `logging` из стандартной библиотеки Python.)

[comment]: <> (Желаем вам удачи в написании ETL! Вы обязательно справитесь 💪 )

[comment]: <> (**Решение задачи залейте в папку `postgres_to_es` вашего репозитория.**)

## Разворачивание проекта

1.  С клонируйте проект

        git clone https://github.com/KorsakovPV/ETL
    
    В корневой папке находим файл .env.sample. Это шаблон файла переменных окружения. По образу и подобию необходимо создать файл .env и заполнить его своими значениями.


2. Запускаем процесс сборки и запуска контейнеров Команды со второй по восьмую выполняют генерирование тестовых данных:

        docker-compose up -d --build

3. создаем базу 

        docker-compose exec db psql -U postgres -c 'CREATE DATABASE movies3;'

4. Накатываем миграции:

        docker-compose exec admin_panel python manage.py migrate

5. Создаем пользователя с правами администратора:

        docker-compose exec admin_panel python manage.py createsuperuser

6. Добавляем в базу тестовые случайно сгенерированные данные:

        docker-compose exec admin_panel python manage.py generating_data

7. Собираем статику:

        docker-compose exec admin_panel python manage.py collectstatic

8. Остановите контейнер

       docker-compose up -d --build


9. Запустите контейнер с ETL.

        docker-compose -f docker-compose.etl.yaml up -d --build


При работе над проектом использован стек технологий: **[Django](https://www.djangoproject.com/)**, **[Python](https://www.python.org/)**, **[PostgreSQL](https://www.postgresql.org/)**, **[NGINX](https://nginx.org/)**, **[Docker](https://www.docker.com/)**, **[Docker-Compose](https://docs.docker.com/compose/)**, **[GitHub](https://github.com)**, код написан в IDE **[PyCharm](https://www.jetbrains.com/pycharm/)**, **[OS Linux Mint](https://linuxmint.com/)**