# Foodgram

![My own! workflow](https://github.com/fruitybang/foodgram-project-react/actions/workflows/main.yml/badge.svg) 

## Стек 
`Python` `Django` `Django Rest Framework` `Docker` `Gunicorn` `NGINX` `PostgreSQL` `CI/CD`

Продуктовый помощник, онлайн-сервис для публикации собственных рецептов, подписки на публикации других пользователей. Можно добавлять рецпеты в "избранное", а также в "покупки" для скачивания списка игредиентов в формате .txt.

**Ссылка на [проект](http://130.193.43.92/)**

## Как запустить проект

- Клонировать репозиторий и перейти в него в командной строке:

git clone git@github.com:FruityBang/foodgram-project-react.git

cd foodgram-project-react

- Подготовить доступный сервер для развертывания:

sudo systemctl stop nginx 

sudo apt install docker.io 

sudo curl -SL https://github.com/docker/compose/releases/download/v2.17.2/ocker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

скопировать файлы docker-compose.yaml и nginx.conf из проекта на сервер  home/<ваш_username>/

- Добавить в Secrets GitHub Actions переменные окружения для работы Workflow

*Проект будет развернут автоматически при пуше в ветку master*
