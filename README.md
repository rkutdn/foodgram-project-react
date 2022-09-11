
# YaMDb
![workflow passing bage](https://github.com/rkutdn/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Описание проекта
**Foodgram** – Проект Foodgram gортал для обмена рецептами невероятных блюд    
Публичный адрес сервера: [158.160.8.42](http://158.160.8.42/)


## Как запустить проект в docker (dev-режим):

- Клонировать репозиторий и перейти в директорию с docker-compose.yaml:

```
git clone git@github.com:rkutdn/foodgram-project-react.git
cd foodgram/infra
```

- Развернуть 4 контейнера, nginx, database, front и web(сам проект + gunicorn):

```
docker-compose up -d
```

- Выполнить миграции и собрать статику:

```
docker-compose exec web python3 manage.py migrate
docker-compose exec web python3 manage.py collectstatic --no-input
```

- Создать суперюзера:

```
docker-compose exec web python manage.py createsuperuser
```

## Проект запущен и доступен по адресу:
- http://localhost/redoc/ - подробная документация
- http://localhost/api/ - url для api запросов
- http://localhost/auth/ - url для запросов авторизации
- http://localhost/users/ - url для запросов связанных с пользователями
- http://localhost/admin - админ зона

## Шаблон заполнения файла .env

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql  
DB_NAME=postgres # имя базы данных  
POSTGRES_USER=postgres # логин для подключения к базе данных  
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)  
DB_HOST=db # название сервиса (контейнера)  
DB_PORT=5432 # порт для подключения к БД

SECRET_KEY='some_secret_key_string'

## Автор
Савенко Юрий <rkutdn@ya.ru>