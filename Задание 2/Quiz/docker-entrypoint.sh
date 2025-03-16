#!/bin/bash

# Применяем миграции
python manage.py migrate --noinput

# Загружаем фикстуры
python manage.py loaddata firstapp/fixtures/initial_data.json --noinput

# Запускаем команду, переданную в CMD (то есть, сервер)
exec "$@"