![](https://img.shields.io/badge/Python-3.8.7-blue) 
![](https://img.shields.io/badge/Django-3.2.13-green)
![](https://img.shields.io/badge/DjangoRestFramework-3.13.1-red)
![](https://badgen.net/badge/icon/postgresql?icon=postgresql&label)
![](https://github.com/BogovAlex/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Продуктовый помощник Foodgram

Сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Развернутый проект с заполненными данными доступен по адерсу: http://foodgram.viewdns.net/


## :computer: Технологии в проекте

:small_blue_diamond: Python <br>
:small_blue_diamond: Django <br>
:small_blue_diamond: Django REST Framework <br>
:small_blue_diamond: React JS <br>
:small_blue_diamond: PostgreSQL <br>
:small_blue_diamond: Docker <br>


## :pencil2: Инструкции по запуску

Клонировать репозиторий, создать и активировать виртуальное окружение:

```sh
git clone git@github.com:BogovAlex/foodgram-project-react.git
cd foodgram-project-react
python -m venv venv
source venv/Scripts/activate
pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r backend/foodgram_project/requirements.txt
```

Из папки backend/foodgram_project/ выполнить миграции:

```
python manage.py migrate
```

Наполнить БД базовыми ингредиентами выполнив команду:

```
python manage.py db_fill_ingredient
```

Из папки infra выполните команду:

```
docker-compose up -d
```

## :books: Документация
Документация к проекту доступна по адресу:

```html
http://localhost/api/docs/redoc.html
```


## :bust_in_silhouette: Автор проекта 
#### Алексей Богов _(Alexey Mi. Bogov)_
E-mail: hi@abogov.ru<br>
GitHub: https://github.com/BogovAlex
