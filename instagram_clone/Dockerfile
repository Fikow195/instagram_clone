# 1. Базовый образ с Python
FROM python:3.13-slim

# 2. Рабочая директория внутри контейнера
WORKDIR /app

# 3. Скопировать файлы проекта внутрь контейнера
COPY . .

# 4. Установить зависимости (из requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Запустить сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
