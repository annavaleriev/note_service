FROM python:3.11-slim

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV}

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN if [ "$DJANGO_ENV" = "local" ]; then \
        poetry install --only=main,dev --no-interaction --no-ansi --no-root; \
    else \
        poetry install --only=main --no-interaction --no-ansi --no-root; \
    fi

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
