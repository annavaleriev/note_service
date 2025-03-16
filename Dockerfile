# 1. Используем официальный образ Python
FROM python:3.11-slim

# 2. Устанавливаем зависимости для Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# 3. Устанавливаем рабочую директорию
WORKDIR /app

# 4. Копируем только файлы, необходимые для установки зависимостей
COPY pyproject.toml poetry.lock /app/

# 5. Устанавливаем зависимости с помощью Poetry
RUN poetry install --no-root --no-dev  # --no-root исключает установку самого проекта, --no-dev исключает dev-зависимости

# 6. Копируем остальную часть проекта
COPY . /app/

# 7. Запускаем миграции и сервер
CMD ["poetry", "run", "python", "manage.py", "migrate"]
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
