FROM python:3.11.6-slim AS builder

RUN apt-get update && apt-get install -y curl make bash
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN poetry --version
RUN ls -l /app

RUN poetry install --with dev

COPY . /app
COPY .env /app/.env

RUN poetry run make check
RUN poetry run make tests

FROM python:3.11.6-slim AS final

RUN apt-get update && apt-get install -y curl make bash
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY --from=builder /app /app

WORKDIR /app

RUN poetry install --no-dev

COPY .env /app/.env
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
