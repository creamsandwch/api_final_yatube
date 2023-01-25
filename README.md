# api_final
api final
Как запустить проект (для Windows):
Клонировать репозиторий и перейти в него в командной строке:

git clone git@github.com:creamsandwch/api_final_yatube.git
cd yatube_api

Cоздать и активировать виртуальное окружение:
python -m venv venv
. venv/scripts/activate # для Windows

Установить зависимости из файла requirements.txt:
python -m pip install --upgrade pip
pip install -r requirements.txt

Выполнить миграции:
python manage.py migrate

Запустить проект:
python manage.py runserver

В проекте не реализованы .html шаблоны, только CRUD API проекта yatube,
который предоставляет функционал создания и управления постами,
комментировая чужих и своих постов, подписок на других авторов.

Все запросы к API обрабатываются по url: api/v1/. Авторизация реализована 
с помощью JWT-токенов и djoser по адресу api/v1/auth/. 
Список запросов djoser: https://djoser.readthedocs.io/en/latest/getting_started.html

