FROM python:3.10-slim

RUN apt-get update &&  \
    apt-get install ffmpeg libsm6 libxext6 -y

ENV WORKDIR /app
WORKDIR $WORKDIR

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=60 \
    PYTHONPATH=$WORKDIR \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \

COPY poetry.lock pyproject.toml $WORKDIR/
COPY src $WORKDIR/src

RUN python3 -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-cache --no-root
