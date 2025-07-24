# E-Soft Analytics API

API-сервис для анализа данных с возможностью загрузки файлов (CSV/Excel), их обработки и визуализации.

## 📌 Возможности

- Загрузка файлов (CSV, Excel)
- Анализ данных (среднее, медиана, корреляция)
- Очистка данных (удаление дубликатов, заполнение пропусков)
- Генерация графиков
- Хранение результатов в PostgreSQL
- RESTful API интерфейс

## 🛠 Технологии

- Python 3.7+
- Flask
- Pandas
- SQLAlchemy
- PostgreSQL
- Matplotlib (для визуализации)

## ⚙️ Установка

1. Клонируйте репозиторий:

git clone https://github.com/yourusername/e-soft-analytics-api.git
cd e-soft-analytics-api

2. Создайте и активируйте виртуальное окружение:

python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac


3. Установите зависимости:

pip install -r requirements.txt


4. Настройте базу данных:
- Создайте БД в PostgreSQL:

CREATE DATABASE analytics_db;

- Обновите настройки в `config.py`

5. Создайте таблицы:

flask shell
>>> db.create_all()
>>> exit()


## 🚀 Запуск

python run.py

Сервер будет доступен по адресу: `http://localhost:5000`

## 📊 API Endpoints

| Метод | Эндпоинт                | Описание                          |
|-------|-------------------------|-----------------------------------|
| POST  | /api/upload             | Загрузка файла (CSV/Excel)        |
| GET   | /api/data/stats/{id}    | Получение статистики по файлу     |
| GET   | /api/data/clean/{id}    | Очистка данных                    |
| GET   | /api/data/plot/{id}     | Получение графика данных          |

## 📝 Примеры запросов

**Загрузка файла:**

curl -X POST -F "file=@test.csv" http://localhost:5000/api/upload


**Получение статистики:**

curl http://localhost:5000/api/data/stats/1


**Генерация графика:**

curl http://localhost:5000/api/data/plot/1 -o plot.png


## 🗄 Структура проекта


e-soft-analytics-api/
├── app/                  # Основное приложение
│   ├── __init__.py
│   ├── routes.py         # Эндпоинты API
│   └── models/
│       └── db_models.py  # Модели БД
├── utils/
│   └── data_processing.py # Анализ данных (Pandas)
├── config.py             # Конфигурации
├── requirements.txt      # Зависимости (включая openpyxl)
├── run.py                # Запуск для разработки
├── wsgi.py               # Production-конфигурация 
└── uploads/              # Папка для загруженных файлов


## 🔧 Настройка Production

1. Установите Gunicorn:

pip install gunicorn


2. Создайте файл `wsgi.py`:

from app import create_app
app = create_app('production')


3. Запустите сервер:

gunicorn -w 4 wsgi:app


## 📄 Лицензия

MIT License.
