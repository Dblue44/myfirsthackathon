FROM python:3.10.0-alpine

ENV WORKDIR /app
WORKDIR $WORKDIR

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=60 \
    PYTHONPATH=$WORKDIR

COPY poetry.lock pyproject.toml $WORKDIR/
COPY src $WORKDIR/src

RUN python3 -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
