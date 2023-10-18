## __Запуск__
1. Клонируйте репозиторий и перейдите в него в командной строке:
```bash
git clone git@github.com:94R1K/avangard.git
```
```bash
cd avangard
```

2. Создайте файл .env:
```bash
touch .env
```
3. Опишите файл **.env** по примеру файла **.env.example**:

2. Выполните команду запуска docker-compose.yml:
```bash
docker-compose up -d
```

3. После того как контейнеры с PostgreSQL и Flask запустятся, нужно инициализировать SQLAlchemy, создать и применить миграции:
```bash
docker-compose exec -T app flask db init
```
```bash
docker-compose exec -T app flask db migrate
```
```bash
docker-compose exec -T app flask db upgrade
```

# ___Об авторе___
Лошкарев Ярослав Эдуардович \
Python-разработчик (Backend) \
Россия, г. Москва \
E-mail: real-man228@yandex.ru

[![VK](https://img.shields.io/badge/Вконтакте-%232E87FB.svg?&style=for-the-badge&logo=vk&logoColor=white)](https://vk.com/yalluv)
[![TG](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/yallluv)