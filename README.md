# LMS (Learning Management System)
Система управления обучением, разработанная с использованием Django REST Framework.
## Описание проекта
Проект представляет собой API для системы управления обучением, которая позволяет:
- Управлять курсами и уроками
- Регистрировать и управлять пользователями
- Загружать медиа-контент (превью для курсов и уроков)
## Структура проекта
```
DRF-Practice/
├── config/             # Основные настройки проекта
├── lms/                # Приложение для управления курсами
│   ├── models.py       # Модели курсов и уроков
│   ├── serializers.py  # Сериализаторы для API
│   ├── views.py        # Представления API
│   └── urls.py         # URL маршруты
├── users/              # Приложение для управления пользователями
│   ├── models.py       # Модель пользователя
│   ├── serializers.py  # Сериализаторы пользователя
│   ├── views.py        # Представления пользователя
│   └── urls.py         # URL маршруты
└── manage.py           # Скрипт управления Django
```
## Технологии
- Python 3.13
- Django 5.1.7
- Django REST Framework 3.16.0
- PostgreSQL
- Poetry (управление зависимостями)
### Дополнительные инструменты
- Black (форматирование кода)
- Flake8 (линтер)
- isort (сортировка импортов)
- Pillow (обработка изображений)
- environs (управление переменными окружения)
## Установка и запуск
1. Клонируйте репозиторий:
```bash
git clone <repository-url>
```
2. Установите зависимости с помощью Poetry:
```bash
poetry install
```
3. Создайте файл `.env` в корневой директории и укажите необходимые переменные окружения:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```
4. Примените миграции:
```bash
poetry run python manage.py migrate
```
5. Запустите сервер разработки:
```bash
poetry run python manage.py runserver
```


## API Endpoints
### Курсы
- `GET /courses/` - список всех курсов
- `POST /courses/` - создание нового курса
- `GET /courses/{id}/` - детали курса
- `PUT /courses/{id}/` - обновление курса
- `DELETE /courses/{id}/` - удаление курса
### Уроки
- `GET /lessons/` - список всех уроков
- `POST /lessons/` - создание нового урока
- `GET /lessons/{id}/` - детали урока
- `PUT /lessons/{id}/` - обновление урока
- `DELETE /lessons/{id}/` - удаление урока
### Пользователи
- `POST /users/register/` - регистрация нового пользователя
- `GET/PUT /users/profile/{id}/` - просмотр/обновление профиля пользователя
## Автор
Антонюк Евгений
- GitHub: [@AntonyukEvgeniy](https://github.com/AntonyukEvgeniy)
## Лицензия
MIT
