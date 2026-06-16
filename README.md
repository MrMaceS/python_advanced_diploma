# Сервис микроблогов (аналог Twitter)

Бэкенд для корпоративного сервиса микроблогов (аналог Twitter), реализованный на **FastAPI** с использованием **PostgreSQL** и **Nginx**.  
Проект соответствует ТЗ: поддерживаются твиты с картинками, лайки, подписки и лента по популярности.

## Стек

- Python, FastAPI
- PostgreSQL
- SQLAlchemy
- Nginx
- Docker, Docker Compose
- pytest, flake8, mypy, black

## Функциональные возможности

Сервис реализует следующие возможности (согласно ТЗ):

1. Пользователь может добавить новый твит: `POST /api/tweets`
2. Пользователь может удалить свой твит: `DELETE /api/tweets/{tweet_id}`
3. Пользователь может зафоловить другого пользователя: `POST /api/users/{user_id}/follow`
4. Пользователь может отписаться от другого пользователя: `DELETE /api/users/{user_id}/follow`
5. Пользователь может отмечать твит как понравившийся: `POST /api/tweets/{tweet_id}/likes`
6. Пользователь может убрать отметку «Нравится»: `DELETE /api/tweets/{tweet_id}/likes`
7. Пользователь может получить ленту твитов от пользователей, на которых он подписан, отсортированных по количеству лайков (по убыванию), затем по дате (сначала новые): `GET /api/tweets`
8. Твит может содержать картинку: загрузка файла `POST /api/medias`, привязка к твиту через `tweet_media_ids`
9. Пользователь может получить информацию о своём профиле: `GET /api/users/me`
10. Пользователь может получить информацию о произвольном профиле: `GET /api/users/{user_id}`

Все ответы сервиса имеют поле `result` и при ошибках возвращают `error_type` и `error_message`.

## Архитектура

Проект состоит из трёх основных сервисов:

- `app` — FastAPI-приложение, реализующее бизнес-логику и REST API
- `db` — PostgreSQL, хранит пользователей, твиты, лайки, подписки и медиа
- `nginx_web` — Nginx, отдаёт фронтенд и медиа-файлы, проксирует запросы к backend

## Структура проекта

```text
python_advanced_diploma/
│
├── static/                  # Собранный фронтенд (отдаётся через nginx)
│   ├── index.html
│   ├── favicon.ico
│   │
│   ├── css/
│   │   ├── app.45d81840.css
│   │   ├── chunk-6f77c742.8d9a3d9c.css
│   │   ├── chunk-10e0d5b4.130d80ef.css
│   │   ├── chunk-0420bcc4.d6bc3184.css
│   │   ├── chunk-732a3e8c.6334cd6b.css
│   │   └── chunk-vendors.de691de6.css
│   │
│   └── js/
│       ├── app.ee2cdef2.js
│       ├── chunk-6f77c742.f09861a7.js
│       ├── chunk-10e0d5b4.e80e67b6.js
│       ├── chunk-0420bcc4.11441662.js
│       ├── chunk-732a3e8c.57e36fb4.js
│       ├── chunk-76301fe8.cc56c3b1.js
│       └── chunk-vendors.398321e0.js
│
├── backend/                 # Бэкенд (FastAPI приложение)
│   └── app/
│       ├── __init__.py
│       ├── main.py          # Точка входа FastAPI
│       ├── config.py        # Конфигурация (env, DB URL)
│       ├── database.py      # Подключение к PostgreSQL
│       │
│       ├── models/          # SQLAlchemy модели
│       │   ├── __init__.py
│       │   ├── user.py      # User
│       │   ├── tweet.py     # Tweet
│       │   ├── like.py      # Like
│       │   ├── follow.py    # Follow
│       │   └── media.py     # Media
│       │
│       ├── schemas/         # Pydantic-схемы (для Swagger / валидации)
│       │   ├── __init__.py
│       │   ├── tweet.py
│       │   ├── user.py
│       │   ├── likes.py
│       │   └── media.py
│       │
│       ├── api/             # API endpoint'ы
│       │   ├── __init__.py
│       │   ├── tweets.py    # /api/tweets
│       │   ├── medias.py    # /api/medias
│       │   └── users.py     # /api/users
│       │
│       ├── services/        # Бизнес-логика
│       │   ├── __init__.py
│       │   ├── tweet_service.py
│       │   └── user_service.py
│       │
│       ├── middlewares/     # Middleware (проверка api-key)
│       │   ├── __init__.py
│       │   └── auth.py
│       │
│       └── media/           # Сохранённые картинки
│           ├── 1_image2.jpg
│           ├── 1_image3.jpg
│           ├── 1_image4.jpg
│           └── 1_images.jpg
│
├── tests/               # Unit-тесты
│      ├── __init__.py
│      ├── test_follow.py
│      ├── test_tweets.py
│      └── test_users.py
│
├── mypy.ini                 # Конфиг 
├── .flake8                  # Конфиг  
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile               # Образ приложения
├── docker-compose.yml       # Docker Compose (app + PostgreSQL + nginx)
├── nginx.conf               # Конфигурация Nginx
├── init_db.py               # Создание БД (таблиц)
├── seed_db.py               # Наполнение БД тестовыми данными
└── README.md
```

## Запуск через Docker Compose #WSL

### Предварительные требования

- Docker и Docker Compose
- Python 3.10+ (для локальных скриптов)

### Запуск

В корне проекта:

```bash
source .venv/bin/activate     # WSL
docker compose up -d          # Обычный запуск
docker compose up --build     # После изменений в коде
docker compose logs
```

Это поднимет:

- backend на порту `8000` (внутренний)
- PostgreSQL на `5432`
- Nginx с фронтендом на http://localhost:8080

### Инициализация базы (seed)

Для демонстрации работы приложения используются заранее подготовленные пользователи, твиты, лайки и медиа.

В отдельном терминале (на хосте, не в контейнере):

```bash
python seed_db.py
```

Скрипт:

- очищает существующие данные
- создаёт пользователей и связи
- добавляет твиты, лайки и привязывает к ним картинки (из `backend/media`)

После этого можно заходить на фронтенд.

### Доступ к фронтенду и API

После запуска:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Frontend (SPA): http://localhost:8080/

Для остановки:

```bash
docker compose down
```

Файл `.env` для Docker не обязателен — все переменные окружения заданы в `docker-compose.yml`.

Для авторизации используется HTTP-заголовок `api-key`. На фронтенде есть форма для ввода ключа.

Примеры пользователей (из сидера):

- `Mr.Mace` — `api-key: test`
- `SpongeBob` — `api-key: bob-key`
- `Lev` — `api-key: lev-key`
- `Alice` — `api-key: alice-key`
- `Bob` — `api-key: bob2-key`
- `Charlie` — `api-key: charlie-key`
- `Dana` — `api-key: dana-key`
- `Екатерина` — `api-key: katya-key`
- `Иван` — `api-key: ivan-key`
- `Николай` — `api-key: nik-key`

## Тестирование и качество кода

### Unit-тесты

Unit-тесты (папка `tests/`) покрывают:

- создание и удаление твитов
- лайки и снятие лайков
- формирование ленты (фолловеры/лайки/сортировка)
- загрузку и привязку медиа-файлов

Запуск тестов:

```bash
pytest -v
```

### Линтер

Для проверки стиля используется `flake8`:

```bash
flake8 backend tests
```

### Типизация (mypy)

Основные функции и сервисы аннотированы типами. Проверка статическими типами:

```bash
mypy backend
```

### Форматтер (black)

```bash
black backend tests --check
```

## Ошибки и формат ответов

При любой ошибке backend возвращает:

```json
{
  "result": false,
  "error_type": "SOME_ERROR_CODE",
  "error_message": "Human readable description"
}
```

Например:

- `EMPTY_TWEET`
- `TWEET_TOO_LONG`
- `TWEET_NOT_FOUND`
- `FORBIDDEN`
- `UPLOAD_MEDIA_ERROR`

## Критерии сдачи

| Критерий         | Требование                                                              |
| ---------------- | ----------------------------------------------------------------------- |
| Функциональность | Все 8 функциональных и 3 нефункциональных требования реализованы        |
| Деплой           | Проект разворачивается за 1–2 команды (docker-compose up -d)            |
| Код              | Pythonic, читаемый, проверен линтерами                                  |
| Типизация        | Основные сущности аннотированы, mypy с минимумом ошибок                 |
| Тесты            | Есть unit-тесты, при необходимости измеряется покрытие                  |
| Документация     | README.md с подробной инструкцией по эксплуатации и ссылками на Swagger |
