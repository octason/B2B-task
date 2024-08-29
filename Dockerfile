FROM python:3.11-slim-bullseye


RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl git gnupg default-libmysqlclient-dev \
    #Begin of mandatory layers for Microsoft ODBC Driver 17 for Debian 11 Bullseye
    && rm -rf /var/lib/apt/lists/*

ARG INSTALL_DEV

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    VIRTUALENV=/venv \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    INSTALL_DEV=${INSTALL_DEV}

WORKDIR /app

# RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock /app/


RUN python3 -m venv $VIRTUALENV \
    && $VIRTUALENV/bin/pip3 install poetry==$POETRY_VERSION \
    && $VIRTUALENV/bin/poetry export --without-hashes --with dev -f requirements.txt -o requirements.txt \
    && $VIRTUALENV/bin/pip3 install --no-cache-dir -r requirements.txt

COPY . .
