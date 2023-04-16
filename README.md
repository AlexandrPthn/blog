### **Тестовое задание**
### Описание
Проект Blog - cоциальная сеть ведения постов. Блог с возможностью публикации постов, подпиской на блог авторов, возможностью оставлять комментарии на посты.


### Стек
![Workflow](https://github.com/AlexandrPthn/foodgram-project-react/actions/workflows/main.yml/badge.svg?event=push)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

### Подготовка запуска локально
Для запуска проекта необходимо чтоб на компьютере был установлен Docker Desktop
Клонировать репозиторий:
```
git clone https://github.com/AlexandrPthn/blog.git
```
Перейти в каталог ../blog_project/infra_local выполнить:
```
docker-compose up -d --build
```
После успешной сборки выполнить миграции:
```
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
```
Создать суперпользователя:
```
docker compose exec backend python manage.py createsuperuser
```
Собрать статику:
```
docker compose exec backend python manage.py collectstatic --noinput
```

### API проекта
Примеры запросов можно посмотреть после запуска проекта по ссылкам:
http://127.0.0.1/swagger/
либо
http://127.0.0.1/redoc/

### Автор
Кокушин Александр